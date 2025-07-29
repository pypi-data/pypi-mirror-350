"""Contain the different estimators of the library."""

from abc import abstractmethod, ABC

import math
import inspect
import warnings
import platform

from sklearn.base import BaseEstimator
from sklearn.utils.validation import check_is_fitted
from sklearn.utils.extmath import safe_sparse_dot, softmax
from sklearn.exceptions import ConvergenceWarning

from collections import defaultdict

import concurrent.futures

import numpy as np
import scipy.sparse

from sklearn.utils import ClassifierTags, RegressorTags

import torch

from cyanure_gpu.data_processing import check_input_fit, check_input_inference, windows_conversion

from cyanure_gpu.logger import setup_custom_logger

from cyanure_gpu.erm.param.model_param import ModelParameters
from cyanure_gpu.erm.param.problem_param import ProblemParameters

from cyanure_gpu.erm.simple_erm import SimpleErm
from cyanure_gpu.erm.multi_erm import MultiErm

from cyanure_gpu.constants import DEVICE, TENSOR_TYPE, ARRAY_TYPE

torch.backends.cudnn.benchmark = False
np.random.seed(0)
torch.manual_seed(0)
torch.set_default_dtype(TENSOR_TYPE)
torch.set_printoptions(precision=20)

logger = setup_custom_logger("INFO")


