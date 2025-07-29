from moapy.enum_pre import enUnitLength, enUnitForce, enUnitStress, enUnitTemperature, enUnitArea, enUnitVolume, enUnitInertia

class UnitConverter:
    """
    A class to convert units between the International System of Units (SI) and the United States Customary Units (US).
    """
    def __init__(self):
        """
        Initializes the unit conversion ratios.
        """
        # si : International System of Units
        # us : United States Customary Units

        # Convert Ratio - Length
        # Base unit is meter and foot
        self.length_si_ratios = {enUnitLength.M: 1, enUnitLength.CM: 1e+2, enUnitLength.MM: 1e+3}
        self.length_us_ratios = {enUnitLength.FT: 1, enUnitLength.IN: 12}

        # Convert Ratio - Area
        # Base unit is square meter and square foot
        self.area_si_ratios = {enUnitLength.M: 1, enUnitLength.CM: 1e+4, enUnitLength.MM: 1e+6}
        self.area_us_ratios = {enUnitLength.FT: 1, enUnitLength.IN: 144}

        # Volume units
        # Base unit is cubic meter and cubic foot
        self.volume_si_ratios = {enUnitLength.M: 1, enUnitLength.CM: 1e+6, enUnitLength.MM: 1e+9}
        self.volume_us_ratios = {enUnitLength.FT: 1, enUnitLength.IN: 1728}

        # Inertia units (Length^4)
        # Base unit is meter^4 and foot^4
        self.inertia_si_ratios = {enUnitLength.M: 1, enUnitLength.CM: 1e+8, enUnitLength.MM: 1e+12}
        self.inertia_us_ratios = {enUnitLength.FT: 1, enUnitLength.IN: 20736}

        # Convert Ratio - Force
        # Base unit is newton and lbf
        self.force_si_ratios = {enUnitForce.N: 1, enUnitForce.kN: 1e-3, enUnitForce.MN: 1e-6}
        self.force_us_ratios = {enUnitForce.lbf: 1, enUnitForce.kip: 1e-3}

        # Convert Ratio - Stress
        # Base unit is pascale and pound per square inch (psi)
        self.stress_si_ratios = {enUnitStress.Pa: 1, enUnitStress.KPa: 1e-3, enUnitStress.MPa: 1e-6}
        self.stress_us_ratios = {enUnitStress.psi: 1, enUnitStress.ksi: 1e-3}

        # Convert Ratio - Strain (Unitless)
        # Base unit is pure number
        self.strain_ratios = {'strain': 1, 'percent': 1e-2, 'permil': 1e-3}

        # Convert Ratio - Mass
        # Base unit is kilogram and pound
        self.mass_si_ratios = {'kg': 1, 'ton': 1e-3}
        self.mass_us_ratios = {'lb': 1}

    def length(
        self,
        value: float,
        from_unit: str,
        to_unit: str
    )-> float:
        """
        Converts length units between SI and US systems.
        
        Parameters:
        - value: The value to convert.
        - from_unit: The unit to convert from.
        - to_unit: The unit to convert to.
        
        Returns:
        - The converted value.
        """
        # https://www.nist.gov/pml/us-surveyfoot/revised-unit-conversion-factors
        
        # SI to SI conversion
        if from_unit in self.length_si_ratios and to_unit in self.length_si_ratios:
            return value * self.length_si_ratios[to_unit] / self.length_si_ratios[from_unit]
        
        # US to US conversion
        elif from_unit in self.length_us_ratios and to_unit in self.length_us_ratios:
            return value * self.length_us_ratios[to_unit] / self.length_us_ratios[from_unit]
        
        # SI to US conversion
        elif from_unit in self.length_si_ratios and to_unit in self.length_us_ratios:
            # First convert to inches and then to the target unit
            value_in_meters = value / self.length_si_ratios[from_unit]
            # 1 foot is 0.3048 meters
            value_in_foots = value_in_meters / 0.3048
            return value_in_foots * self.length_us_ratios[to_unit]
        
        # US to SI conversion
        elif from_unit in self.length_us_ratios and to_unit in self.length_si_ratios:
            # First convert to inches and then to the target unit
            value_in_foots = value / self.length_us_ratios[from_unit]
            # 1 foot is 0.3048 meters
            value_in_meters = value_in_foots * 0.3048
            return value_in_meters * self.length_si_ratios[to_unit]
        
        else:
            raise ValueError("Invalid unit conversion")

    def area(
        self,
        value: float,
        from_unit: str,
        to_unit: str
    )-> float:
        """
        Converts area units between SI and US systems.
        
        Parameters:
        - value: The value to convert.
        - from_unit: The unit to convert from.
        - to_unit: The unit to convert to.
        
        Returns:
        - The converted value.
        """
        # SI to SI conversion
        if from_unit in self.area_si_ratios and to_unit in self.area_si_ratios:
            return value * self.area_si_ratios[to_unit] / self.area_si_ratios[from_unit]
        
        # US to US conversion
        elif from_unit in self.area_us_ratios and to_unit in self.area_us_ratios:
            return value * self.area_us_ratios[to_unit] / self.area_us_ratios[from_unit]
        
        # SI to US conversion
        elif from_unit in self.area_si_ratios and to_unit in self.area_us_ratios:
            # First convert to inches and then to the target unit
            value_in_meters = value / self.area_si_ratios[from_unit]
            # 1 foot is 0.3048 meters
            value_in_foots = value_in_meters / (0.3048**2)
            return value_in_foots * self.area_us_ratios[to_unit]
        
        # US to SI conversion
        elif from_unit in self.area_us_ratios and to_unit in self.area_si_ratios:
            # First convert to inches and then to the target unit
            value_in_foots = value / self.area_us_ratios[from_unit]
            # 1 foot is 0.3048 meters
            value_in_meters = value_in_foots * (0.3048**2)
            return value_in_meters * self.area_si_ratios[to_unit]
        
        else:
            raise ValueError("Invalid unit conversion")

    def volume(
        self,
        value: float,
        from_unit: str,
        to_unit: str
    )-> float:
        """
        Converts volume units between SI and US systems.
        
        Parameters:
        - value: The value to convert.
        - from_unit: The unit to convert from.
        - to_unit: The unit to convert to.
        
        Returns:
        - The converted value.
        """
        # SI to SI conversion
        if from_unit in self.volume_si_ratios and to_unit in self.volume_si_ratios:
            return value * self.volume_si_ratios[to_unit] / self.volume_si_ratios[from_unit]
        
        # US to US conversion
        elif from_unit in self.volume_us_ratios and to_unit in self.volume_us_ratios:
            return value * self.volume_us_ratios[to_unit] / self.volume_us_ratios[from_unit]
        
        # SI to US conversion
        elif from_unit in self.volume_si_ratios and to_unit in self.volume_us_ratios:
            # First convert to inches and then to the target unit
            value_in_meters = value / self.volume_si_ratios[from_unit]
            # 1 foot is 0.3048 meters
            value_in_foots = value_in_meters / (0.3048**3)
            return value_in_foots * self.volume_us_ratios[to_unit]
        
        # US to SI conversion
        elif from_unit in self.volume_us_ratios and to_unit in self.volume_si_ratios:
            # First convert to inches and then to the target unit
            value_in_foots = value / self.volume_us_ratios[from_unit]
            # 1 foot is 0.3048 meters
            value_in_meters = value_in_foots * (0.3048**3)
            return value_in_meters * self.volume_si_ratios[to_unit]
        
        else:
            raise ValueError("Invalid unit conversion")

    def inertia(
        self,
        value: float,
        from_unit: str,
        to_unit: str
    )-> float:
        """
        Converts inertia units between SI and US systems.
        
        Parameters:
        - value: The value to convert.
        - from_unit: The unit to convert from.
        - to_unit: The unit to convert to.
        
        Returns:
        - The converted value.
        """
        # SI to SI conversion
        if from_unit in self.inertia_si_ratios and to_unit in self.inertia_si_ratios:
            return value * self.inertia_si_ratios[to_unit] / self.inertia_si_ratios[from_unit]
        
        # US to US conversion
        elif from_unit in self.inertia_us_ratios and to_unit in self.inertia_us_ratios:
            return value * self.inertia_us_ratios[to_unit] / self.inertia_us_ratios[from_unit]
        
        # SI to US conversion
        elif from_unit in self.inertia_si_ratios and to_unit in self.inertia_us_ratios:
            # First convert to inches and then to the target unit
            value_in_meters = value / self.inertia_si_ratios[from_unit]
            # 1 foot is 0.3048 meters
            value_in_foots = value_in_meters / (0.3048**4)
            return value_in_foots * self.inertia_us_ratios[to_unit]
        
        # US to SI conversion
        elif from_unit in self.inertia_us_ratios and to_unit in self.inertia_si_ratios:
            # First convert to inches and then to the target unit
            value_in_foots = value / self.inertia_us_ratios[from_unit]
            # 1 foot is 0.3048 meters
            value_in_meters = value_in_foots * (0.3048**4)
            return value_in_meters * self.inertia_si_ratios[to_unit]
        
        else:
            raise ValueError("Invalid unit conversion")

    def length_exponential(
        self,
        value: float,
        exponent: int,
        from_unit: str,
        to_unit: str
    )-> float:
        """
        Converts length units between SI and US systems with exponents.
        
        Parameters:
        - value: The value to convert.
        - exponent: The exponent to apply.
        - from_unit: The unit to convert from.
        - to_unit: The unit to convert to.
        
        Returns:
        - The converted value.
        """
        # SI to SI conversion
        if from_unit in self.length_si_ratios and to_unit in self.length_si_ratios:
            return value * (self.length_si_ratios[to_unit] / self.length_si_ratios[from_unit])**exponent
        
        # US to US conversion
        elif from_unit in self.length_us_ratios and to_unit in self.length_us_ratios:
            return value * (self.length_us_ratios[to_unit] / self.length_us_ratios[from_unit])**exponent
        
        # SI to US conversion
        elif from_unit in self.length_si_ratios and to_unit in self.length_us_ratios:
            # First convert to inches and then to the target unit
            value_in_meters = value / (self.length_si_ratios[from_unit]**exponent)
            # 1 foot is 0.3048 meters
            value_in_foots = value_in_meters / (0.3048**exponent)
            return value_in_foots * (self.length_us_ratios[to_unit]**exponent)
        
        # US to SI conversion
        elif from_unit in self.length_us_ratios and to_unit in self.length_si_ratios:
            # First convert to inches and then to the target unit
            value_in_foots = value / (self.length_us_ratios[from_unit]**exponent)
            # 1 foot is 0.3048 meters
            value_in_meters = value_in_foots * (0.3048**exponent)
            return value_in_meters * (self.length_si_ratios[to_unit]**exponent)
        
        else:
            raise ValueError("Invalid unit conversion")
    
    def temperature(
        self,
        value: float,
        from_unit: str,
        to_unit: str
    )-> float:
        """
        Converts temperature units between Kelvin, Celsius, and Fahrenheit.
        
        Parameters:
        - value: The value to convert.
        - from_unit: The unit to convert from.
        - to_unit: The unit to convert to.
        
        Returns:
        - The converted value.
        """
        
        if from_unit == 'K' and to_unit == 'C':
            return value - 273.15
        elif from_unit == 'K' and to_unit == 'F':
            return (value - 273.15) * 9/5 + 32
        elif from_unit == 'C' and to_unit == 'K':
            return value + 273.15
        elif from_unit == 'C' and to_unit == 'F':
            return value * 9/5 + 32
        elif from_unit == 'F' and to_unit == 'K':
            return (value - 32) * 5/9 + 273.15
        elif from_unit == 'F' and to_unit == 'C':
            return (value - 32) * 5/9
        else:
            raise ValueError("Invalid unit conversion")
    
    def force(
        self,
        value: float,
        from_unit: str,
        to_unit: str
    )-> float:
        """
        Converts force units between SI and US systems.
        
        Parameters:
        - value: The value to convert.
        - from_unit: The unit to convert from.
        - to_unit: The unit to convert to.
        
        Returns:
        - The converted value.
        """
        # https://en.wikipedia.org/wiki/Standard_gravity
        # https://en.wikipedia.org/wiki/International_yard_and_pound
        # https://en.wikipedia.org/wiki/Pound_(force)
        # Standard Acceleration due to Gravity; ISO 80000 =  9.80665m/s2
        # 1 lb = 0.453 592 37 kg
        # 1 lbf = 1 lb X 0.453 592 37 kg X 9.80665 m/s2 = 4.448 221 615 260 5 N
        
        # SI to SI conversion
        if from_unit in self.force_si_ratios and to_unit in self.force_si_ratios:
            return value * self.force_si_ratios[to_unit] / self.force_si_ratios[from_unit]
        
        # US to US conversion
        elif from_unit in self.force_us_ratios and to_unit in self.force_us_ratios:
            return value * self.force_us_ratios[to_unit] / self.force_us_ratios[from_unit]
        
        # SI to US conversion
        elif from_unit in self.force_si_ratios and to_unit in self.force_us_ratios:
            # First convert to newtons and then to the target unit
            value_in_newtons = value / self.force_si_ratios[from_unit]
            # 1 lbf is 4.4482216152605 newtons
            value_in_lbf = value_in_newtons / 4.4482216152605
            return value_in_lbf * self.force_us_ratios[to_unit]
        
        # Imperial to Metric conversion
        elif from_unit in self.force_us_ratios and to_unit in self.force_si_ratios:
            # First convert to lbf and then to the target unit
            value_in_lbf = value / self.force_us_ratios[from_unit]
            # 1 lbf is 4.4482216152605 newtons
            value_in_newtons = value_in_lbf * 4.4482216152605
            return value_in_newtons * self.force_si_ratios[to_unit]
        
        else:
            raise ValueError("Invalid unit conversion")

    def stress(
        self,
        value: float,
        from_unit: str,
        to_unit: str
    )-> float:
        """
        Converts stress units between SI and US systems.
        
        Parameters:
        - value: The value to convert.
        - from_unit: The unit to convert from.
        - to_unit: The unit to convert to.
        
        Returns:
        - The converted value.
        """
        # 1 lbf = 1 lb X 0.453 592 37 kg X 9.80665 m/s2 = 4.448 221 615 260 5 N
        # 1 in = 0.0254 m , 1 in2 = 0.0254^2 m2
        # 1 psi = 1 lbf/in2 = 4.448 221 615 260 5 N / 0.0254^2 m2 = 6894.75729316836 Pa
        
        # SI to SI conversion
        if from_unit in self.stress_si_ratios and to_unit in self.stress_si_ratios:
            return value * self.stress_si_ratios[to_unit] / self.stress_si_ratios[from_unit]
        
        # US to US conversion
        elif from_unit in self.stress_us_ratios and to_unit in self.stress_us_ratios:
            return value * self.stress_us_ratios[to_unit] / self.stress_us_ratios[from_unit]
        
        # SI to US conversion
        elif from_unit in self.stress_si_ratios and to_unit in self.stress_us_ratios:
            # First convert to pascales and then to the target unit
            value_in_pascales = value / self.stress_si_ratios[from_unit]
            # 1 psi is 6894.75729316836 pascales
            value_in_psi = value_in_pascales / 6894.75729316836
            return value_in_psi * self.stress_us_ratios[to_unit]
        
        # US to SI conversion
        elif from_unit in self.stress_us_ratios and to_unit in self.stress_si_ratios:
            # First convert to psi and then to the target unit
            value_in_psi = value / self.stress_us_ratios[from_unit]
            # 1 psi is 6894.75729316836 pascales
            value_in_pascales = value_in_psi * 6894.75729316836
            return value_in_pascales * self.stress_si_ratios[to_unit]
        
        else:
            raise ValueError("Invalid unit conversion")

    def strain(
        self,
        value: float,
        from_unit: str,
        to_unit: str
    )-> float:
        """
        Converts strain units between unitless, percent, and permil.
        
        Parameters:
        - value: The value to convert.
        - from_unit: The unit to convert from.
        - to_unit: The unit to convert to.
        
        Returns:
        - The converted value.
        """
        # Conversion
        if from_unit in self.strain_ratios and to_unit in self.strain_ratios:
            return value * self.strain_ratios[from_unit] / self.strain_ratios[to_unit]
        else:
            raise ValueError("Invalid unit conversion")
    
    def mass(
        self,
        value: float,
        from_unit: str,
        to_unit: str
    )-> float:
        """
        Converts mass units between SI and US systems.
        
        Parameters:
        - value: The value to convert.
        - from_unit: The unit to convert from.
        - to_unit: The unit to convert to.
        
        Returns:
        - The converted value.
        """
        # https://en.wikipedia.org/wiki/Pound_(mass)
        # 1 lb = 0.453 592 37 kg
        
        # SI to SI conversion
        if from_unit in self.mass_si_ratios and to_unit in self.mass_si_ratios:
            return value * self.mass_si_ratios[to_unit] / self.mass_si_ratios[from_unit]
        
        # US to US conversion
        elif from_unit in self.mass_us_ratios and to_unit in self.mass_us_ratios:
            return value * self.mass_us_ratios[to_unit] / self.mass_us_ratios[from_unit]
        
        # SI to US conversion
        elif from_unit in self.mass_si_ratios and to_unit in self.mass_us_ratios:
            # First convert to inches and then to the target unit
            value_in_kilograms = value / self.mass_si_ratios[from_unit]
            # 1 lb is 0.45359237 kg
            value_in_pounds = value_in_kilograms / 0.45359237
            return value_in_pounds * self.mass_us_ratios[to_unit]
        
        # US to SI conversion
        elif from_unit in self.mass_us_ratios and to_unit in self.mass_si_ratios:
            # First convert to inches and then to the target unit
            value_in_pounds = value / self.mass_us_ratios[from_unit]
            # 1 lb is 0.45359237 kg
            value_in_kilograms = value_in_pounds * 0.45359237
            return value_in_kilograms * self.mass_si_ratios[to_unit]
        
        else:
            raise ValueError("Invalid unit conversion")
    
    def density(
        self,
        value: float,
        from_mass_units: str,
        from_volumn_units: str,
        to_mass_units: str,
        to_volumn_units: str,
    )-> float:
            """
            Converts density units between SI and US systems.
            
            Parameters:
            - value: The value to convert.
            - from_volumn_units: The volumn unit to convert from.
            - from_mass_units: The mass unit to convert from.
            - to_volumn_units: The volumn unit to convert to.
            - to_mass_units: The mass unit to convert to.
            
            Returns:
            - The converted value.
            """
            
            # Convert the value to the base unit
            value_in_kilograms = self.mass(value, from_mass_units, 'kg')
            value_in_meters = self.volume(value, from_volumn_units, enUnitLength.M)
            
            # Convert the value to the target unit
            value_in_target_mass_units = self.mass(value_in_kilograms, 'kg', to_mass_units)
            value_in_target_volumn_units = self.volume(value_in_meters, enUnitLength.M, to_volumn_units)
            
            # Calculate the density
            return value_in_target_mass_units / value_in_target_volumn_units
        
    def moment(
        self,
        value: float,
        from_force_units: str,
        from_length_units: str,
        to_force_units: str,
        to_length_units: str
    )-> float:
        """
        Converts moment units between SI and US systems.
        
        Parameters:
        - value: The value to convert.
        - from_force_units: The force unit to convert from.
        - from_length_units: The length unit to convert from.
        - to_force_units: The force unit to convert to.
        - to_length_units: The length unit to convert to.
        
        Returns:
        - The converted value.
        """
        # Convert the value to the base unit
        value_in_newtons = self.force(value, from_force_units, enUnitForce.N)
        value_in_meters = self.length(value, from_length_units, enUnitLength.M)
        
        # Convert the value to the target unit
        value_in_target_force_units = self.force(value_in_newtons, enUnitForce.N, to_force_units)
        value_in_target_length_units = self.length(value_in_meters, enUnitLength.M, to_length_units)
        
        # Calculate the moment
        return value_in_target_force_units * value_in_target_length_units
    
