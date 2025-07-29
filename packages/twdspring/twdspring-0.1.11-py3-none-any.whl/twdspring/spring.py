import logging
from dataclasses import dataclass, field
from typing import Generator, NamedTuple, Self

import numpy as np

log = logging.getLogger(__name__)


class Searcher(NamedTuple):
    """
    A class used to represent searching result
    """
    status: str
    """Search status ('tracking' or 'match')."""
    twd_min: float
    """The minimum time warping distance."""
    t_start: int
    """The start time index (0-based)."""
    t_end: int
    """The end time index (0-based)."""
    t: int
    """The time index of status (0-based)."""


@dataclass(eq=False)
class Spring:
    """
    A class used to represent a Spring object for time series analysis based on Time Warping Distance.
    """

    query_vector: np.ndarray
    """The query vector used for distance calculations."""
    epsilon: float
    """The epsilon value used for thresholding."""
    alpha: float | None = None
    """The smoothing factor for moving average calculations. If value is None aplpha will be equal 2 / (k + 1) where k is the number of past time steps in consideration of moving average. Defaults to None."""  # noqa: E501
    ddof: int = 0
    """The delta degrees of freedom for variance calculations. Defaults to 0."""
    distance_type: str = 'quadratic'
    """The type of distance calculation ('quadratic' or 'absolute'). Defaults to 'quadratic'."""
    use_z_norm: bool = False
    """Flag to indicate if z-score normalization should be used. Defaults to False."""
    query_vector_z_norm: np.ndarray | None = None 
    """The z-score normalized query vector. Will compute z-norm of query vector if None. Defaults to None."""

    D: np.ndarray | None = field(init=False)
    """The distance matrix used for calculations. Defaults to None."""
    S: np.ndarray | None = field(init=False)
    """The state matrix used for calculations. Defaults to None."""
    t: int = field(init=False, default=0)
    """The internal time step counter. Defaults to 0."""
    current_x: float = field(init=False, default=float('nan'))
    """The current normalized/non-normalized input value. Defaults to NaN."""
    d_min: float = field(init=False, default=float('inf'))
    """The minimum time warping distance. Defaults to infinity."""
    t_start: int = field(init=False, default=0)
    """The start time index (0-based). Defaults to 0."""
    t_end: int = field(init=False, default=0)
    """The end time index (0-based). Defaults to 0."""
    status: str | None = field(init=False, default=None)
    """The current status of the Spring object. Defaults to None."""
    d_min_status: float = field(init=False, default=float('inf'))
    """The minimum time warping distance status. Defaults to infinity."""
    t_start_status: int = field(init=False, default=0)
    """The start time index status (0-based). Defaults to 0."""
    t_end_status: int = field(init=False, default=0)
    """The end time index status (0-based). Defaults to 0."""
    mean: float = field(init=False, default=0.0)
    """The moving average of the input values. Defaults to 0.0."""
    variance: float = field(init=False, default=0.0)
    """The moving variance of the input values. Defaults to 0.0."""
    M2: float = field(init=False, default=0.0)
    """The second moment of the input values. Defaults to 0.0."""

    def __post_init__(self):
        if self.query_vector.size == 0:
            raise ValueError("Query vector must not be empty.")
        if self.query_vector.ndim != 1:
            raise ValueError("Query vector must be 1-dimensional.")
        if self.epsilon <= 0:
            raise ValueError("Epsilon must be greater than 0.")
        if self.alpha is not None and (self.alpha <= 0 or self.alpha >= 1):
            raise ValueError("Alpha must be in the range (0, 1).")
        if self.ddof < 0:
            raise ValueError("Delta degrees of freedom must be greater than or equal to 0")
        if self.distance_type not in ['quadratic', 'absolute']:
            raise ValueError("Invalid distance type.")
        if self.query_vector_z_norm is None:
            self.query_vector_z_norm = (self.query_vector - np.mean(self.query_vector)) / np.std(self.query_vector)
        elif self.query_vector_z_norm.size != self.query_vector.size:
            raise ValueError("Query vector z-norm must be 1-dimensional and size equal to query verctor.")

        self.reset()

        self.search_gen = self._search()
        next(self.search_gen)

    def reset(self) -> Self:
        """
        Resets the internal state of the Spring object.
        """
        self.D = np.full((self.query_vector.shape[0]+1, 1), np.inf, dtype=np.float64)
        self.S = np.ones_like(self.D, dtype=np.int64)

        self.t = 0
        self.d_min = float('inf')
        self.t_start, self.t_end = self.t, self.t
        self.mean, self.variance = 0.0, 0.0
        self.M2 = 0.0
        self.status = None
        self.d_min_status = self.d_min
        self.t_start_status = self.t_start
        self.t_end_status = self.t_end
        self.current_x = float('nan')
        return self

    @classmethod
    def from_dict(cls, **kwargs) -> Self:
        """
        Creates a Spring object from a dictionary of parameters.

        Parameters:
            **kwargs: Keyword arguments representing the parameters for the Spring object.

        Returns:
            Spring: An instance of the Spring object.
        """
        internal_status_keys = {'D', 'S', 't', 'current_x', 'd_min', 't_start', 't_end', 'status', 'd_min_status',
                                't_start_status', 't_end_status', 'mean', 'variance', 'M2'}

        internal_status = {key: kwargs.pop(key) for key in internal_status_keys if key in kwargs}
        kls = cls(**kwargs)
        for key, value in internal_status.items():
            if hasattr(kls, key):
                setattr(kls, key, value)
            else:
                raise ValueError(f"Invalid parameter '{key}' for Spring object.")
        return kls

    def __eq__(self, other: Self) -> bool:
        """
        Compares two Spring objects for equality.

        Parameters:
            other (Spring): The other Spring object to compare with.

        Returns:
            bool: True if the objects are equal, False otherwise.
        """
        if not isinstance(other, Spring):
            return NotImplemented

        exclude_keys = {'search_gen'}
        checks = []
        for key in self.__dict__.keys():
            if key in exclude_keys:
                continue

            self_value = getattr(self, key)
            if isinstance(self_value, np.ndarray):
                checks.append(np.array_equal(self_value, getattr(other, key)))
            else:
                checks.append(self_value == getattr(other, key))
        
        return all(checks)

    def distance(self, x: float) -> float:
        """
        Calculates the distance between the input value x and the query vector.

        The distance calculation method depends on the `distance_type` attribute of the Spring object.
        It can be either 'quadratic' or 'absolute'.

        Parameters:
            x (float): The input value for which the distance is calculated.

        Returns:
            float: The calculated distance.

        Raises:
            ValueError: If the `distance_type` is not 'quadratic' or 'absolute'.
        """
        query_vector = self.query_vector_z_norm if self.use_z_norm else self.query_vector

        match self.distance_type:
            case 'quadratic':
                return (x - query_vector) ** 2
            case 'absolute':
                return np.abs(x - query_vector)
            case _:
                raise ValueError("Invalid distance type.")

    def update_tick(self) -> Self:
        """
        Increments the internal time step counter.
        """
        self.t += 1
        return self

    def moving_average(self, x: float):
        """
        Updates the moving average of the input value x.

        Parameters:
            x (float): The input value used to update the moving average.
        """
        # 2 / (n + 1) for n-th element. Because self.update_trick() running before.
        alpha = self.alpha if self.alpha is not None else 2 / self.t

        match self.t:
            case 1:
                self.mean = x
            case _:
                self.mean = (1 - alpha) * self.mean + alpha * x

    def moving_variance(self, x: float) -> float:
        """
        Updates the moving variance based on the input value x.

        Parameters:
            x (float): The input value used to update the variance.

        Returns:
            float: The updated variance.
        """
        delta = x - self.mean
        self.moving_average(x)
        delta2 = x - self.mean
        self.M2 += delta*delta2
        self.variance = self.M2 / (self.t - self.ddof)

    def z_norm(self, x: float) -> Self:
        """
        Normalizes the input value x using z-score normalization if enabled.

        Parameters:
            x (float): The input value to be normalized.

        Returns:
            float: The normalized value or NaN if variance is zero.
        """
        match self.use_z_norm:
            case True:
                self.moving_variance(x)
                self.current_x = float((x - self.mean) / np.sqrt(self.variance) if self.variance != 0 else np.nan)
            case False:
                self.current_x = x
        return self

    def update_state(self) -> Self:
        """
        Updates the state of the Spring object based on the input value x.

        Parameters:
            x (float): The input value used to update the state.

        Returns:
            Spring: The updated Spring object.
        """
        match not np.isnan(self.current_x):
            case np.True_:
                new_column = np.hstack((0, self.distance(self.current_x)))[..., np.newaxis]
            case _:
                new_column = self.D[:, self.D.shape[1] - 1:]

        self.D = np.hstack((self.D, new_column))
        self.S = np.hstack((self.S, np.zeros_like(new_column, dtype=np.int64)))
        self.S[0, -1] = self.t

        if np.isnan(self.current_x):
            return self

        for i in range(1, self.D.shape[0]):
            sub_d = np.copy(self.D[i-1:i+1, -2:])
            sub_d[1,1] = np.inf
            d_best = sub_d.min()
            self.D[i, -1] = self.D[i, -1] + d_best
            match sub_d[0, 1] == d_best, sub_d[1, 0] == d_best, sub_d[0, 0] == d_best:
                case np.True_, *_:
                    self.S[i, -1] = self.S[i-1, -1]
                case _, np.True_, _:
                    self.S[i, -1] = self.S[i, -2]
                case _, _, np.True_:
                    self.S[i, -1] = self.S[i - 1, -2]
        return self

    def _search(self) -> Generator[Searcher, float, None]:
        """
        A generator method that yields a Searcher object and updates the state based on the input value.

        Yields:
            Searcher: An object containing the current status, minimum twd, start time index, end time index, and current time index of 'tracking' or 'match' status (All indexes are 0-based). 

        The method continues to update the state and yields Searcher objects until the generator is closed.
        """  # noqa: E501
        while True:
            x: float = yield Searcher(self.status, float(self.d_min_status), int(self.t_start_status - 1),
                                      int(self.t_end_status + 1), self.t_end_status)
            self.update_tick().z_norm(x).update_state()

            if self.d_min <= self.epsilon:
                if ((self.D[:, -1] >= self.d_min) | (self.S[:, -1] > self.t_end))[1:].all():
                    self.status = 'match'
                    self.d_min_status = self.d_min
                    self.t_start_status = self.t_start
                    self.t_end_status = self.t_end

                    self.d_min = float('inf')
                    self.D[1:, -1] = np.where(self.S[1:, -1] <= self.t_end, np.inf, self.D[1:, -1])
            if self.D[-1, -1] <= self.epsilon and self.D[-1, -1] < self.d_min:
                self.d_min = self.D[-1, -1]
                self.t_start, self.t_end = int(self.S[-1, -1]), self.t

                self.status = 'tracking'
                self.d_min_status = self.d_min
                self.t_start_status = self.t_start
                self.t_end_status = self.t_end

            self.D[0, -1] = np.inf
            self.D[:, -2] = self.D[:, -1]
            self.D = self.D[:, 0:self.D.shape[1] - 1]  # for column vector return
            self.S[:, -2] = self.S[:, -1]
            self.S = self.S[:, 0:self.S.shape[1] - 1]  # for column vector return

    def step(self, x: float) -> Searcher:
        return self.search_gen.send(x)