class ERM(BaseEstimator, ABC):
    """
    The generic class for empirical risk minimization problems.

    For univariates problems, minimizes

        min_{w,b} (1/n) sum_{i=1}^n L( y_i, <w, x_i> + b)   + psi(w)

    """

    def __sklearn_tags__(self):
        tags = super().__sklearn_tags__()
        return tags

    def _warm_start(self, X, initial_weight, nclasses):
        if self.warm_start and hasattr(self, "coef_"):
            if self.verbose:
                logger.info("Restarting with current coefficients")
            if self.fit_intercept:
                initial_weight[-1, ] = np.squeeze(self.intercept_)
                initial_weight[0:-1, ] = np.squeeze(self.coef_)
            else:
                initial_weight = np.squeeze(self.coef_)

        if self.warm_start and self.solver in ('auto', 'miso', 'catalyst-miso', 'qning-miso'):
            n = X.shape[0]
            # TODO Ecrire test pour dual surtout défensif
            reset_dual = np.any(self.dual is None)
            if not reset_dual and self._binary_problem:
                reset_dual = self.dual.shape[0] != n
            if not reset_dual and not self._binary_problem:
                reset_dual = np.any(self.dual.shape != [n, nclasses])
            if reset_dual and self.verbose:
                logger.info("Resetting dual")
            if reset_dual and self._binary_problem:
                self.dual = np.zeros(
                    n, dtype=X.dtype, order='F')
            if reset_dual and not self._binary_problem:
                self.dual = np.zeros(
                    [n, nclasses], dtype=X.dtype, order='F')

        return initial_weight

    def _initialize_weight(self, X, labels):
        nclasses = 0
        p = X.shape[1] + 1 if self.fit_intercept else X.shape[1]
        if self._binary_problem:
            initial_weight = np.zeros((p))
            yf = np.squeeze(labels)
        else:
            if labels.squeeze().ndim > 1:
                nclasses = labels.squeeze().shape[1]
                yf = np.asfortranarray(labels.T)
            else:
                nclasses = len(np.unique(labels))
                if platform.system() == "Windows":
                    yf = np.squeeze(np.intc(np.float64(labels)))
                else:
                    yf = np.squeeze(np.int32(labels))
            initial_weight = np.zeros([p, nclasses], order='F')

        initial_weight = self._warm_start(X, initial_weight, nclasses)

        initial_weight = np.asfortranarray(initial_weight, ARRAY_TYPE)

        return initial_weight, yf, nclasses

    def _multiclass_logistic(self, labels: torch.Tensor) -> str:
        if self.loss == "logistic":
            if (self.multi_class == "multinomial" or (self.multi_class == "auto" and not self._binary_problem)):
                if len(np.unique(labels)) != 2:

                    self._binary_problem = False

                    logger.info("Loss has been set to multiclass-logistic because "
                                "the multiclass parameter is set to multinomial!")

                    return "multiclass-logistic"
                else:
                    return self.loss

    def _check_max_iter(self):
        for index in range(self.n_iter_.shape[0]):
            if self.n_iter_[index] == self.max_iter:
                warnings.warn(
                    "The max_iter was reached which means the coef_ did not converge",
                    ConvergenceWarning)

    def __init__(self, loss='square', penalty='l2', fit_intercept=False, dual=None, tol=1e-3,
                 solver="auto", random_state=0, max_iter=2000, fista_restart=60,
                 verbose=True, warm_start=False, limited_memory_qning=50, multi_class="auto",
                 lambda_1=0, lambda_2=0, lambda_3=0, duality_gap_interval=5, n_threads=-1, safe=True):
        r"""
        Instantiate the ERM class.

        Parameters
        ----------
        loss: string, default='square'
            Loss function to be used. Possible choices are

                - 'square'
                    :math:`L(y,z) = \\frac{1}{2} ( y-z)^2`
                - 'logistic'
                    :math:`L(y,z) = \\log(1 + e^{-y z} )`
                - 'multiclass-logistic'
                    which is also called multinomial or softmax logistic:
                    .. math::`L(y, W^\\top x + b) = \\sum_{j=1}^k
                    \\log\\left(e^{w_j^\\top + b_j} - e^{w_y^\\top + b_y} \\right)`

        penalty (string): default='none'
            Regularization function psi. Possible choices are

            For binary_problem problems:

            - 'none'
                :math:`psi(w) = 0`
            - 'l2'
                :math:`psi(w) = \\frac{\\lambda_1}{2} ||w||_2^2`
            - 'l1'
                :math:`psi(w) = \\lambda_1 ||w||_1`

            For multivariate problems, the previous penalties operate on each
            individual (e.g., class) predictor.

            .. math::
                \\psi(W) = \\sum_{j=1}^k \\psi(w_j).

        fit_intercept (boolean): default='False'
            Learns an unregularized intercept b  (or several intercepts for
            multivariate problems)

        lambda_1 (float): default=0
            First regularization parameter

        lambda_2 (float): default=0
            Second regularization parameter, if needed

        lambda_3 (float): default=0
            Third regularization parameter, if needed

        solver (string): default='auto'
            Optimization solver. Possible choices are

            - 'ista'
            - 'ista-barzilai'
            - 'fista'
            - 'catalyst-ista'
            - 'qning-ista'  (proximal quasi-Newton method)
            - 'auto'

            see the Latex documentation for more details.
            If you are unsure, use 'auto'

        tol (float): default='1e-3'
            Tolerance parameter. For almost all combinations of loss and
            penalty functions, this parameter is based on a duality gap.
            Assuming the (non-negative) objective function is "f" and its
            optimal value is "f^*", the algorithm stops with the guarantee

            :math:`f(x_t) - f^*  <=  tol f(x_t)`

        max_iter (int): default=500
            Maximum number of iteration of the algorithm in terms of passes
            over the data

        duality_gap_interval (int): default=10
            Frequency of duality-gap computation

        verbose (boolean): default=True
            Display information or not

        n_threads (int): default=-1
            Maximum number of cores the method may use (-1 = all cores).
            Note that more cores is not always better.

        random_state (int): default=0
            Random seed

        warm_start (boolean): default=False
            Use a restart strategy

        binary_problem (boolean): default=True
            univariate or multivariate problems

        limited_memory_qning (int): default=20
            Memory parameter for the qning method

        fista_restart (int): default=50
            Restart strategy for fista (useful for computing regularization path)

        multi_class (string): default="auto"
            Determine the comportment of the instance in case of multivariate problem (for classification)

        """
        self.loss = loss
        self.penalty = penalty
        self.fit_intercept = fit_intercept
        self.dual = dual
        self.solver = solver
        self.tol = tol
        self.random_state = random_state
        self.max_iter = max_iter
        self.lambda_1 = lambda_1
        self.lambda_2 = lambda_2
        self.lambda_3 = lambda_3
        self.limited_memory_qning = limited_memory_qning
        self.fista_restart = fista_restart
        self.verbose = verbose
        self.warm_start = warm_start
        self.multi_class = multi_class
        self.duality_gap_interval = duality_gap_interval
        self.n_threads = n_threads
        self.safe = safe

    def fit(self, X, labels, le_parameter=None):
        """
        Fit the parameters.

        Parameters
        ----------
            X (numpy array):
                input n X p numpy matrix; the samples are on the rows

            y (numpy array):
                - vector of size n with real values for regression
                - vector of size n with {-1,+1} for binary classification,
                  which will be automatically converted if {0,1} are
                  provided
                - matrix of size n X k for multivariate regression
                - vector of size n with entries in {0,1,k-1} for classification
                  with k classes

        Returns
        -------
            self (ERM):
                Returns the instance
        """
        labels = np.squeeze(labels)
        initial_weight, yf, nclasses = self._initialize_weight(X, labels)

        initial_weight_torch = torch.from_numpy(initial_weight).to(DEVICE)

        if scipy.sparse.issparse(X):
            raise TypeError("Sparse data are not supported")
        else:
            training_data_fortran = np.asfortranarray(X.T, ARRAY_TYPE)

        weight_torch = torch.clone(initial_weight_torch)

        training_data_fortran, yf = windows_conversion(training_data_fortran, yf)
        labels_gpu = torch.from_numpy(yf).to(DEVICE)
        training_data_gpu = torch.from_numpy(training_data_fortran).to(DEVICE)

        loss = None
        self.le_ = le_parameter

        loss = self._multiclass_logistic(labels)

        if loss is None:
            loss = self.loss

        self.duality_gap_interval = -1 if self.duality_gap_interval <= 0 else min(self.duality_gap_interval, self.max_iter)

        model_parameter = ModelParameters(int(self.max_iter), float(self.tol), int(self.duality_gap_interval),
                                          500, 1, int(self.n_threads), int(self.limited_memory_qning),
                                          int(self.fista_restart), bool(self.verbose), False, self.solver)

        problem_parameter = ProblemParameters(float(self.lambda_1), float(self.lambda_2), float(self.lambda_3),
                                              bool(self.fit_intercept), self.penalty, loss=loss)

        optim_info = torch.empty

        if self.dual is not None:
            dual_torch = torch.from_numpy(self.dual).to(DEVICE)
        else:
            dual_torch = None

        with torch.no_grad():
            if self._binary_problem:
                erm = SimpleErm(initial_weight_torch, weight_torch, problem_parameter,
                                model_parameter, optim_info, dual_variable=dual_torch)
                self.optimization_info_, w = erm.solve_problem(training_data_gpu, labels_gpu)
            else:
                erm = MultiErm(initial_weight_torch, weight_torch, problem_parameter,
                               model_parameter, optim_info, dual_variable=dual_torch)
                if len(yf.shape) == 1:
                    self.optimization_info_, w = erm.solve_problem_vector(training_data_gpu, labels_gpu)
                else:
                    self.optimization_info_, w = erm.solve_problem_matrix(training_data_gpu, labels_gpu)

        if ("cuda" in DEVICE.type):
            w = w.cpu().numpy()
        else:
            w = w.numpy()

        self.n_iter_ = np.array([self.optimization_info_[class_index][0][-1]
                                for class_index in range(self.optimization_info_.shape[0])])

        self._check_max_iter()

        if self.fit_intercept:
            self.intercept_ = w[-1, ]
            self.coef_ = w[0:-1, ]
        else:
            self.coef_ = w

        self.n_features_in_ = self.coef_.shape[0]
        return self

    @abstractmethod
    def predict(self, X):
        """Predict the labels given an input matrix X (same format as fit)."""

    def get_weights(self):
        """
        Get the model parameters (either w or the tuple (w,b)).

        Returns
        -------
            w or (w,b) (numpy.array or tuple of numpy.array):
                Model parameters
        """
        return (self.coef_, self.intercept_) if self.fit_intercept else self.coef_

    def get_params(self, deep=True):
        """
        Get parameters for the estimator.

        Parameters
        ----------
            deep (bool, optional):
                If True returns also subobjects that are estimators. Defaults to True.

        Returns
        -------
            params (dict):
                Parameters names and values
        """
        out = {}
        for key in self._get_param_names():
            try:
                value = getattr(self, key)
            except AttributeError:
                value = None
            if deep and hasattr(value, 'get_params'):
                deep_items = value.get_params().items()
                out.update((key + '__' + k, val) for k, val in deep_items)
            out[key] = value
        return out

    @classmethod
    def _get_param_namesrestart(cls):
        init = getattr(cls.__init__, 'deprecated_original', cls.__init__)
        if init is object.__init__:
            # No explicit constructor to introspect
            return []

        # introspect the constructor arguments to find the model parameters
        # to represent
        init_signature = inspect.signature(init)
        # Consider the constructor parameters excluding 'self'
        parameters = [p for p in init_signature.parameters.values()
                      if p.name != 'self' and p.kind != p.VAR_KEYWORD]
        for p in parameters:
            if p.kind == p.VAR_POSITIONAL:
                raise RuntimeError()
        # Extract and sort argument names excluding 'self'
        return sorted([p.name for p in parameters])

    def set_params(self, **params):
        """
        Allow to change the value of parameters.

        Parameters
        ----------
            params (dict):
                Estimator parameters to set

        Raises
        ------
            ValueError:
                The parameter does not exist

        Returns
        -------
            self (ERM):
                Estimator instance
        """
        if not params:
            # Simple optimization to gain speed (inspect is slow)
            return self
        valid_params = self.get_params(deep=True)

        # Grouped by prefix
        nested_params = defaultdict(dict)
        for key, value in params.items():
            key, delim, sub_key = key.partition('__')
            if key not in valid_params:
                raise ValueError(f'Invalid parameter {key} for estimator {self}. '
                                 'Check the list of available parameters '
                                 'with `estimator.get_params().keys()`.')

            if delim:
                nested_params[key][sub_key] = value
            else:
                setattr(self, key, value)
                valid_params[key] = value

        for key, sub_params in nested_params.items():
            valid_params[key].set_params(**sub_params)
        return self

    def densify(self):
        """
        Convert coefficient matrix to dense array format.

        Converts the ``coef_`` member (back) to a numpy.ndarray. This is the
        default format of ``coef_`` and is required for fitting, so calling
        this method is only required on models that have previously been
        sparsified; otherwise, it is a no-op.

        Returns
        -------
        self (ERM):
            Fitted estimator converted to dense estimator

        """
        msg = "Estimator, %(name)s, must be fitted before densifying."
        check_is_fitted(self, msg=msg)
        if scipy.sparse.issparse(self.coef_):
            self.coef_ = self.coef_.toarray()
        return self


