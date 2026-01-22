from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


import warnings
import numpy as np
import math
from astropy import units as u
from scipy.optimize import fsolve
from scipy.special import erf as erf

from itur.utils import get_input_type, prepare_quantity, prepare_output_array, prepare_input_array

class __ITU1814__():
    """Prediction methods required for the design of terrestrial free-space optical links

    Available versions:
    * P.1814-0 (08/07) (Superseded)
    * P.1814-1 (09/25) (Current version)

    """

    # This is an abstract class that contains an instance to a version of the
    # ITU-R P.1814 recommendation.

    def __init__(self, version=1):
        if version == 1:

            self.instance = _ITU1814_1_()
        else:
            raise ValueError(
                f"Version {version} is not implemented for the ITU-R P.1814 model."
            )


    @property
    def __version__(self):
        return self.instance.__version__

    def calculate_link_margin(self, *args, **kwargs):
        return self.instance.calculate_link_margin(*args, **kwargs)

    def calculate_geometrical_attenuation(self, capture_surface_diameter_m, Tx_Rx_distance_km, beam_divergence_mrad):
        return self.instance.calculate_geometrical_attenuation(capture_surface_diameter_m, Tx_Rx_distance_km, beam_divergence_mrad)

    def calculate_specific_atmospheric_attenuation(self, *args, **kwargs):
        return self.instance.calculate_specific_atmospheric_attenuation(*args, **kwargs)

    def calculate_specific_attenuation_due_to_suspended_particles(self, *args, **kwargs):
        return self.instance.calculate_specific_attenuation_due_to_suspended_particles(*args, **kwargs)

    def specific_attenuation_due_to_rain(self, rain_rate, dsd_shape_param):
        return self.instance.specific_attenuation_due_to_rain(rain_rate, dsd_shape_param)

    def path_attentuation_due_to_rain(self, rain_rate, dsd_shape_param, path_length):
        return self.instance.path_attentuation_due_to_rain(rain_rate, dsd_shape_param, path_length)


