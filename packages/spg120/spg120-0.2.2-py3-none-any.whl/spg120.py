import enum
import math

import sigma_koki

DISABLE_CONTROLLER = False

class DeviceType(enum.Enum):
    """
    Enum for device type.
    """
    S = 1
    UV = 2
    IR = 3

class AT120FLC():
    """
    Class for Filter Changer AT-120FLC by Shimadzu.
    """
    
    def __init__(self, controller):
        """
        Initialize the AT120FLC class.
        """
        self.__controller = controller
        if not DISABLE_CONTROLLER:
            self.__controller.move(0, -3000) # find the mechanical origin
            self.__controller.waitForReady(10)
            self.__controller.move(0, 10) # rotate by 3.6 degrees
            self.__controller.waitForReady(10)
            self.__controller.initializeOrigin(False, True) # initialize the 2nd port

        self.__current_filter = 1
        self.printCurrentFilter()

    def getCurrentFilter(self) -> int:
        """
        Get the current filter of the AT-120FLC.
        """
        return self.__current_filter

    def printCurrentFilter(self) -> None:
        """
        Print the current filter of the AT-120FLC.
        """
        print(f'Current Filter = {self.__current_filter}')

    def changeFilter(self, next_filter:int) -> None:
        """
        Change the filter of the AT-120FLC.
        """
        if next_filter == self.__current_filter:
            return

        if next_filter < 1 or 6 < next_filter:
            raise ValueError("Filter number must be between 1 and 6.")

        # filter positions are at every 60 degrees
        # 1 pulse correpsonds to 0.36 degrees
        npulses = (next_filter - self.__current_filter) * round(60 / 0.36)
        if not DISABLE_CONTROLLER:
            self.__controller.move(0, npulses)
            self.__controller.waitForReady(10)

        self.__current_filter = next_filter

        self.printCurrentFilter()

class SPG120REV():
    """
    Class for the spectrometer SPG-120-REV by Shimadzu.
    """
    def __init__(self, controller, dev:DeviceType, c1:float, c2:float):
        self.__controller = controller
        self.__dev_type = dev # Device type
        self.__C1 = c1 # Calibration parameter C1, offset pulse
        self.__C2 = c2 # Calibration parameter C2, optical mount correction coefficient

        m = -1
        deg = 180. / math.pi
        # number of gratings per meter
        Ng = 600e3 if self.__dev_type == DeviceType.IR else 1200e3
        K = 14.4 * deg
        ConstDefK_nom = Ng * m / (2 * math.cos(K / (180 *deg) * math.pi) * 1e9)
        self.__coeff = ConstDefK_nom * (1 + self.__C2)

        if not DISABLE_CONTROLLER:
            self.__controller.returnToMechanicalOrigin(True, False)
            self.__controller.waitForReady(10)
            self.__controller.move(self.__C1 - 1000, 0)
            self.__controller.waitForReady(10)
            self.__controller.initializeOrigin(True, False) # initialize the 1st port

        self.__current_pos = 0
        self.__current_nominal_wavelength_in_nm = 0
        self.__current_actual_wavelength_in_nm = self.pulses2wavelength(self.__current_pos)

        self.printCurrentWavelength()

    def printCurrentWavelength(self) -> None:
        """
        Print the current nominal and actual wavelengths.
        """
        print(f'Current Nominal and Actual Wavelengths = {self.__current_nominal_wavelength_in_nm : .3f}, {self.__current_actual_wavelength_in_nm : .3f} (nm)')

    def wavelength2pulses(self, wavelength_in_nm:float) -> int:
        """
        Convert wavelength in nm to number of pulses.
        """
        theta = math.asin(self.__coeff * wavelength_in_nm) * 180 / math.pi
        res = 0.0018 # (deg/pulse)
        next_pos = round(-1 * theta / res)

        return next_pos
    
    def pulses2wavelength(self, pulses:int) -> float:
        """
        Convert number of pulses to wavelength in nm.
        """
        res = 0.0018 # (deg/pulse)
        theta = -1 * pulses * res
        wavelength_in_nm = math.sin(theta / 180 * math.pi) / self.__coeff

        return wavelength_in_nm
    
    def getDeviceType(self) -> DeviceType:
        """
        Get the device type.
        """
        return self.__dev_type

    def changeWavelength(self, wavelength_in_nm:float) -> None:
        """
        Change the wavelength of the SPG120REV. See Page 17 of the manual M818-0129.
        Parameters
        ----------
        wavelength_in_nm : float
            The wavelength in nm.
        """
        if self.__dev_type == DeviceType.S or self.__dev_type == DeviceType.UV:
            if wavelength_in_nm < 0 or 1300 < wavelength_in_nm:
                raise ValueError("Wavelength must be between 0 and 1300 nm.")
        elif self.__dev_type == DeviceType.IR:
            if wavelength_in_nm < 0 or 2600 < wavelength_in_nm:
                raise ValueError("Wavelength must be between 0 and 2600 nm.")

        next_pos = self.wavelength2pulses(wavelength_in_nm)

        if not DISABLE_CONTROLLER:
            if next_pos == self.__current_pos:
                pass
            elif next_pos > self.__current_pos:
                self.__controller.move(next_pos - self.__current_pos, 0)
                self.__controller.waitForReady(10)
            else:
                # Step backward by additional 800 pulses to avoid backlash.
                # See Page 14 of the manual M818-0129.
                delta = 800
                self.__controller.move(next_pos - self.__current_pos - delta, 0)
                self.__controller.waitForReady(10)
                self.__controller.move(+delta, 0)
                self.__controller.waitForReady(10)

        self.__current_pos = next_pos
        self.__current_nominal_wavelength_in_nm = wavelength_in_nm
        self.__current_actual_wavelength_in_nm = self.pulses2wavelength(next_pos)

        print(f'Current Nominal and Actual Wavelengths = {self.__current_nominal_wavelength_in_nm : .3f}, {self.__current_actual_wavelength_in_nm : .3f} (nm)')

    def getCurrentActualWavelength(self) -> float:
        """
        Get the current actual wavelength.
        """
        return self.__current_actual_wavelength_in_nm

    def getCurrentNominalWavelength(self) -> float:
        """
        Get the current nominal wavelength.
        """
        return self.__current_nominal_wavelength_in_nm