class ClassifierAbstraction(ERM):
    """A class to define abstract methods for classifiers."""

    @abstractmethod
    def predict_proba(self, X):
        """
        Estimate the probability for each class.

        Parameters
        ----------
            X (numpy array):
                Data matrix for which we want probabilities

        Returns
        -------
            proba (numpy.array):
                Return the probability of the samples for each class.
        """
        pass


class Regression(ERM):
    r"""
    The regression class which derives from ERM.

    The goal is to minimize the following objective:

        .. math::
            \min_{w,b} \frac{1}{n} \sum_{i=1}^n
            L\left( y_i, w^\top x_i + b\right) + \psi(w),

        where :math:`L` is a regression loss, :math:`\\psi` is a
        regularization function (or constraint), :math:`w` is a p-dimensional
        vector representing model parameters, and b is an optional
        unregularized intercept., and the targets will be real values.

    Parameters
    ----------
        loss (string): default='square'
            Loss function to be used. Possible choices are:
            Only the square loss is implemented at this point. Given two
            k-dimensional vectors y,z:

            * 'square' =>  :math:`L(y,z) = \frac{1}{2}( y-z)^2`

        penalty (string): default='none'
            Regularization function psi. Possible choices are

            For binary_problem problems:

            - 'none'
                :math:`psi(w) = 0`
            - 'l2'
                :math:`psi(w) = \frac{\lambda_1}{2} ||w||_2^2`
            - 'l1
                :math:`psi(w) = \lambda_1 ||w||_1`

            For multivariate problems, the previous penalties operate on each
            individual (e.g., class) predictor.

            .. math::
                \psi(W) = \sum_{j=1}^k \psi(w_j).

        fit_intercept (boolean): default='False'
            Learns an unregularized intercept b  (or several intercepts for
            multivariate problems)

        lambda_1 (float): default=0
            First regularization parameter

        lambda_2 (float): default=0
            Second regularization parameter, if needed

        lambda_3 (float): default=0
            Third regularization parameter, if needed

        solver (string): default='auto'
            Optimization solver. Possible choices are

            - 'ista'
            - 'ista-barzilai'
            - 'fista'
            - 'catalyst-ista'
            - 'qning-ista'  (proximal quasi-Newton method)
            - 'auto'

            see the Latex documentation for more details.
            If you are unsure, use 'auto'

        tol (float): default='1e-3'
            Tolerance parameter. For almost all combinations of loss and
            penalty functions, this parameter is based on a duality gap.
            Assuming the (non-negative) objective function is "f" and its
            optimal value is "f^*", the algorithm stops with the guarantee

            :math:`f(x_t) - f^*  <=  tol f(x_t)`

        max_iter (int): default=500
            Maximum number of iteration of the algorithm in terms of passes
            over the data

        duality_gap_interval (int): default=10
            Frequency of duality-gap computation

        verbose (boolean): default=True
            Display information or not

        n_threads (int): default=-1
            Maximum number of cores the method may use (-1 = all cores).
            Note that more cores is not always better.

        random_state (int): default=0
            Random seed

        warm_start (boolean): default=False
            Use a restart strategy

        binary_problem (boolean): default=True
            univariate or multivariate problems

        limited_memory_qning (int): default=20
            Memory parameter for the qning method

        fista_restart (int): default=50
            Restart strategy for fista (useful for computing regularization path)

    """

    def __sklearn_tags__(self):
        tags = super().__sklearn_tags__()
        tags.target_tags.multi_output = True
        tags.estimator_type = "regressor"
        tags.regressor_tags = RegressorTags()
        return tags

    def __init__(self, loss='square', penalty='l2', fit_intercept=True, random_state=0,
                 lambda_1=0, lambda_2=0, lambda_3=0, solver='auto', tol=1e-3,
                 duality_gap_interval=10, max_iter=500,
                 limited_memory_qning=20, fista_restart=50, verbose=True,
                 warm_start=False, n_threads=-1, dual=None, safe=True):
        super().__init__(loss=loss, penalty=penalty,
                         fit_intercept=fit_intercept, random_state=random_state, lambda_1=lambda_1,
                         lambda_2=lambda_2, lambda_3=lambda_3, solver=solver, tol=tol,
                         duality_gap_interval=duality_gap_interval, max_iter=max_iter,
                         limited_memory_qning=limited_memory_qning,
                         fista_restart=fista_restart, verbose=verbose,
                         warm_start=warm_start, n_threads=n_threads, dual=dual, safe=safe)

    def fit(self, X, y, le_parameter=None):
        """
        Fit the parameters.

        Parameters
        ----------
            X (numpy array):
                input n X p numpy matrix; the samples are on the rows

            y (numpy array):
                - vector of size n with real values for regression
                - matrix of size n X k for multivariate regression

        Returns
        -------
            self (ERM):
                Returns the instance of the class
        """
        if self.loss != 'square':
            raise ValueError("square loss should be used")

        if self.safe:
            X, labels, _ = check_input_fit(X, y, self)
        else:
            labels = y

        if labels.squeeze().ndim <= 1:
            self._binary_problem = True
        else:
            self._binary_problem = False

        return super().fit(X, labels, le_parameter)

    def predict(self, X):
        """
        Predict the labels given an input matrix X (same format as fit).

        Parameters
        ----------
            X (numpy array):
                Input matrix for the prediction

        Returns
        -------
            pred (numpy.array):
                Prediction for the X matrix
        """
        check_is_fitted(self)

        if self.safe:
            X = check_input_inference(X, self)

        X = self._validate_data(X, reset=False)

        pred = safe_sparse_dot(X, self.coef_, dense_output=False)

        if self.fit_intercept:
            pred = pred + self.intercept_

        return pred.squeeze()

    def score(self, X, y, sample_weight=None):
        r"""
        Return the coefficient of determination of the prediction.

        The coefficient of determination :math:`R^2` is defined as
        :math:`(1 - \\frac{u}{v})`, where :math:`u` is the residual
        sum of squares ``((y_true - y_pred)** 2).sum()`` and :math:`v`
        is the total sum of squares ``((y_true - y_true.mean()) ** 2).sum()``.
        The best possible score is 1.0 and it can be negative (because the
        model can be arbitrarily worse). A constant model that always predicts
        the expected value of `y`, disregarding the input features, would get
        a :math:`R^2` score of 0.0.

        Parameters
        ----------
            X (numpy array):
                Test samples.
            y (numpy.array):
                True labels for X.
            sample_weight (numpy.array, optional):
                Sample weights. Defaults to None.

        Returns
        -------
            score (float):
                :math:`R^2` of ``self.predict(X)`` wrt. `y`.
        """
        from sklearn.metrics import r2_score

        y_pred = self.predict(X)
        return r2_score(y, y_pred, sample_weight=sample_weight)


