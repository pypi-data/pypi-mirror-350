"""
This module contains the wrapper class for the HuggingFace transformer models.
"""

import json
import logging
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Union, Optional, List, Tuple, Iterable

import numpy as np
import pandas as pd
import torch
from transformers import PretrainedConfig, AutoTokenizer, AutoModel, AutoConfig, PreTrainedModel, PreTrainedTokenizer

from evoml_preprocessor.preprocess.models import EmbeddingTransformer
from evoml_preprocessor.preprocess.models.enum import ProteinEmbeddingTransformer
from evoml_preprocessor.utils.conf.conf_manager import conf_mgr
from evoml_preprocessor.utils.requirements import _onnxruntime_installed, _optimum_installed


# ──────────────────────────────────────────────────────────────────────────── #
# Logger
logger = logging.getLogger("preprocessor")
# ──────────────────────────────────────────────────────────────────────────── #


def init_ort_model(model_path: Path, config_path: Path, device: Optional[str] = None):
    """Initiates an optimus ORTModel with the given model onnx and config paths.
    If the device is not specified, it will use the GPU if available, otherwise
    it will use the CPU.

    Args:
        model_path (Path):
            The path to the model onnx file.
        config_path (Path):
            The path to the model config file.
        device (str):
            The device to use. Defaults to None.
    Returns:
        ORTModel:
            The ORTModel.
    """

    from onnxruntime import InferenceSession, SessionOptions, GraphOptimizationLevel
    from optimum.onnxruntime import ORTModelForFeatureExtraction

    device = device or "cpu"
    opts = SessionOptions()
    providers = None
    if device == "cpu":
        providers = ["CPUExecutionProvider"]
        opts.inter_op_num_threads = 1
        opts.intra_op_num_threads = conf_mgr.preprocess_conf.THREADS
        opts.graph_optimization_level = GraphOptimizationLevel.ORT_ENABLE_ALL
    with open(config_path) as config_f:
        config = PretrainedConfig.from_dict(json.load(config_f))
    model = InferenceSession(str(model_path), providers=providers, sess_options=opts)
    return ORTModelForFeatureExtraction(model, config)