class _ITU1814_1_:
    def __init__(self):
        self.__version__ = 1
        self.year = 2025
        self.month = 9
        self.link = "https://www.itu.int/rec/R-REC-P.1814-1-202509-I/en"

    @classmethod
    def calculate_link_margin(self,P_e, S_r, A_geo, A_atmo, A_scintillation, A_system):
        """
        Calculate the link margin (Mlink) for an FSO communication system.

        Parameters
        ----------
        P_e : float
            Total power of the emitter (dBm).
        S_r : float
            Sensitivity of the receiver (dBm), which depends on the bandwidth (data rate).
        A_geo : float
            Link geometrical attenuation (dB) due to transmit beam spreading with increasing range.
        A_atmo : float
            Atmospheric attenuation (dB) due to absorption and scattering.
        A_scintillation : float
            Attenuation (dB) due to atmospheric turbulence.
        A_system : float
            System-dependent losses (dB), including misalignment, receiver optical losses, beam wander,
            ambient light, etc.

        Returns
        -------
        M_link : float
            Link margin (dB), the power available above the sensitivity of the receiver.
        """
        # Calculate the link margin using the given formula
        M_link = P_e - S_r - A_geo - A_atmo - A_scintillation - A_system
        return M_link

    @classmethod
    def calculate_geometrical_attenuation(self, capture_surface_diameter_m, Tx_Rx_distance_km, beam_divergence_mrad):
        """
        Calculate the geometrical attenuation (A_geo) for an FSO communication system using a gaussian beam with a set divergence.
        The receiver is a circular aperture with a given diameter.

        Parameters
        ----------
        capture_surface_diameter_m : float
            Receiver capture surface diameter m.
        Tx_Rx_distance_km : float
            Emitter-receiver distance (km).
        theta : float
            Beam divergence (mrad).

        Returns
        -------
        A_geo : float
            Geometrical attenuation (dB). If the capture area is greater than the beam area, A_geo is set to 0.
        """
        if capture_surface_diameter_m<= 0:
            raise ZeroDivisionError("Capture diameter must be greater than zero.")

        #convert sensor diamter to surface area
        capture_surface_m = (math.pi / 4.0) * capture_surface_diameter_m** 2

        # Calculate the surface area of the transmit beam at range d
        s_d = (math.pi / 4.0) * (Tx_Rx_distance_km * beam_divergence_mrad) ** 2

        # If the capture area is greater than the beam area, set A_geo to 0
        if capture_surface_m>= s_d:

            return 0 * u.dB

        # Calculate geometrical attenuation
        A_geo = 10 * math.log10(s_d / capture_surface_m)
        return A_geo * u.dB

    @classmethod
    def calculate_specific_atmospheric_attenuation(self, gamma_clear_air, gamma_excess):
        """
        Calculate the specific atmospheric attenuation (gamma_atmo) for an FSO communication system.

        Parameters
        ----------
        gamma_clear_air : float
            Specific attenuation under clear air conditions due to the atmospheric constituents (dB/km).
        gamma_excess : float
            Specific attenuation due to the occasional presence of aerosol, haze, fog, rain, snow, hail, etc. (dB/km).

        Returns
        -------
        gamma_atmo : float
            Specific atmospheric attenuation (dB/km), also referred to as the extinction coefficient.
        """
        # Calculate the specific atmospheric attenuation
        gamma_atmo = gamma_clear_air + gamma_excess

        return gamma_atmo

    @classmethod
    def calculate_specific_attenuation_due_to_suspended_particles(self, visibility, wavelength):
        """
        #not yet tested
        Calculate the specific attenuation due to suspended particles (gamma_sp) for a given visibility and wavelength.

        Parameters
        ----------
        visibility : float
            Visibility (km) defined according to the 2% threshold.
        wavelength : float
            Wavelength (μm), valid for 0.4 μm ≤ λ ≤ 1.55 μm.

        Returns
        -------
        gamma_sp : float
            Specific attenuation due to suspended particles (dB/km).
        """

        # Check if the wavelength is within the valid range
        if not (0.4 <= wavelength <= 1.55):
            raise ValueError("Wavelength must be between 0.4 μm and 1.55 μm.")

        # Determine the value of q based on visibility
        if visibility > 50:
            q = 1.6
        elif 6 < visibility <= 50:
            q = 1.3
        elif 1 <= visibility <= 6:
            q = 0.16 * visibility + 0.34
        elif 0.5 <= visibility < 1:
            q = visibility - 0.5
        else:  # visibility < 0.5
            q = 0

        # Calculate the specific attenuation using the given formula
        gamma_sp = 17 * visibility * (0.55 / wavelength) ** q

        return gamma_sp

    @classmethod
    def specific_attenuation_due_to_rain(self, rain_rate, dsd_shape_param):
        """
        Calculate the specific attenuation due to rain (γ_rain) in dB/km.

        Parameters
        ----------
        rain_rate : float
            Rain rate (R) in mm/h.
        dsd_shape_param : int
            Drop size distribution (DSD) shape parameter (μ), valid for -2 ≤ μ ≤ 2.

        Returns
        -------
        gamma_rain : float
            Specific attenuation due to rain (γ_rain) in dB/km.

        Raises
        ------
        ValueError
            If the DSD shape parameter is outside the valid range (-2 to 2).
        """

        # Coefficients for different values of the DSD shape parameter (μ)
        coefficients = {
            -2: (2.2838, 0.4050),
            -1: (1.5921, 0.5506),
            0: (1.2924, 0.6436),
            1: (1.1394, 0.7057),
            2: (1.0505, 0.7497),
        }

        # Check if the DSD shape parameter is valid
        if dsd_shape_param not in coefficients:
            raise ValueError("DSD shape parameter (μ) must be an integer between -2 and 2.")
        if rain_rate < 0:
            raise ValueError("Rain rate (R) must be non-negative.")
        # Retrieve the coefficients k and α for the given μ
        k, alpha = coefficients[dsd_shape_param]

        # Calculate the specific attenuation using the power-law relationship
        gamma_rain = k * (rain_rate ** alpha)

        return gamma_rain

    @classmethod
    def path_attentuation_due_to_rain(self, rain_rate, dsd_shape_param, path_length):
        # Calculate the path attenuation due to rain (A_rain) in dB.

        gamma_rain = self.specific_attenuation_due_to_rain(rain_rate, dsd_shape_param)
        gamma_rain_float = getattr(gamma_rain, "value", gamma_rain)
        rain_rate_float = getattr(rain_rate, "value", rain_rate)
        path_length_float = getattr(path_length, "value", path_length)

        F_rain = 1/(1+(path_length_float*(rain_rate_float-6.2))/2623)

        coefficients = {
    -2: (0.010012, 0.025381, -0.001606, 0.250329, -0.035278, 0.008349),
    -1: (0.014551, 0.010932, 0.001532, 0.279336, 0.023974, 0.004421),
     0: (0.015940, -0.001476, 0.008297, 0.117663, 0.029602, 0.002142),
     1: (0.023468, 0.002897, 0.008912, 0.090689, 0.034955, 0.004583),
     2: (-0.000316, 0.062233, -0.007835, 0.192092, -0.081869, 0.033669),
}
# Each tuple: (μ, p0, p1, p2, k0, k1, k2)

        if dsd_shape_param not in coefficients:
            raise ValueError("DSD shape parameter (μ) must be an integer between -2 and 2.")
        if rain_rate < 0:
            raise ValueError("Rain rate (R) must be non-negative.")
        # Retrieve the coefficients k and α for the given μ
        p0, p1, p2, k0, k1, k2 = coefficients[dsd_shape_param]
        if rain_rate_float <= 0:
            return 0 * u.dB  # or another appropriate value
        # Ca
        path_attenuation_rain_star = gamma_rain_float*path_length_float*F_rain

        a_ms = p0+p1*math.log(rain_rate_float)+p2*(math.log(rain_rate_float))**2
        b_ms = k0+k1*math.log(rain_rate_float)+k2*(math.log(rain_rate_float))**2
        G_ms = a_ms*path_length_float**b_ms
        path_attenuation_rain = path_attenuation_rain_star - G_ms
        if path_attenuation_rain <= 0:
            return 0 * u.dB  # or another appropriate value
        return path_attenuation_rain *u.dB