class Classifier(ClassifierAbstraction):
    r"""
    The classification class.

    The goal is to minimize the following objective:

    .. math::

        \min_{W,b} \frac{1}{n} \sum_{i=1}^n
        L\left( y_i, W^\top x_i + b\right) + \psi(W)

    where :math:`L` is a classification loss, :math:`\psi` is a regularization
    function (or constraint), :math:`W=[w_1,\ldots,w_k]` is a (p x k) matrix
    that carries the k predictors, where k is the number of classes, and
    :math:`y_i` is a label in :math:`\{1,\ldots,k\}`.
    b is a k-dimensional vector representing an unregularized intercept
    (which is optional).

    In the case of binary classification:
    :math:`w` is a p-dimensional vector representing model parameters,
    and b is an optional unregularized intercept. We expect binary labels in {-1,+1}.

    In a multivariate scenario, if you set multi_class parameter to "multinomial"
    or if multi_class="auto" and loss="logistic".
    The loss will automatically be changed to "multiclass-logistic".
    If you have a multivariate problem and are not in one of the previous configuration,
    a one-vs-all strategy will be used.


    Parameters
    ----------
    loss: string, default='square'
        Loss function to be used. Possible choices are

            - 'square'
                :math:`L(y,z) = \frac{1}{2} ( y-z)^2`
            - 'logistic'
                :math:`L(y,z) = \log(1 + e^{-y z} )`
            - 'multiclass-logistic'
                which is also called multinomial or softmax logistic:
                :math:`L(y, W^\top x + b) = \sum_{j=1}^k
                \log\left(e^{w_j^\top + b_j} - e^{w_y^\top + b_y} \right)`

    penalty (string): default='none'
        Regularization function psi. Possible choices are

        For binary_problem problems:

        - 'none'
            :math:`psi(w) = 0`
        - 'l2'
            :math:`psi(w) = \frac{\lambda_1}{2} ||w||_2^2`
        - 'l1'
            :math:`psi(w) = \lambda_1 ||w||_1`

        For multivariate problems, the previous penalties operate on each
        individual (e.g., class) predictor.

        .. math::
            \psi(W) = \sum_{j=1}^k \psi(w_j).

    fit_intercept (boolean): default='False'
        Learns an unregularized intercept b  (or several intercepts for
        multivariate problems)

    lambda_1 (float): default=0
        First regularization parameter

    lambda_2 (float): default=0
        Second regularization parameter, if needed

    lambda_3 (float): default=0
        Third regularization parameter, if needed

    solver (string): default='auto'
        Optimization solver. Possible choices are

        - 'ista'
        - 'ista-barzilai'
        - 'fista'
        - 'catalyst-ista'
        - 'qning-ista'  (proximal quasi-Newton method)
        - 'auto'

        see the Latex documentation for more details.
        If you are unsure, use 'auto'

    tol (float): default='1e-3'
        Tolerance parameter. For almost all combinations of loss and
        penalty functions, this parameter is based on a duality gap.
        Assuming the (non-negative) objective function is "f" and its
        optimal value is "f^*", the algorithm stops with the guarantee

        :math:`f(x_t) - f^*  <=  tol f(x_t)`

    max_iter (int): default=500
        Maximum number of iteration of the algorithm in terms of passes
        over the data

    duality_gap_interval (int): default=10
        Frequency of duality-gap computation

    verbose (boolean): default=True
        Display information or not

    n_threads (int): default=-1
        Maximum number of cores the method may use (-1 = all cores).
        Note that more cores is not always better.

    random_state (int): default=0
        Random seed

    warm_start (boolean): default=False
        Use a restart strategy

    binary_problem (boolean): default=True
        univariate or multivariate problems

    limited_memory_qning (int): default=20
        Memory parameter for the qning method

    fista_restart (int): default=50
        Restart strategy for fista (useful for computing regularization path)

    multi_class (string): default="auto"
        Determine the comportment of the instance in case of multivariate problem

    """

    def __sklearn_tags__(self):
        tags = super().__sklearn_tags__()
        tags.estimator_type = "classifier"
        tags.classifier_tags = ClassifierTags()
        return tags

    def __init__(self, loss='square', penalty='l2', fit_intercept=True, tol=1e-3, solver="auto",
                 random_state=0, max_iter=500, fista_restart=50, verbose=True,
                 warm_start=False, multi_class="auto",
                 limited_memory_qning=20, lambda_1=0, lambda_2=0, lambda_3=0,
                 duality_gap_interval=5, n_threads=-1, dual=None, safe=True):
        super().__init__(loss=loss, penalty=penalty, fit_intercept=fit_intercept,
                         tol=tol, solver=solver,
                         random_state=random_state, max_iter=max_iter, fista_restart=fista_restart,
                         verbose=verbose, warm_start=warm_start,
                         limited_memory_qning=limited_memory_qning,
                         lambda_1=lambda_1, lambda_2=lambda_2, lambda_3=lambda_3,
                         duality_gap_interval=duality_gap_interval,
                         n_threads=n_threads, multi_class=multi_class, dual=dual, safe=safe)

    def fit(self, X, y, le_parameter=None):
        """
        Fit the parameters.

        Parameters
        ----------
        X (numpy array):
            input n x p numpy matrix; the samples are on the rows

        y (numpy.array):
            Input labels.

            - vector of size n with {-1, +1} labels for binary classification,
              which will be automatically converted if labels in {0,1} are
              provided and {0,1,..., n} for multiclass classification.
        """
        if self.safe:
            X, labels, le = check_input_fit(X, y, self)
        else:
            labels = y
            le = None

        if le_parameter is not None:
            self.le_ = le_parameter
        else:
            self.le_ = le

        labels = np.squeeze(labels)
        unique = np.unique(labels)
        nb_classes = len(unique)

        if self.le_ is not None:
            self.classes_ = self.le_.classes_
        else:
            self.classes_ = unique

        if nb_classes != 2 and (nb_classes != unique.shape[0] or
                                not all(np.unique(labels) == np.arange(nb_classes))):
            logger.info("Class labels should be of the form")
            logger.info(np.arange(nb_classes))
            logger.info("but they are")
            logger.info(unique)
            logger.info(
                "The labels have been converted to respect the expected format.")

        if nb_classes == 2:
            self._binary_problem = True
            if self.le_ is not None:
                neg = labels == self.le_.transform(self.classes_)[0]
            else:
                neg = labels == self.classes_[0]
            labels = labels.astype(int)
            labels[neg] = -1
            labels[np.logical_not(neg)] = 1
        else:
            min_value = min(labels)
            if min_value != 0:
                labels = labels - min_value
            self._binary_problem = False

        super().fit(
            X, labels, le_parameter=self.le_)

        self.coef_ = self.coef_.reshape(self.coef_.shape[0], -1)
        self.coef_ = np.squeeze(self.coef_)
        if self.fit_intercept:
            self.intercept_ = self.intercept_.reshape(1, -1)

        return self

    def predict(self, X):
        """
        Predict the labels given an input matrix X (same format as fit).

        Parameters
        ----------
            X (numpy array):
                Input matrix for the prediction

        Returns
        -------
            pred (numpy.array):
                Prediction for the X matrix
        """
        check_is_fitted(self)

        pred = self.decision_function(X)

        output = None
        if len(self.classes_) == 2:
            if self.le_ is None:
                output = np.sign(pred)
                output[output == -1.0] = self.classes_[0]
                output = output.astype(np.int32)
            else:
                output = np.sign(pred)
                output[output == -1.0] = 0
                output = output.astype(np.int32)
                output = self.le_.inverse_transform(output)
        else:
            if self.le_ is None:
                output = np.argmax(pred, axis=1)
            else:
                output = self.le_.inverse_transform(np.argmax(pred, axis=1))

        return output

    def score(self, X, y):
        """
        Give an accuracy score on test data.

        Parameters
        ----------
            X (numpy array):
                Test samples.
            y (numpy.array):
                True labels for X.
            sample_weight (numpy.array, optional):
                Sample weights. Defaults to None.

        Returns
        -------
            score : float
                Mean accuracy of ``self.predict(X)`` wrt. `y`.
        """
        check_is_fitted(self)

        if self.safe:
            X = check_input_inference(X, self)

        pred = np.squeeze(self.predict(X))
        return np.sum(np.squeeze(y) == pred) / pred.shape[0]

    def decision_function(self, X):
        """
        Predict confidence scores for samples.

        Parameters
        ----------
            X (numpy array):
                The data for which we want scores

        Returns
        -------
            scores (numpy.array):
                Confidence scores per (n_samples, n_classes) combination.
                In the binary case, confidence score for self.classes_[1] where >0 means t
                his class would be predicted.
        """
        check_is_fitted(self)

        if self.safe:
            X = check_input_inference(X, self)

        if self.fit_intercept:
            scores = safe_sparse_dot(
                X, self.coef_, dense_output=False) + self.intercept_
        else:
            scores = safe_sparse_dot(X, self.coef_, dense_output=False)

        output = None
        if len(self.classes_) == 2:
            output = scores.ravel()
        else:
            output = scores.ravel() if scores.shape[1] == 1 else scores

        return output

    def predict_proba(self, X):
        """
        Estimate the probability for each class.

        Parameters
        ----------
            X (numpy array):
                Data matrix for which we want probabilities

        Returns
        -------
            proba (numpy.array):
                Return the probability of the samples for each class.
        """
        check_is_fitted(self)

        if self.safe:
            X = check_input_inference(X, self)

        decision = self.decision_function(X)
        if decision.ndim == 1:
            # Workaround for binary outcomes
            # which requires softmax prediction with only a 1D decision.
            decision = np.c_[-decision, decision]
        return softmax(decision, copy=False)