class FilterConfig():
    """
    Class for filter configuration.
    """
    def __init__(self):
        self.__config__ = []

    def addConfig(self, start_wavelength:float, end_wavelength:float, filter_number:int) -> None:
        self.__config__.append((start_wavelength, end_wavelength, filter_number))

    def getConfigList(self) -> list:
        return self.__config__

    def makeDefaultConfig(device_type:DeviceType) -> 'FilterConfig':
        config = FilterConfig()
        inf = float('inf')
        if device_type == DeviceType.S or device_type == DeviceType.UV:
            config.addConfig(-inf, 400, 1)
            config.addConfig(400, 600, 2)
            config.addConfig(600, 900, 3)
            config.addConfig(900, inf, 1)
        elif device_type == DeviceType.IR:
            config.addConfig(-inf, 700, 1)
            config.addCofig(700, 900, 2) # VIS2
            config.addConfig(900, 1200, 3) # NIR1
            config.addConfig(1200, 1700, 4) # NIR2
            config.addConfig(1700, 2600, 5) # NIR3
            config.addConfig(2600, inf, 1)

        return config

class Controller():
    """
    Class for stage controller.
    """
    def __init__(self, path, dev:DeviceType, C1, C2):
        """
        Initialize the Controller class.
        
        Parameters
        ----------
        path : str
            The device name like '/dev/ttyUSB0' or '/dev/tty.usbserial-A4008T7f'.
        """
        self.__shot702 = sigma_koki.SHOT702()
        if not DISABLE_CONTROLLER:
            self.__shot702.open(path)
            status = self.__shot702.getStatus()
            values = status.split(',')
            if values[2] != 'K' or values[3] != 'K' or values[4] != 'R':
                print(status)
                raise ValueError("The controller status is abnormal.")

        # We assume that SPG120REV is connected to the first port of the controller and AT-120FLC is connected to the second port.
        # Min/Max speeds are 200/10000 pps and acceleration time is 200 ms for the first port
        # Min/Max speeds are 100/400 pps and acceleration time is 200 ms for the second port
        # See Table 6.1 of the sample software manual M818-0126 by Shimadzu
        if not DISABLE_CONTROLLER:
            self.__shot702.setSpeed(200, 10000, 200, 100, 400, 200)

        self.__spg120rev = SPG120REV(self.__shot702, dev, C1, C2)
        self.__at120flc = AT120FLC(self.__shot702)
        self.__filter_config = FilterConfig.makeDefaultConfig(dev)

    def __del__(self):
        """
        Destructor for the Controller class.
        """
        if not DISABLE_CONTROLLER:
            self.__shot702.close()

    def getSPG120REV(self):
        """
        Get the SPG120REV object.
        """
        return self.__spg120rev

    def getAT120FLC(self):
        """
        Get the AT120FLC object.
        """
        return self.__at120flc

    def setFilterConfig(self, config:FilterConfig) -> None:
        """
        Set the filter configuration.
        
        Parameters
        ----------
        config : FilterConfig
            The filter configuration.
        """
        self.__filter_config = config

    def changeWaveLength(self, wavelength_in_nm):
        """"
        Change the wavelength of the spectrometer.
        
        Parameters
        ----------
        wavelength_in_nm : float
            The wavelength in nm.
        """
        configList = self.__filter_config.getConfigList()

        for i in range(len(configList)):
            start_wavelength, end_wavelength, filter_number = configList[i]
            if start_wavelength < wavelength_in_nm <= end_wavelength:
                next_filter = filter_number
                break

        self.__at120flc.changeFilter(next_filter)
        self.__spg120rev.changeWavelength(wavelength_in_nm)