__model = __ITU1814__()

def change_version(new_version):
    """
    Change the version of the ITU-R P.1814 recommendation currently being used.

    This function changes the model used for the ITU-R P.1814 recommendation
    to a different version.

    Parameters
    ----------
    new_version : int
        Number of the version to use.
        Valid values are:
          * 1: Activates recommendation ITU-R P.1814-1 (09/2025) (Current version)
    """

    global __model
    __model = __ITU1814__(new_version)

def get_version():
    """
    Obtain the version of the ITU-R P.1814 recommendation currently being used.

    Returns
    -------
    version: int
        Version currently being used.
    """
    return __model.__version__

def calculate_geometrical_attenuation(capture_surface_diameter_m, Tx_Rx_distance_km, beam_divergence_mrad):
        """
        Calculate the geometrical attenuation (A_geo) for an FSO communication system using a gaussian beam with a set divergence.
        The receiver is a circular aperture with a given diameter.

        Parameters
        ----------
        capture_surface_diameter_m : float
            Receiver capture surface diameter m.
        Tx_Rx_distance_km : float
            Emitter-receiver distance (km).
        theta : float
            Beam divergence (mrad).

        Returns
        -------
        A_geo : float
            Geometrical attenuation (dB). If the capture area is greater than the beam area, A_geo is set to 0.
        """
        capture_surface_diameter_m = prepare_quantity(capture_surface_diameter_m, u.meter, 'capture_surface_diameter_m')
        Tx_Rx_distance_km = prepare_quantity(Tx_Rx_distance_km, u.kilometer, 'Tx_Rx_distance_km')
        beam_divergence_mrad = prepare_quantity(beam_divergence_mrad, u.milliradian, 'beam_divergence_mrad')

        A_geo = __model.calculate_geometrical_attenuation(capture_surface_diameter_m, Tx_Rx_distance_km, beam_divergence_mrad)
        return A_geo


def specific_attenuation_due_to_rain(rain_rate, dsd_shape_param):
        """
        Calculate the specific attenuation due to rain (γ_rain) in dB/km.

        Parameters
        ----------
        rain_rate : float
            Rain rate (R) in mm/h.
        dsd_shape_param : int
            Drop size distribution (DSD) shape parameter (μ), valid for -2 ≤ μ ≤ 2.

        Returns
        -------
        gamma_rain : float
            Specific attenuation due to rain (γ_rain) in dB/km.

        Raises
        ------
        ValueError
            If the DSD shape parameter is outside the valid range (-2 to 2).
        """


        # Coefficients for different values of the DSD shape parameter (μ)
        rain_rate = prepare_quantity(rain_rate, u.mm / u.hour, 'rain_rate')
        dsd_shape_param = int(dsd_shape_param)
        gamma_rain = __model.specific_attenuation_due_to_rain(rain_rate, dsd_shape_param)

        return gamma_rain * u.dB / u.km

def path_attentuation_due_to_rain(rain_rate, dsd_shape_param, path_length):
     # Calculate the path attenuation due to rain (A_rain) in dB.

        rain_rate = prepare_quantity(rain_rate, u.mm / u.hour, 'rain_rate')
        dsd_shape_param = int(dsd_shape_param)
        path_length = path_length * u.km


        path_attenuation_rain = __model.path_attentuation_due_to_rain(rain_rate, dsd_shape_param, path_length)

        return path_attenuation_rain * u.dB