class LogisticRegression(Classifier):
    """A pre-configured class for logistic regression loss."""

    def __sklearn_tags__(self):
        tags = super().__sklearn_tags__()
        tags.estimator_type = "classifier"
        tags.classifier_tags = ClassifierTags()
        return tags

    def __init__(self, penalty='l2', loss='logistic', fit_intercept=True,
                 verbose=False, lambda_1=0, lambda_2=0, lambda_3=0,
                 solver='auto', tol=1e-3, duality_gap_interval=10,
                 max_iter=500, limited_memory_qning=20,
                 fista_restart=50, warm_start=False, n_threads=-1,
                 random_state=0, multi_class="auto", dual=None, safe=True):
        super().__init__(loss=loss, penalty=penalty, fit_intercept=fit_intercept,
                         solver=solver, tol=tol, random_state=random_state, verbose=verbose,
                         lambda_1=lambda_1, lambda_2=lambda_2, lambda_3=lambda_3,
                         duality_gap_interval=duality_gap_interval, max_iter=max_iter,
                         limited_memory_qning=limited_memory_qning, multi_class=multi_class,
                         fista_restart=fista_restart, warm_start=warm_start,
                         n_threads=n_threads, dual=dual, safe=safe)


def compute_r(estimator_name, aux, X, labels, active_set, fit_intercept):
    """
    Compute R coefficient corresponding to the estimator.

    Parameters
    ----------
        estimator_name (string):
            Name of the estimator class

        aux (ERM):
            Auxiliary estimator

        X (numpy array):
            Features matrix

        labels (numpy.array):
            Labels matrix

        active_set (numpy.array):
            Active set

    Returns
    -------
        R (float):
            _description_
    """
    R = None

    if len(active_set) != 0:
        pred = aux.predict(X[:, active_set])
    if estimator_name == "Lasso":
        if len(active_set) == 0:
            R = labels
        else:
            R = labels.ravel() - pred.ravel()
    elif estimator_name == "L1Logistic":
        if len(active_set) == 0:
            R = -0.5 * labels.ravel()
        else:
            R = -labels.ravel() / (1.0 + np.exp(labels.ravel() * pred.ravel()))
        if fit_intercept:
            pred += aux.intercept_

    return R


