import unittest
import math
from itur import calculate_geometrical_attenuation, specific_attenuation_due_to_rain

class TestCalculateGeometricalAttenuation(unittest.TestCase):

    ## testing calculate_geometrical_attenuation function

    def test_capture_diameter_greater_than_beam_diameter(self):
        self.assertAlmostEqual(calculate_geometrical_attenuation(3.0, 1.0, 1.0), 0.0)  # Diameter greater than beam diameter

    def test_capture_diameter_equal_to_beam_diameter(self):
        self.assertAlmostEqual(calculate_geometrical_attenuation(2.0, 1.0, 1.0), 0.0)  # Diameter equal to beam diameter

    def test_capture_diameter_less_than_beam_diameter(self):
        result = calculate_geometrical_attenuation(1.0, 1.0, 1.0)
        expected = 10 * math.log10((math.pi /4 * ((1.0*1.0)** 2)) / (math.pi/4 * (1.0 ** 2)))  # Diameter of beam = 2.0 m
        self.assertAlmostEqual(result, expected)

    def test_zero_capture_diameter(self):
        with self.assertRaises(ZeroDivisionError):
            calculate_geometrical_attenuation(0.0, 1.0, 1.0)

    def test_large_distance(self):
        result = calculate_geometrical_attenuation(0.1, 10.0, 10.0)
        expected = 10 * math.log10(((math.pi/4) * ((10.0 * 10.0) ** 2)) / ((math.pi/4) * (0.1 ** 2)))  # Diameter of beam at large distance
        self.assertAlmostEqual(result, expected)

    ## testing specific_attenuation_due_to_rain function
class TestSpecificAttenuationDueToRain(unittest.TestCase):
    def test_valid_inputs(self):
        # Test with valid rain rates and DSD shape parameters
        self.assertAlmostEqual(specific_attenuation_due_to_rain(10, -2), 5.8031, places=4)
        self.assertAlmostEqual(specific_attenuation_due_to_rain(20, -1), 8.2855, places=4)
        self.assertAlmostEqual(specific_attenuation_due_to_rain(30, 0), 11.5365, places=4)
        self.assertAlmostEqual(specific_attenuation_due_to_rain(40, 1), 15.3904, places=4)
        self.assertAlmostEqual(specific_attenuation_due_to_rain(50, 2), 19.7294, places=4)

    def test_zero_rain_rate(self):
        # Test with zero rain rate
        self.assertAlmostEqual(specific_attenuation_due_to_rain(0, 0), 0.0, places=4)
        self.assertAlmostEqual(specific_attenuation_due_to_rain(0, -2), 0.0, places=4)

    def test_invalid_dsd_shape_param(self):
        # Test with invalid DSD shape parameter
        with self.assertRaises(ValueError):
            specific_attenuation_due_to_rain(10, -3)
        with self.assertRaises(ValueError):
            specific_attenuation_due_to_rain(10, 3)

    def test_negative_rain_rate(self):
        # Test with a negative rain rate
        with self.assertRaises(ValueError):
            specific_attenuation_due_to_rain(-5, 0)


if __name__ == '__main__':
    unittest.main()