import unittest

class TestUnitConverter(unittest.TestCase):
    def setUp(self):
        self.converter = UnitConverter()

    def test_length_conversion(self):
        # SI unit conversions
        self.assertAlmostEqual(self.converter.length(1, enUnitLength.M, enUnitLength.MM), 1000, places=5)
        self.assertAlmostEqual(self.converter.length(1, enUnitLength.M, enUnitLength.CM), 100, places=5)
        self.assertAlmostEqual(self.converter.length(1000, enUnitLength.MM, enUnitLength.M), 1, places=5)
        self.assertAlmostEqual(self.converter.length(100, enUnitLength.CM, enUnitLength.M), 1, places=5)
        self.assertAlmostEqual(self.converter.length(1000, enUnitLength.MM, enUnitLength.CM), 100, places=5)
        self.assertAlmostEqual(self.converter.length(100, enUnitLength.CM, enUnitLength.MM), 1000, places=5)

        # US Customary unit conversions
        self.assertAlmostEqual(self.converter.length(1, enUnitLength.FT, enUnitLength.IN), 12, places=5)
        self.assertAlmostEqual(self.converter.length(12, enUnitLength.IN, enUnitLength.FT), 1, places=5)

        # SI to US conversions
        self.assertAlmostEqual(self.converter.length(1, enUnitLength.M, enUnitLength.FT), 3.28084, places=5)
        self.assertAlmostEqual(self.converter.length(1, enUnitLength.M, enUnitLength.IN), 39.37008, places=5)
        self.assertAlmostEqual(self.converter.length(100, enUnitLength.CM, enUnitLength.FT), 3.28084, places=5)
        self.assertAlmostEqual(self.converter.length(1000, enUnitLength.MM, enUnitLength.FT), 3.28084, places=5)
        self.assertAlmostEqual(self.converter.length(100, enUnitLength.CM, enUnitLength.IN), 39.37008, places=5)
        self.assertAlmostEqual(self.converter.length(1000, enUnitLength.MM, enUnitLength.IN), 39.37008, places=5)

        # US to SI conversions
        self.assertAlmostEqual(self.converter.length(1, enUnitLength.FT, enUnitLength.M), 0.3048, places=5)
        self.assertAlmostEqual(self.converter.length(1, enUnitLength.FT, enUnitLength.CM), 30.48, places=5)
        self.assertAlmostEqual(self.converter.length(1, enUnitLength.FT, enUnitLength.MM), 304.8, places=5)
        self.assertAlmostEqual(self.converter.length(1, enUnitLength.IN, enUnitLength.M), 0.0254, places=5)
        self.assertAlmostEqual(self.converter.length(1, enUnitLength.IN, enUnitLength.CM), 2.54, places=5)
        self.assertAlmostEqual(self.converter.length(1, enUnitLength.IN, enUnitLength.MM), 25.4, places=5)

    def test_area_conversion(self):
        # SI unit conversions (metric)
        self.assertAlmostEqual(self.converter.area(1, enUnitLength.M, enUnitLength.MM), 1e6, places=0)
        self.assertAlmostEqual(self.converter.area(1, enUnitLength.M, enUnitLength.CM), 1e4, places=0)
        self.assertAlmostEqual(self.converter.area(1e6, enUnitLength.MM, enUnitLength.M), 1, places=5)
        self.assertAlmostEqual(self.converter.area(1e4, enUnitLength.CM, enUnitLength.M), 1, places=5)
        self.assertAlmostEqual(self.converter.area(1e6, enUnitLength.MM, enUnitLength.CM), 1e4, places=0)
        self.assertAlmostEqual(self.converter.area(1e4, enUnitLength.CM, enUnitLength.MM), 1e6, places=0)

        # US Customary unit conversions
        self.assertAlmostEqual(self.converter.area(1, enUnitLength.FT, enUnitLength.IN), 144, places=0)
        self.assertAlmostEqual(self.converter.area(144, enUnitLength.IN, enUnitLength.FT), 1, places=5)

        # SI to US conversions
        self.assertAlmostEqual(self.converter.area(1, enUnitLength.M, enUnitLength.FT), 10.7639, places=4)
        self.assertAlmostEqual(self.converter.area(1, enUnitLength.M, enUnitLength.IN), 1550.0031, places=4)
        self.assertAlmostEqual(self.converter.area(10000, enUnitLength.CM, enUnitLength.FT), 10.7639, places=4)
        self.assertAlmostEqual(self.converter.area(1000000, enUnitLength.MM, enUnitLength.FT), 10.7639, places=4)
        self.assertAlmostEqual(self.converter.area(10000, enUnitLength.CM, enUnitLength.IN), 1550.0031, places=4)
        self.assertAlmostEqual(self.converter.area(1000000, enUnitLength.MM, enUnitLength.IN), 1550.0031, places=4)

        # US to SI conversions
        self.assertAlmostEqual(self.converter.area(1, enUnitLength.FT, enUnitLength.M), 0.092903, places=6)
        self.assertAlmostEqual(self.converter.area(1, enUnitLength.FT, enUnitLength.CM), 929.0304, places=4)
        self.assertAlmostEqual(self.converter.area(1, enUnitLength.FT, enUnitLength.MM), 92903.04, places=2)
        self.assertAlmostEqual(self.converter.area(1, enUnitLength.IN, enUnitLength.M), 0.00064516, places=8)
        self.assertAlmostEqual(self.converter.area(1, enUnitLength.IN, enUnitLength.CM), 6.4516, places=4)
        self.assertAlmostEqual(self.converter.area(1, enUnitLength.IN, enUnitLength.MM), 645.16, places=2)

    def test_volume_conversion(self):
        # Metric unit conversions (SI)
        self.assertAlmostEqual(self.converter.volume(1, enUnitLength.M, enUnitLength.CM), 1e6, places=0)
        self.assertAlmostEqual(self.converter.volume(1, enUnitLength.M, enUnitLength.MM), 1e9, places=0)
        self.assertAlmostEqual(self.converter.volume(1e6, enUnitLength.CM, enUnitLength.M), 1, places=5)
        self.assertAlmostEqual(self.converter.volume(1e9, enUnitLength.MM, enUnitLength.M), 1, places=5)
        self.assertAlmostEqual(self.converter.volume(1e6, enUnitLength.CM, enUnitLength.MM), 1e9, places=0)
        self.assertAlmostEqual(self.converter.volume(1e9, enUnitLength.MM, enUnitLength.CM), 1e6, places=0)

        # US Customary unit conversions
        self.assertAlmostEqual(self.converter.volume(1, enUnitLength.FT, enUnitLength.IN), 1728, places=0)
        self.assertAlmostEqual(self.converter.volume(1728, enUnitLength.IN, enUnitLength.FT), 1, places=5)

        # SI to US conversions
        self.assertAlmostEqual(self.converter.volume(1, enUnitLength.M, enUnitLength.FT), 35.3147, places=4)
        self.assertAlmostEqual(self.converter.volume(1, enUnitLength.M, enUnitLength.IN), 61023.7441, places=4)
        self.assertAlmostEqual(self.converter.volume(1e6, enUnitLength.CM, enUnitLength.FT), 35.3147, places=4)
        self.assertAlmostEqual(self.converter.volume(1e9, enUnitLength.MM, enUnitLength.FT), 35.3147, places=4)
        self.assertAlmostEqual(self.converter.volume(1e6, enUnitLength.CM, enUnitLength.IN), 61023.7441, places=4)
        self.assertAlmostEqual(self.converter.volume(1e9, enUnitLength.MM, enUnitLength.IN), 61023.7441, places=4)

        # US to SI conversions
        self.assertAlmostEqual(self.converter.volume(1, enUnitLength.FT, enUnitLength.M), 0.0283168, places=7)
        self.assertAlmostEqual(self.converter.volume(1, enUnitLength.FT, enUnitLength.CM), 28316.8466, places=4)
        self.assertAlmostEqual(self.converter.volume(1, enUnitLength.FT, enUnitLength.MM), 28316846.6, places=1)
        self.assertAlmostEqual(self.converter.volume(1, enUnitLength.IN, enUnitLength.M), 0.0000163871, places=10)
        self.assertAlmostEqual(self.converter.volume(1, enUnitLength.IN, enUnitLength.CM), 16.3871, places=4)
        self.assertAlmostEqual(self.converter.volume(1, enUnitLength.IN, enUnitLength.MM), 16387.1, places=1)

    def test_length_exponential_conversion(self):
        exponent = 4

        # SI to SI conversions
        self.assertAlmostEqual(self.converter.length_exponential(1, exponent, enUnitLength.M, enUnitLength.CM), 100**exponent, places=8)
        self.assertAlmostEqual(self.converter.length_exponential(1, exponent, enUnitLength.M, enUnitLength.MM), 1000**exponent, places=8)
        self.assertAlmostEqual(self.converter.length_exponential(1, exponent, enUnitLength.CM, enUnitLength.M), (1/100)**exponent, places=8)
        self.assertAlmostEqual(self.converter.length_exponential(1, exponent, enUnitLength.CM, enUnitLength.MM), 10**exponent, places=8)
        self.assertAlmostEqual(self.converter.length_exponential(1, exponent, enUnitLength.MM, enUnitLength.M), (1/1000)**exponent, places=8)
        self.assertAlmostEqual(self.converter.length_exponential(1, exponent, enUnitLength.MM, enUnitLength.CM), (1/10)**exponent, places=8)

        # US to US conversions
        self.assertAlmostEqual(self.converter.length_exponential(1, exponent, enUnitLength.FT, enUnitLength.IN), 12**exponent, places=8)
        self.assertAlmostEqual(self.converter.length_exponential(1, exponent, enUnitLength.IN, enUnitLength.FT), (1/12)**exponent, places=8)

        # SI to US conversions
        self.assertAlmostEqual(self.converter.length_exponential(1, exponent, enUnitLength.M, enUnitLength.FT), (1 / 0.3048)**exponent, places=8)
        self.assertAlmostEqual(self.converter.length_exponential(1, exponent, enUnitLength.M, enUnitLength.IN), (1 / (0.3048 / 12))**exponent, places=8)
        self.assertAlmostEqual(self.converter.length_exponential(1, exponent, enUnitLength.CM, enUnitLength.FT), (0.01 / 0.3048)**exponent, places=8)
        self.assertAlmostEqual(self.converter.length_exponential(1, exponent, enUnitLength.CM, enUnitLength.IN), (0.01 / (0.3048 / 12))**exponent, places=8)
        self.assertAlmostEqual(self.converter.length_exponential(1, exponent, enUnitLength.MM, enUnitLength.FT), (0.001 / 0.3048)**exponent, places=8)
        self.assertAlmostEqual(self.converter.length_exponential(1, exponent, enUnitLength.MM, enUnitLength.IN), (0.001 / (0.3048 / 12))**exponent, places=8)

        # US to SI conversions
        self.assertAlmostEqual(self.converter.length_exponential(1, exponent, enUnitLength.FT, enUnitLength.M), 0.3048**exponent, places=8)
        self.assertAlmostEqual(self.converter.length_exponential(1, exponent, enUnitLength.FT, enUnitLength.CM), (0.3048 * 100)**exponent, places=8)
        self.assertAlmostEqual(self.converter.length_exponential(1, exponent, enUnitLength.FT, enUnitLength.MM), (0.3048 * 1000)**exponent, places=8)
        self.assertAlmostEqual(self.converter.length_exponential(1, exponent, enUnitLength.IN, enUnitLength.M), (0.0254)**exponent, places=8)
        self.assertAlmostEqual(self.converter.length_exponential(1, exponent, enUnitLength.IN, enUnitLength.CM), (0.0254 * 100)**exponent, places=8)
        self.assertAlmostEqual(self.converter.length_exponential(1, exponent, enUnitLength.IN, enUnitLength.MM), (0.0254 * 1000)**exponent, places=8)

    def test_force_conversion(self):
        # SI to SI conversions
        self.assertAlmostEqual(self.converter.force(1, enUnitForce.N, enUnitForce.kN), 0.001, places=6)
        self.assertAlmostEqual(self.converter.force(1, enUnitForce.N, enUnitForce.MN), 1e-6, places=9)
        self.assertAlmostEqual(self.converter.force(1, enUnitForce.kN, enUnitForce.N), 1000, places=0)
        self.assertAlmostEqual(self.converter.force(1, enUnitForce.MN, enUnitForce.N), 1e6, places=0)
        self.assertAlmostEqual(self.converter.force(1, enUnitForce.kN, enUnitForce.MN), 0.001, places=6)
        self.assertAlmostEqual(self.converter.force(1, enUnitForce.MN, enUnitForce.kN), 1000, places=0)

        # US to US conversions
        self.assertAlmostEqual(self.converter.force(1, enUnitForce.lbf, enUnitForce.kip), 0.001, places=6)
        self.assertAlmostEqual(self.converter.force(1, enUnitForce.kip, enUnitForce.lbf), 1000, places=0)

        # SI to US conversions
        self.assertAlmostEqual(self.converter.force(1, enUnitForce.N, enUnitForce.lbf), 0.224809, places=6)
        self.assertAlmostEqual(self.converter.force(1, enUnitForce.kN, enUnitForce.lbf), 224.809, places=3)
        self.assertAlmostEqual(self.converter.force(1, enUnitForce.MN, enUnitForce.lbf), 224809, places=0)
        self.assertAlmostEqual(self.converter.force(1, enUnitForce.N, enUnitForce.kip), 0.000224809, places=9)
        self.assertAlmostEqual(self.converter.force(1, enUnitForce.kN, enUnitForce.kip), 0.224809, places=6)
        self.assertAlmostEqual(self.converter.force(1, enUnitForce.MN, enUnitForce.kip), 224.809, places=3)

        # US to SI conversions
        self.assertAlmostEqual(self.converter.force(1, enUnitForce.lbf, enUnitForce.N), 4.44822, places=5)
        self.assertAlmostEqual(self.converter.force(1, enUnitForce.lbf, enUnitForce.kN), 0.00444822, places=8)
        self.assertAlmostEqual(self.converter.force(1, enUnitForce.lbf, enUnitForce.MN), 4.44822e-6, places=5)
        self.assertAlmostEqual(self.converter.force(1, enUnitForce.kip, enUnitForce.N), 4448.22, places=2)
        self.assertAlmostEqual(self.converter.force(1, enUnitForce.kip, enUnitForce.kN), 4.44822, places=5)
        self.assertAlmostEqual(self.converter.force(1, enUnitForce.kip, enUnitForce.MN), 0.00444822, places=8)

    def test_stress_conversion(self):
        # SI to SI conversions
        self.assertAlmostEqual(self.converter.stress(1, enUnitStress.Pa, enUnitStress.KPa), 0.001, places=6)
        self.assertAlmostEqual(self.converter.stress(1, enUnitStress.Pa, enUnitStress.MPa), 1e-6, places=9)
        self.assertAlmostEqual(self.converter.stress(1, enUnitStress.KPa, enUnitStress.Pa), 1000, places=0)
        self.assertAlmostEqual(self.converter.stress(1, enUnitStress.MPa, enUnitStress.Pa), 1e6, places=0)
        self.assertAlmostEqual(self.converter.stress(1, enUnitStress.KPa, enUnitStress.MPa), 0.001, places=6)
        self.assertAlmostEqual(self.converter.stress(1, enUnitStress.MPa, enUnitStress.KPa), 1000, places=0)

        # US to US conversions
        self.assertAlmostEqual(self.converter.stress(1, enUnitStress.psi, enUnitStress.ksi), 0.001, places=6)
        self.assertAlmostEqual(self.converter.stress(1, enUnitStress.ksi, enUnitStress.psi), 1000, places=0)

        # SI to US conversions
        self.assertAlmostEqual(self.converter.stress(1, enUnitStress.Pa, enUnitStress.psi), 0.000145038, places=9)
        self.assertAlmostEqual(self.converter.stress(1, enUnitStress.KPa, enUnitStress.psi), 0.145038, places=6)
        self.assertAlmostEqual(self.converter.stress(1, enUnitStress.MPa, enUnitStress.psi), 145.038, places=3)
        self.assertAlmostEqual(self.converter.stress(1, enUnitStress.Pa, enUnitStress.ksi), 0.000000145038, places=12)
        self.assertAlmostEqual(self.converter.stress(1, enUnitStress.KPa, enUnitStress.ksi), 0.000145038, places=9)
        self.assertAlmostEqual(self.converter.stress(1, enUnitStress.MPa, enUnitStress.ksi), 0.145038, places=6)

        # US to SI conversions
        self.assertAlmostEqual(self.converter.stress(1, enUnitStress.psi, enUnitStress.Pa), 6894.757, places=3)
        self.assertAlmostEqual(self.converter.stress(1, enUnitStress.psi, enUnitStress.KPa), 6.894757, places=6)
        self.assertAlmostEqual(self.converter.stress(1, enUnitStress.psi, enUnitStress.MPa), 0.006894757, places=9)
        self.assertAlmostEqual(self.converter.stress(1, enUnitStress.ksi, enUnitStress.Pa), 6894757, places=0)
        self.assertAlmostEqual(self.converter.stress(1, enUnitStress.ksi, enUnitStress.KPa), 6894.757, places=3)
        self.assertAlmostEqual(self.converter.stress(1, enUnitStress.ksi, enUnitStress.MPa), 6.894757, places=6)

    def test_strain_conversion(self):
        # Unitless to percent and permil
        self.assertAlmostEqual(self.converter.strain(1, 'strain', 'percent'), 100, places=5)
        self.assertAlmostEqual(self.converter.strain(1, 'strain', 'permil'), 1000, places=5)

        # Percent to unitless and permil
        self.assertAlmostEqual(self.converter.strain(100, 'percent', 'strain'), 1, places=5)
        self.assertAlmostEqual(self.converter.strain(1, 'percent', 'permil'), 10, places=5)

        # Permil to unitless and percent
        self.assertAlmostEqual(self.converter.strain(1000, 'permil', 'strain'), 1, places=5)
        self.assertAlmostEqual(self.converter.strain(10, 'permil', 'percent'), 1, places=5)

    def test_mass_conversion(self):
        # SI to SI conversions
        self.assertAlmostEqual(self.converter.mass(1, 'kg', 'ton'), 0.001, places=6)
        self.assertAlmostEqual(self.converter.mass(1, 'ton', 'kg'), 1000, places=0)

        # SI to US conversions
        self.assertAlmostEqual(self.converter.mass(1, 'kg', 'lb'), 2.20462, places=5)
        self.assertAlmostEqual(self.converter.mass(1, 'ton', 'lb'), 2204.62, places=2)

        # US to SI conversions
        self.assertAlmostEqual(self.converter.mass(1, 'lb', 'kg'), 0.45359237, places=8)
        self.assertAlmostEqual(self.converter.mass(1, 'lb', 'ton'), 0.00045359237, places=11)
        
    def test_density_conversion(self):
        # Metric to Metric conversions
        self.assertAlmostEqual(self.converter.density(1, 'kg', enUnitLength.M, 'ton', enUnitLength.CM), 1e-9, places=12)
        self.assertAlmostEqual(self.converter.density(1, 'ton', enUnitLength.M, 'kg', enUnitLength.CM), 1e-3, places=0)
        self.assertAlmostEqual(self.converter.density(1, 'kg', enUnitLength.CM, 'ton', enUnitLength.M), 1e+3, places=5)
        self.assertAlmostEqual(self.converter.density(1, 'kg', enUnitLength.MM, 'ton', enUnitLength.M), 1e+6, places=12)

        # Imperial to Imperial conversions
        self.assertAlmostEqual(self.converter.density(1, 'lb', enUnitLength.FT, 'lb', enUnitLength.IN), 1/1728, places=12)
        self.assertAlmostEqual(self.converter.density(1, 'lb', enUnitLength.IN, 'lb', enUnitLength.FT), 1728, places=0)

        # Metric to Imperial conversions
        self.assertAlmostEqual(self.converter.density(1, 'kg', enUnitLength.M, 'lb', enUnitLength.FT), 0.062428, places=6)
        self.assertAlmostEqual(self.converter.density(1, 'ton', enUnitLength.M, 'lb', enUnitLength.FT), 62.42796, places=5)
        self.assertAlmostEqual(self.converter.density(1, 'kg', enUnitLength.CM, 'lb', enUnitLength.FT), 62428, places=0)
        self.assertAlmostEqual(self.converter.density(1, 'kg', enUnitLength.M, 'lb', enUnitLength.IN), 3.61273e-5, places=10)

        # Imperial to Metric conversions
        self.assertAlmostEqual(self.converter.density(1, 'lb', enUnitLength.FT, 'kg', enUnitLength.M), 16.0185, places=4)
        self.assertAlmostEqual(self.converter.density(1, 'lb', enUnitLength.FT, 'ton', enUnitLength.M), 0.0160185, places=7)
        self.assertAlmostEqual(self.converter.density(1, 'lb', enUnitLength.IN, 'kg', enUnitLength.CM), 0.0276799, places=7)
        
if __name__ == '__main__':
    unittest.main()