def fit_large_feature_number(estimator, aux, X, labels):
    """
    Fitting function when the number of feature is superior to 1000.

    Args
    ----
        estimator (ERM):
            Fitted estimator

        aux (ERM):
            Auxiliary estimator

        X (numpy array):
            Features matrix

        labels (numpy.array):
            Labels matrix
    """
    n, p = X.shape

    scaling = 4.0
    init = min(100, p)

    num_as = math.ceil(math.log10(p / init) / math.log10(scaling))
    active_set = []
    n_active = 0

    estimator.coef_ = np.zeros(p, dtype=X.dtype)
    estimator.restart = True

    estimator_name = type(estimator).__name__

    for ii in range(num_as):
        R = compute_r(estimator_name, aux, X, labels, active_set, estimator.fit_intercept)

        corr = np.abs(X.T @ R) / n

        if n_active > 0:
            corr[active_set] = -10e10
        n_new_as = max(
            min(init * math.ceil(scaling ** ii), p) - n_active, 0)
        new_as = corr.argsort()[-n_new_as:]

        if len(new_as) == 0 or max(corr[new_as]) <= estimator.lambda_1 * (1 + estimator.tol):
            if ii == 0:
                return estimator.fit_fallback(X, labels)
            else:
                break

        if len(active_set) > 0:
            neww = np.zeros(n_active + n_new_as,
                            dtype=X.dtype)
            neww[0:n_active] = aux.coef_
            aux.coef_ = neww
            active_set = np.concatenate((active_set, new_as))
        else:
            active_set = new_as
            aux.coef_ = np.zeros(
                len(active_set), dtype=X.dtype)

        n_active = len(active_set)
        if estimator.verbose:
            logger.info(f"Size of the active set: {n_active}")

        aux.fit(X[:, active_set], labels)

        estimator.coef_[active_set] = aux.coef_
        estimator.n_features_in_ = estimator.coef_.shape[0]
        if estimator.fit_intercept:
            estimator.intercept_ = aux.intercept_

    return estimator