class HuggingFaceWrapper:
    def __init__(
        self, encoder_slug: Union[EmbeddingTransformer, ProteinEmbeddingTransformer], device: Optional[str] = None
    ):
        self.max_length = None
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.pool = True
        self.batch_size = 16 if device == "cuda" else 128

        self.encoder_slug = encoder_slug.get_huggingface_encoder()

        logger.info(f"→ initializing HuggingFace transformer {self.encoder_slug} on {self.device} device")

        self._initialize_model()

    def _initialize_model(self) -> None:
        if self.encoder_slug == EmbeddingTransformer.XLNET_BASE_CASED:
            self._initialize_xlnet_model()
        else:
            self._initialize_general_model()
        self.config = AutoConfig.from_pretrained(self.encoder_slug)

        self._optimize_onnx_model()
        self._set_max_length()

    def _initialize_xlnet_model(self) -> None:
        from transformers import XLNetTokenizer, XLNetModel

        self.tokenizer = XLNetTokenizer.from_pretrained(EmbeddingTransformer.XLNET_BASE_CASED.value)
        self.model = XLNetModel.from_pretrained(EmbeddingTransformer.XLNET_BASE_CASED.value)

    def _initialize_general_model(self) -> None:
        self.tokenizer = AutoTokenizer.from_pretrained(self.encoder_slug)
        self.model = AutoModel.from_pretrained(self.encoder_slug)

    def _set_max_length(self) -> None:
        self.max_length = getattr(self.tokenizer, "model_max_length", None)
        if self.max_length is not None and hasattr(self.model.config, "max_position_embeddings"):
            self.max_length = min(self.max_length, self.model.config.max_position_embeddings)

    def _optimize_onnx_model(self) -> None:
        def _dependencies_imported_successfully() -> bool:
            try:
                from transformers.onnx import export, FeaturesManager
                from optimum.onnxruntime import ORTOptimizer, ORTQuantizer
                from optimum.onnxruntime.configuration import OptimizationConfig, AutoQuantizationConfig

                return True
            except (ImportError, RuntimeError):
                logger.warning("ONNX dependencies import failed, falling back to PyTorch")
                return False

        def _convert_to_onnx(tmp_path: Path, model: PreTrainedModel, tokenizer: PreTrainedTokenizer) -> bool:
            try:
                model_kind, model_onnx_config = FeaturesManager.check_supported_model_or_raise(model, feature="default")
                onnx_config = model_onnx_config(model.config)
                _, _ = export(
                    preprocessor=tokenizer, model=model, config=onnx_config, opset=13, output=tmp_path / "model.onnx"
                )
                model.config.to_json_file(tmp_path / "config.json")
                return True
            except:
                logger.warning("ONNX conversion failed, falling back to PyTorch")
                return False

        def _optimize_onnx_model(tmp_path) -> None:
            try:
                optimizer = ORTOptimizer.from_pretrained(tmp_path)
                optimization_config = OptimizationConfig(
                    optimization_level=99, optimize_with_onnxruntime_only=False, optimize_for_gpu=False
                )
                optimizer.optimize(save_dir=tmp_path, optimization_config=optimization_config, file_suffix=None)
            except:
                logger.warning("ONNX optimization failed")

        def _quantize_onnx_model(tmp_path) -> None:
            try:
                quantizer = ORTQuantizer.from_pretrained(tmp_path)
                dqconfig = AutoQuantizationConfig.avx512_vnni(is_static=False, per_channel=False)
                quantizer.quantize(save_dir=tmp_path, quantization_config=dqconfig, file_suffix=None)
            except:
                logger.warning("ONNX quantization failed")

        if (
            self.device == "cpu"
            and _optimum_installed()
            and _onnxruntime_installed()
            and _dependencies_imported_successfully()
        ):
            from transformers.onnx import export, FeaturesManager
            from optimum.onnxruntime import ORTOptimizer, ORTQuantizer
            from optimum.onnxruntime.configuration import OptimizationConfig, AutoQuantizationConfig

            with TemporaryDirectory() as f:
                tmp_path = Path(f) / "model"
                tmp_path.mkdir(parents=True)
                if _convert_to_onnx(tmp_path, self.model, self.tokenizer):
                    logger.info("Optimizing ONNX transformer")
                    _optimize_onnx_model(tmp_path)
                    _quantize_onnx_model(tmp_path)
                    self.batch_size = 1
                    self.model = init_ort_model(tmp_path / "model.onnx", tmp_path / "config.json", self.device)
                    logger.info("ONNX optimization complete")
        else:
            self.model.to(self.device)

    @staticmethod
    def _batch(iterable: List[str], n: int = 1) -> Iterable[Tuple[List[str], int, int]]:
        """Yield successive n-sized chunks from iterable.
        Args:
            iterable (List[str]):
                The iterable to batch
            n (int):
                The size of the batch
        Returns:
            A batch of size n
        """

        l = len(iterable)
        for ndx in range(0, l, n):
            start = ndx
            end = min(ndx + n, l)
            yield iterable[start:end], start, end

    def fit_transform(self, data: pd.Series) -> pd.DataFrame:
        """Fit and transform the data.
        Args:
            data (pd.Series):
                The data to fit and transform
        Returns:
            pd.DataFrame:
                A dataframe of the embeddings
        """

        return self.transform(data)

    def transform(self, data: pd.Series) -> pd.DataFrame:
        """Transform the data.
        Args:
            data (pd.Series):
                The data to transform
        Returns:
            pd.DataFrame:
                A dataframe of the embeddings
        """

        # Tokenize the sentences
        if self.encoder_slug in [EmbeddingTransformer.XLNET_BASE_CASED, EmbeddingTransformer.GPT2]:
            if self.encoder_slug == EmbeddingTransformer.GPT2:
                # GPT2 tokenizer requires us to set a pad token
                self.tokenizer.pad_token = self.tokenizer.eos_token
            self.pool = False
        return self._transformer_embedding(data)

    def _transformer_embedding(self, data: pd.Series) -> pd.DataFrame:
        sentences = data.tolist()

        # Pre-allocate Result array
        num_dimensions = self.config.hidden_size
        sentence_embeddings = np.zeros((len(sentences), num_dimensions), dtype=np.float32)

        for batch_sentences, start_index, end_index in self._batch(sentences[0:], n=self.batch_size):

            # tokenize sentences
            # set max_length to model_max_length, as this varies based on the model selected
            encoded_input = self.tokenizer(
                batch_sentences, padding=True, truncation=True, max_length=self.max_length, return_tensors="pt"
            )
            encoded_input.to(self.device)

            with torch.no_grad():
                model_output = self.model(**encoded_input)

            # Concat the batched results to build the final result
            if self.pool:
                # Perform pooling. In this case, mean pooling
                pooled_embeddings = self.mean_pooling(model_output, encoded_input["attention_mask"])

                # Concat the batch results
                embedded_batch = pooled_embeddings.cpu().numpy()

                sentence_embeddings[start_index:end_index] = embedded_batch
            else:
                #  Perform [CLS] embedding extraction
                embedded_batch = model_output.last_hidden_state[:, 0, :].cpu().numpy()

                sentence_embeddings[start_index:end_index] = embedded_batch

        columns = [f"{i}" for i in range(sentence_embeddings.shape[1])]
        return pd.DataFrame(sentence_embeddings, index=data.index, columns=columns)

    def mean_pooling(self, model_output, attention_mask):
        """Perform mean pooling on the model output.
        Args:
            model_output:
                The model output
            attention_mask:
                The attention mask
        Returns:
            The mean pooled output
        """

        token_embeddings = model_output[0]  # First element of model_output contains all token embeddings
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)
        sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
        return sum_embeddings / sum_mask
