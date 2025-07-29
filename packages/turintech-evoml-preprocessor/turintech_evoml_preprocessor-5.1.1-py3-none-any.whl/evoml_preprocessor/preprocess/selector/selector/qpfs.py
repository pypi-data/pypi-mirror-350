"""This module provides the Quadratic Programming Feature Selection (QPFS) method."""

# ───────────────────────────────── imports ────────────────────────────────── #
# Standard libraries
from __future__ import annotations

import logging
from typing import Literal, Optional, Tuple

# Dependencies
import numpy as np
import pandas as pd
from cvxopt import matrix, solvers

# Private dependencies
from evoml_api_models import MlTask
from numpy.linalg import LinAlgError
from scipy.linalg import eigh, pinvh

# Module
from evoml_preprocessor.preprocess.models import SelectionMetric, SelectorType
from evoml_preprocessor.preprocess.selector.models import SelectionMethodReport
from evoml_preprocessor.preprocess.selector.selector import Selector
from evoml_preprocessor.preprocess.selector.util import SelectorParameters, SingleSelectionMetric

# ──────────────────────────────────────────────────────────────────────────── #
logger = logging.getLogger("preprocessor")
# NYSTROM_THRESHOLD is the minimum number of features required to use nyström approximation
NYSTROM_THRESHOLD = 150
# ─────────────────────────────────── Code ─────────────────────────────────── #