def execute_fit_large_feature_number(instance, auxiliary_solver, X, labels):

    with concurrent.futures.ProcessPoolExecutor() as executor:
        f = executor.submit(fit_large_feature_number, instance, auxiliary_solver, X, labels)
        return f.result()  # will rethrow any exceptions


class Lasso(Regression):
    """
    A pre-configured class for Lasso regression.

    Using active set when the number of features is superior to 1000.
    """

    def __init__(self, lambda_1=0, solver='auto', tol=1e-3,
                 duality_gap_interval=10, max_iter=500, limited_memory_qning=20,
                 fista_restart=50, verbose=True,
                 warm_start=False, n_threads=-1, random_state=0, fit_intercept=True, dual=None, safe=True):
        super().__init__(loss='square', penalty='l1', lambda_1=lambda_1, solver=solver, tol=tol,
                         duality_gap_interval=duality_gap_interval, max_iter=max_iter,
                         limited_memory_qning=limited_memory_qning, fista_restart=fista_restart,
                         verbose=verbose, warm_start=warm_start, n_threads=n_threads,
                         random_state=random_state, fit_intercept=fit_intercept, dual=dual, safe=safe)

    def fit(self, X, y):
        """
        Fit the parameters.

        Parameters
        ----------
            X (numpy array):
                input n X p numpy matrix; the samples are on the rows

            y (numpy array):
                - vector of size n with real values for regression
                - matrix of size n X k for multivariate regression

        Returns
        -------
            self (ERM):
                Returns the instance of the class
        """
        if self.safe:
            X, labels, _ = check_input_fit(X, y, self)
        else:
            labels = y

        _, p = X.shape
        if p <= 1000:
            # no active set
            super().fit(X, labels)
        else:
            aux = Regression(loss='square', penalty='l1',
                             fit_intercept=self.fit_intercept, random_state=self.random_state,
                             lambda_1=self.lambda_1, safe=self.safe,
                             tol=self.tol, duality_gap_interval=self.duality_gap_interval,
                             max_iter=self.max_iter, solver=self.solver, verbose=self.verbose)

            estimator = execute_fit_large_feature_number(self, aux, X, labels)

            self.coef_ = estimator.coef_
            if self.fit_intercept:
                self.intercept_ = estimator.intercept_

        return self

    def fit_fallback(self, X, y):
        """
        Fit the parameters.

        Parameters
        ----------
            X (numpy array):
                input n X p numpy matrix; the samples are on the rows

            y (numpy array):
                - vector of size n with real values for regression
                - matrix of size n X k for multivariate regression

        Returns
        -------
            self (ERM):
                Returns the instance of the class
        """

        if self.safe:
            X, labels, le = check_input_fit(X, y, self)
        else:
            le = None
            labels = y
        self.le_ = le

        super().fit(X, labels, le_parameter=self.le_)

        return self


