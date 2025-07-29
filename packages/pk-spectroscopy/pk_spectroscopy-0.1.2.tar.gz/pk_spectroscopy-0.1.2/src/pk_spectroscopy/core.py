from __future__ import annotations

from enum import Enum
import numpy as np
from scipy.optimize import nnls

# Default constants
Kw = 1e-14  # Ion product of water
F = 96485  # Faraday constant
LOG10 = np.log(10)  # Binary algorithm of 10
TOLERANCE = 1e-6  # Default convergence tolerance
PK_START = 0.0  # Start of pK search range
PK_END = 10.0  # End of pK search range
D_PK = 0.05  # Resolution of pK values
USE_INTEGRATION_CONSTANT = True  # Use the integration constant


class TitrationMode(Enum):
    """
    Implementation of the titration mode selection
    """
    VOLUMETRIC = 1
    COULOMETRIC = 2


class pK_Spectroscopy:
    """
    Base pK spectroscopy class
    :param mode: Mode of titration
    :param tolerance: Calculation tolerance
    :param pk_start: Starting point of the pK search
    :param pk_end: Ending point of the pK search
    :param d_pk: pK search resolution
    :param use_integration_constant: Use integration constant
    """
    def __init__(
            self,
            mode: TitrationMode = TitrationMode.VOLUMETRIC,
            tolerance: float = TOLERANCE,
            pk_start: float = PK_START,
            pk_end: float = PK_END,
            d_pk: float = D_PK,
            use_integration_constant: bool = USE_INTEGRATION_CONSTANT,
    ):
        self.mode = mode
        self.tolerance = tolerance
        self.pk_start = pk_start
        self.pk_end = pk_end
        self.d_pk = d_pk
        self.use_integration_constant = use_integration_constant
        self.sample_volume = None
        self.alkaline_concentration = None
        self.current = None
        self.alkaline_volumes = []
        self.times = []
        self.ph_values = []
        self.alpha_values = []
        self.valid_points = 0
        self.acid_peaks = []

    def load_data(
            self,
            sample_volume: float,
            alkaline_concentration_or_current: float,
            volumes: list[float],
            ph_values: list[float],
    ):
        """
        Loads the titration data
        :param sample_volume: Volume of the sample (ml)
        :param alkaline_concentration_or_current: Concentration of the titrant (mol/l) or titration current (A)
        :param volumes: Volumes of the titration points (ml)
        :param ph_values: pH values of the titration points
        :return: None
        """
        # Get sample information
        self.sample_volume = sample_volume
        if self.mode == TitrationMode.VOLUMETRIC:
            self.alkaline_concentration = alkaline_concentration_or_current
        else:
            self.current = alkaline_concentration_or_current

        # Arrange titration data
        combined = list(zip(volumes, ph_values))
        combined.sort(key=lambda x: x[0])
        volumes, ph_values = zip(*combined)
        volumes = list(volumes)
        ph_values = list(ph_values)

        if len(volumes) == len(ph_values):
            self.alkaline_volumes = volumes
            self.ph_values = ph_values
        else:
            raise ValueError('Volumes and ph values must have same length!')

        # Transform volume data to time if needed
        if self.mode == TitrationMode.COULOMETRIC:
            self.times = list(self.alkaline_volumes)
            self.alkaline_volumes = []

        # Check data validity
        for i in range(len(self.alkaline_volumes)):
            h = pow(10, -self.ph_values[i])
            if self.mode == TitrationMode.VOLUMETRIC:
                t = ((h - Kw / h) / self.sample_volume) * (self.alkaline_volumes[i] + self.sample_volume) + \
                    self.alkaline_concentration * self.alkaline_volumes[i] / self.sample_volume
            else:
                t = h - Kw / h + self.current * self.times[i] / F / self.sample_volume
            if t >= 0:
                self.alpha_values.append(t)
                self.valid_points = i + 1
            else:
                raise ValueError('Wrong titration data!')

    def make_calculation(
            self,
            pk_start: float = PK_START,
            pk_end: float = PK_END,
            d_pk: float = D_PK,
            use_integration_constant: bool = USE_INTEGRATION_CONSTANT,
    ):
        """
        Calculates pK spectrum
        :param pk_start: Starting point of the pK search
        :param pk_end: Ending point of the pK search
        :param d_pk: pK search resolution
        :param use_integration_constant: Use integration constant
        :return: Peaks, calculation error
        """

        # Check for the valid points
        if self.valid_points < 7:
            return None, np.nan

        # Calculate constant step
        pk_step = round((self.pk_end - self.pk_start) / self.d_pk) + 1

        # Fill the right part
        if self.use_integration_constant:
            shape_1 = pk_step + 2
        else:
            shape_1 = pk_step
        right = np.zeros((self.valid_points, shape_1))
        for i in range(self.valid_points):
            for j in range(pk_step):
                right[i, j] = self.d_pk / (1 + np.exp(LOG10 * (self.pk_start + self.d_pk * j - self.ph_values[i])))

        # Add items for the constant calculation
        if self.use_integration_constant:
            right[:, -2] = 1
            right[:, -1] = -1

        # Solve equation
        constants, residual = nnls(right, np.array(self.alpha_values))

        # Remove constant from scope
        if self.use_integration_constant:
            constants = constants[:-2]

        # Normalization
        constants *= self.d_pk

        # Truncate border artifacts
        if constants[0] > TOLERANCE > constants[1]:
            constants[0] = 0
        if constants[-1] > TOLERANCE > constants[-2]:
            constants[-1] = 0

        sum_constants = constants.sum()
        max_constant = constants.max(initial=0)
        threshold = max_constant / 100
        constants_relative = constants / sum_constants

        # Peak calculation sequence
        i = 0
        while i < pk_step:
            if constants[i] > threshold:
                self.acid_peaks.append({'point_count': 0, 'concentration': 0, 'first_point': i})
                while i < pk_step and constants[i] > threshold:
                    self.acid_peaks[-1]['point_count'] += 1
                    self.acid_peaks[-1]['concentration'] += constants[i]
                    i += 1
            else:
                i += 1

        # Peaks exact position and height calculation
        if len(self.acid_peaks) > 0:
            for i in range(len(self.acid_peaks)):
                t1 = 0
                t2 = 0
                peak = self.acid_peaks[i]
                for j in range(peak['point_count']):
                    t1 += constants_relative[peak['first_point'] + j] * \
                          (self.pk_start + self.d_pk * (peak['first_point'] + j))
                    t2 += constants_relative[peak['first_point'] + j]
                peak['mean'] = t1 / t2
            for i in range(len(self.acid_peaks)):
                peak = self.acid_peaks[i]
                if peak['point_count'] > 0:
                    t1 = 0
                    t2 = 0
                    for j in range(peak['point_count']):
                        t1 += constants_relative[peak['first_point'] + j] * \
                              (self.pk_start + self.d_pk * (peak['first_point'] + j) - peak['mean']) ** 2
                        t2 += constants_relative[peak['first_point'] + j]
                    peak['interval'] = 1.96 * np.sqrt(t1 / t2) / np.sqrt(peak['point_count'])
                else:
                    peak['interval'] = 0.

        # Calculate error
        error = np.sqrt(residual) / np.sqrt(pk_step - 1)

        return self.acid_peaks, error