class QPFSelector(Selector):
    """Quadratic Programming Feature Selector.

    Quadratic Programming Feature Selection (QPFS) method, an alternative
    approach to feature selection that utilises quadratic programming to
    identify the optimal combination of features. These features, when combined,
    exhibit minimal redundancy and maximum relevance. In contrast, the
    Max-Relevance Min-Redundancy (mRMR) method employs an iterative approach,
    selecting the best feature at each iteration,
    which does not guarantee the best overall combination.

    Important:
        Please note that errors are suppressed. After fitting the selector,
        examine the 'selector.selected_features' attribute. If the selection
        process fails, the attribute will return an empty pandas.Index (pd.Index([])).
        On the other hand, if the selection is successful, the attribute will return
        a pandas.Index containing the selected features. Proceed to use the
        'transform' method to transform the data accordingly.

    Notes:
        If the 'nystrom' parameter is set to 'auto', the Nystrom approximation
        will be applied when the number of features exceeds the predefined
        NYSTROM_THRESHOLD.

        The Nystrom approximation is a technique used to estimate the kernel
        matrix by utilising a subset of the data. This approach is
        beneficial when dealing with a large number of features, as it
        reduces the size of the kernel matrix. Consequently, the
        problem becomes more manageable for the cvxopt quadratic
        programming solver. Although this approximation incurs a slight
        performance cost, the impact is minimal and can be disregarded.

    Glossary:
        All variable names are based on the paper's notations.

        - X: pd.DataFrame (# rows x d) is the feature matrix.
        - y: pd.Series (# rows,) is the target vector.
        - d: int is the number of features of X.
        - n: int is the number of features to select.
        - Q: np.ndarray (d x d) is the redundancy matrix of absolute dependency
            between features. In the case of Pearson correlation, Q contains
            absolute values of the correlation matrix.
        - F: np.ndarray (d,) is the relevancy vector of absolute dependency
            between features and the target. Similarly, in the case of Pearson
            correlation, F contains absolute values of the correlation vector.
        - alpha: float \\in [0, 1], is the scaling parameter.
            alpha = 1: only relevance is considered; the QP problem becomes linear
                and equivalent to the MaxRel criterion.
            alpha = 0: only independence between features is considered. Least
                correlated features are selected.

        When the Nystrom approximation is applied, the following notations are used:
        - r: int is the number of features used to approximate the matrix Q.
        - A: np.ndarray (r x r) is the kernel matrix.
        - L np.ndarray (r,) is the vector of eigenvalues of the approximation of Q.
        - U np.ndarray (d x r) is the matrix of eigenvectors of the approximation of Q.

    Redundancy options:
        - Pearson correlation

    Relevancy options:
        - Pearson correlation
        - F-test

    Possible improvements:
        Adding other redundancy and relevancy metrics is possible, but keep in
        mind that QPFS is known for its speed. Using information-theoretic or
        randomised metrics, like MI, MIC, and RDC, might lead to slightly better
        performance but with much higher computational costs.

        Pearson correlation is used mainly for its speed, even though it's biased
        towards continuous features. However, it still performs well compared to
        more demanding metrics like MI, MIC, and RDC when tested on dataset
        in Research Box.

        If you choose different metrics for redundancy and relevancy, make
        sure they're comparable in scale and normalized to the same range.
        Otherwise, the results might be biased and the alpha parameter could
        behave unpredictably.

    References:
        The original paper:
        https://www.jmlr.org/papers/volume11/rodriguez-lujan10a/rodriguez-lujan10a.pdf

    """

    def __init__(self, parameters: SelectorParameters):
        super().__init__(parameters)
        self.nystrom: Literal["auto", "yes", "no"] = parameters.nystrom
        self._report = SelectionMethodReport(method=SelectorType.QPFS)

        # internal variables
        self._d: int = 0  # number of features

    @property
    def name(self) -> str:
        return "qpfs"

    @classmethod
    def default(cls, ml_task: MlTask) -> QPFSelector:
        return cls(
            SelectorParameters(
                relevancy=[SingleSelectionMetric.from_selector(ml_task, metric=SelectionMetric.PEARSON)],
                redundancy=SingleSelectionMetric.from_selector(ml_task, metric=SelectionMetric.PEARSON),
            )
        )

    def fit(self, X: pd.DataFrame, y: pd.Series, n: int) -> None:
        """Fit the selector to the data.

        Args:
            X (pd.DataFrame): The features.
            y (pd.Series): The target.
            n (int): The number of features to select.

        """

        self.init_fit(X, y, n)  # initial setup

        self._d = X.shape[1]

        # order features is decreasing order of importance
        if self.nystrom == "yes" or self._d > NYSTROM_THRESHOLD and self.nystrom == "auto":
            best_cols = self._nystrom_approximated_solution(X, y)

        else:
            best_cols = self._full_solution(X, y)

        # if the solver failed, show a warning and fall back to mRMR
        if best_cols is None:
            logger.warning("QPFS failed to find a solution.")
            return

        # select the best n features
        self.selected_features = best_cols[:n]

        # calculate scores
        scores = pd.Series(np.arange(len(best_cols), 0, -1), index=best_cols)
        self.scores.combined[scores.index] = scores

        self._generate_report()

    def _full_solution(self, X: pd.DataFrame, y: pd.Series) -> Optional[pd.Index]:
        """Full solution without Nystrom approximation.

        Args:
            X (pd.DataFrame): The features.
            y (pd.Series): The target.

        Returns:
            pd.Index | None: Indexes of selected columns.
                None if the solver failed.

        """

        # compute redundancy matrix and relevancy vector
        Q, F = self._compute_matrices(X, y)

        # alpha balancing parameter
        q_mean = np.mean(Q)
        alpha = q_mean / (q_mean + np.mean(F))

        try:
            # Convert to cvxopt matrices
            p_cvxopt = matrix((1 - alpha) * Q, tc="d")
            q_cvxopt = matrix(alpha * F * -1, tc="d")
            g_cvxopt = matrix(-1 * np.eye(self._d), tc="d")
            h_cvxopt = matrix(np.zeros(shape=(self._d, 1)), tc="d")
            a_cvxopt = matrix(np.ones(self._d), (1, self._d), tc="d")
            b_cvxopt = matrix(1.0, tc="d")

            # Solve the quadratic program
            solvers.options["show_progress"] = False
            sol = solvers.qp(p_cvxopt, q_cvxopt, g_cvxopt, h_cvxopt, a_cvxopt, b_cvxopt)

            # get solution
            x = np.array(sol["x"]).flatten()

            indexes = np.argsort(x)[::-1]

        except Exception:
            return None

        return X.columns[indexes]

    def _nystrom_approximated_solution(self, x: pd.DataFrame, y: pd.Series) -> Optional[pd.Index]:
        """Nystrom approximated solution.

        Args:
            x (pd.DataFrame): The features.
            y (pd.Series): The target.

        Returns:
            pd.Index | None: Indexes of selected columns.
                None if either of the two failed:
                    - calculating eigendecomposition of the Q approximation.
                    - solving the quadratic program.

        """

        # store original column order
        cols = x.columns

        r = int(self._sampling_rate(self._d) * self._d)

        feature_indexes = self.rng.choice(self._d, size=r, replace=False, shuffle=False)
        rest_indexes = np.setdiff1d(np.arange(self._d), feature_indexes)
        reordered_indexes = np.concatenate((feature_indexes, rest_indexes))

        # reorder columns of X with the chosen indexes being first
        x = x.iloc[:, reordered_indexes]

        # compute redundancy matrix and relevancy vector
        Q, F = self._compute_matrices(x, y, r)

        A = Q[:, :r]
        B = Q[:, r:]

        # alpha balancing parameter
        try:
            q_mean = np.mean(np.vstack((Q, np.abs(np.hstack((B.T, B.T @ pinvh(A) @ B))))))

        except LinAlgError:
            return None

        alpha = float(q_mean / (q_mean + np.mean(F)))  # floating[Any] -> float

        try:
            L, U = self._compute_nystrom_eigendecomposition(A, B)

        except LinAlgError:
            return None

        try:
            x_array: np.ndarray = self._formulate_and_solve_nystrom_qp(L, U, F, alpha)

            if x_array is None or np.isnan(x_array).any():
                return None

        except Exception:
            return None

        sorted_indexes_x = np.argsort(x_array)[::-1]

        return cols[reordered_indexes][sorted_indexes_x]

    def _formulate_and_solve_nystrom_qp(
        self, l_vec_eigenvalues: np.ndarray, u_matrix_eigenvalues: np.ndarray, f_vector: np.ndarray, alpha: float
    ) -> np.ndarray:
        """Formulate and solve the quadratic programming problem.

        Args:
            l_vec_eigenvalues (np.ndarray): (r,) The L vector of eigenvalues.
            u_matrix_eigenvalues (np.ndarray): (d x r) The U matrix of eigenvectors.
            f_vector (np.ndarray): (d,) The vector F.
            alpha (float): The alpha balancing parameter.

        Returns:
            np.ndarray: (d,) The solution vector.

        """

        # Convert to cvxopt matrices
        p_cvxopt = matrix(np.diag(l_vec_eigenvalues * (1 - alpha)), tc="d")
        q_cvxopt = matrix((f_vector * alpha) @ u_matrix_eigenvalues * -1, tc="d")
        g_cvxopt = matrix((u_matrix_eigenvalues * -1), tc="d")
        h_cvxopt = matrix(np.zeros(shape=(self._d, 1)), tc="d")
        a_cvxopt = matrix(np.sum(u_matrix_eigenvalues, axis=0).reshape(1, -1), tc="d")
        b_cvxopt = matrix(1, tc="d")

        # Solve the quadratic program
        solvers.options["show_progress"] = False
        solution = solvers.qp(p_cvxopt, q_cvxopt, g_cvxopt, h_cvxopt, a_cvxopt, b_cvxopt)
        y = np.array(solution["x"]).flatten()

        return u_matrix_eigenvalues @ y

    @staticmethod
    def _compute_nystrom_eigendecomposition(A: np.ndarray, B: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Compute the eigendecomposition of the Q approximation.

        Args:
            A (np.ndarray): (r x r) The top-left square block of the matrix Q.
            B (np.ndarray): (r x (d - r)) The top-right block of the matrix Q.

        Returns:
            np.ndarray: (r,) The L vector of eigenvalues.
            np.ndarray: (d x r) The U matrix of eigenvectors.

        """

        A_inv = pinvh(A)

        a_inv_evals, a_inv_evects = eigh(A_inv)
        sqrt_A_evals = np.sqrt(np.abs(a_inv_evals))
        a_inv_sqrt = a_inv_evects @ np.diag(sqrt_A_evals) @ a_inv_evects.T

        S = A + a_inv_sqrt @ B @ B.T @ a_inv_sqrt
        s_evals, s_evects = eigh(S)

        l_inv_sqrt = np.diag(np.sqrt(np.abs(1 / s_evals)))

        L = np.abs(s_evals)[::-1]
        U = np.vstack((A, B.T)) @ a_inv_sqrt @ s_evects @ l_inv_sqrt
        U = U[:, ::-1]

        return L, U

    @staticmethod
    def _sampling_rate(d: int) -> float:
        """Compute the sampling rate.

        The formula to compute the sampling rate is:

        .. math::
            max(0.1, min(0.9, 1.60498870 - 0.15738818 * lnx))

        The formula was chosen to approximate the following X, Y distribution:
            X (n features):
                [150, 300, 600, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 10000]
            Y (Sampling Rate):
                [0.8, 0.70, 0.65, 0.5, 0.4, 0.35, 0.3, 0.26, 0.23, 0.22, 0.15]

            But the sampling rate cannot be less than 0.1 or greater than 0.9.

        Args:
            d (int): The number of features.

        Returns:
            float: The sampling rate.

        References:
            Tool used to approximate the distribution:
            https://planetcalc.com/5992/

        """

        return max(0.1, min(0.9, 1.60498870 - 0.15738818 * np.log(d)))

    def _compute_matrices(
        self, x: pd.DataFrame, y: pd.Series, r: Optional[int] = None
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Compute the Q and F matrices.

        Q is the redundancy matrix of absolute dependency between features.
        F is the relevancy vector of absolute dependency between features
        and the target.

        The default redundancy metric is the Pearson correlation due to high
        computational cost of other metrics, such as MIC and RDC.

        The default relevancy metric is the Pearson correlation,
        but ANOVA F-value can be used as well.

        In the case of Pearson correlation, we use the absolute value of the
        correlation coefficient, as we are only interested in the power of the
        correlation.

        Notes:
            Explain that X might be reordered and in this case we will calculate only the first r features.

        Args:
            x (pd.DataFrame): The feature matrix.
            y (pd.Series): The target vector.
            r (int | None): The number of consecutive features of the reordered
                X to use for redundancy calculation.
                If None, the matrices are computed for all features.

        Returns:
            np.ndarray:
                (d x d) The Q matrix if r is None.
                (r x d) The Q matrix if r is not None.
            np.ndarray: (d,) The F vector.

        """

        # Relevancy vector
        metric = self.relevancy_metrics[0]
        F = metric.evaluate(x, y).to_numpy()
        F = np.abs(F)

        # Redundancy matrix
        if r is not None:
            Q = self.redundancy_metric.matrix_evaluate_numpy(x, x.iloc[:, :r])
        else:
            Q = self.redundancy_metric.matrix_evaluate(x).to_numpy()

        return Q, F

    def _generate_report(self) -> None:
        super()._generate_report()
        self.report.relevancyMetricReports = [m.report for m in self.relevancy_metrics]
        # there's an edge case here where redundancy isn't called (if n_features == 1)
        try:
            self.report.redundancyMetricReport = self.redundancy_metric.report
        except AttributeError:
            self.report.redundancyMetricReport = None