class L1Logistic(Classifier):
    """
    A pre-configured class for L1 logistic classification.

    Using active set when the number of features is superior to 1000
    """

    def __sklearn_tags__(self):
        tags = super().__sklearn_tags__()
        tags.estimator_type = "classifier"
        tags.classifier_tags = ClassifierTags()
        return tags

    def _more_tags(self):
        return {
            "_xfail_checks": {
                "check_non_transformer_estimators_n_iter": (
                    "We have a different implementation of _n_iter in the multinomial case."
                ),
            }
        }

    def __init__(self, lambda_1=0, solver='auto', tol=1e-3,
                 duality_gap_interval=10, max_iter=500, limited_memory_qning=20,
                 fista_restart=50, verbose=True, warm_start=False, n_threads=-1,
                 random_state=0, fit_intercept=True, multi_class="auto", dual=None, safe=True):
        super().__init__(loss='logistic', penalty='l1', lambda_1=lambda_1, solver=solver, tol=tol,
                         duality_gap_interval=duality_gap_interval, max_iter=max_iter,
                         limited_memory_qning=limited_memory_qning,
                         fista_restart=fista_restart, verbose=verbose,
                         warm_start=warm_start, n_threads=n_threads, random_state=random_state,
                         fit_intercept=fit_intercept, multi_class=multi_class, dual=dual, safe=safe)

    def fit(self, X, y):
        """
        Fit the parameters.

        Parameters
        ----------
        X (numpy array):
            input n x p numpy matrix; the samples are on the rows

        y (numpy.array):
            Input labels.

            - vector of size n with {-1, +1} labels for binary classification,
              which will be automatically converted if labels in {0,1} are
              provided and {0,1,..., n} for multiclass classification.
        """

        if self.multi_class == "multinomial":
            self.loss = "multiclass-logistic"
        if self.safe:
            X, labels, le = check_input_fit(X, y, self)
        else:
            le = None
            labels = y
        self.le_ = le

        _, p = X.shape
        if p <= 1000:
            # no active set
            super().fit(X, labels, le_parameter=self.le_)
        else:
            aux = Classifier(
                loss='logistic', penalty='l1', fit_intercept=self.fit_intercept,
                random_state=self.random_state,
                lambda_1=self.lambda_1, safe=self.safe, tol=self.tol,
                duality_gap_interval=self.duality_gap_interval, max_iter=self.max_iter,
                solver=self.solver, verbose=self.verbose)

            estimator = execute_fit_large_feature_number(self, aux, X, labels)

            self.coef_ = estimator.coef_
            if self.fit_intercept:
                self.intercept_ = estimator.intercept_

        return self

    def fit_fallback(self, X, y):
        """
        Fit the parameters.

        Parameters
        ----------
        X (numpy array):
            input n x p numpy matrix; the samples are on the rows

        y (numpy.array):
            Input labels.

            - vector of size n with {-1, +1} labels for binary classification,
            which will be automatically converted if labels in {0,1} are
            provided and {0,1,..., n} for multiclass classification.
        """

        if self.safe:
            X, labels, le = check_input_fit(X, y, self)
        else:
            le = None
            labels = y
        self.le_ = le

        super().fit(X, labels, le_parameter=self.le_)

        return self
