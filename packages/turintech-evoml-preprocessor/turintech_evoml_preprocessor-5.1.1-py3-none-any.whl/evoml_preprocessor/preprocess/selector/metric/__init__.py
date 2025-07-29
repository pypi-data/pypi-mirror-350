from typing import Dict, Type

from evoml_preprocessor.preprocess.models import SelectionMetric
from evoml_preprocessor.preprocess.selector.util import MetricParameters

from ._base import Metric
from .constant import ConstantMetric
from .correlation import CorrelationMetric
from .ftest import FTestMetric
from .importance import FeatureImportanceMetric
from .ks import KSRelevancyMetric
from .mutual_information import MutualInformationMetric


def build_relevancy_metric(metric_type: SelectionMetric, parameters: MetricParameters) -> Metric:
    mapping: Dict[SelectionMetric, Type[Metric]] = {
        SelectionMetric.PEARSON: CorrelationMetric,
        SelectionMetric.SPEARMAN: CorrelationMetric,
        SelectionMetric.F_TEST: FTestMetric,
        SelectionMetric.KOLMOGOROV_SMIRNOV: KSRelevancyMetric,
        SelectionMetric.MUTUAL_INFORMATION: MutualInformationMetric,
        SelectionMetric.FEATURE_IMPORTANCE: FeatureImportanceMetric,
        SelectionMetric.NONE: ConstantMetric,
    }
    if metric_type not in mapping:
        raise ValueError(f"Invalid metric for relevancy: {metric_type}")
    return mapping[metric_type](parameters)


def build_redundancy_metric(metric_type: SelectionMetric, parameters: MetricParameters) -> Metric:
    mapping: Dict[SelectionMetric, Type[Metric]] = {
        SelectionMetric.PEARSON: CorrelationMetric,
        SelectionMetric.SPEARMAN: CorrelationMetric,
        SelectionMetric.MUTUAL_INFORMATION: MutualInformationMetric,
        SelectionMetric.NONE: ConstantMetric,
    }
    if metric_type not in mapping:
        raise ValueError(f"Invalid metric for redundancy: {metric_type}")
    return mapping[metric_type](parameters)


__all__ = [
    "Metric",
    "ConstantMetric",
    "CorrelationMetric",
    "FTestMetric",
    "KSRelevancyMetric",
    "MutualInformationMetric",
    "FeatureImportanceMetric",
    "build_relevancy_metric",
    "build_redundancy_metric",
]
