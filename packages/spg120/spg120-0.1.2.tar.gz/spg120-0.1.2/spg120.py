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

    def getCurrentFilter(self):
        """ 
        Get the current filter of the AT-120FLC.
        """
        return self.__current_filter

    def changeFilter(self, next_filter:int):
        """ 
        Change the filter of the AT-120FLC.
        """
        if next_filter == self.__current_filter:
            return

        if next_filter < 1 or 6 < next_filter:
            raise ValueError("Filter number must be between 1 and 6.")

        # filter positions are at every 60 degrees
        # 1 pulse correpsonds to 0.36 degrees
        npulses = (next_filter - self.__current_filter) * int(60 / 0.36)
        if not DISABLE_CONTROLLER:
            self.__controller.move(0, npulses)
            self.__controller.waitForReady(10)

        self.__current_filter = next_filter

        print(f'Current Filter = {self.__current_filter}')

class SPG120():
    """
    Class for Spectrometer SPG-120 seriese by Shimadzu.
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
        self.__current_actual_wavelength_in_nm = 0

    def wavelength2pulses(self, wavelength_in_nm:float):
        """ 
        Convert wavelength in nm to number of pulses.
        """
        theta = math.asin(self.__coeff * wavelength_in_nm) * 180 / math.pi
        res = 0.0018 # (deg/pulse)
        next_pos = round(-1 * theta / res)

        return next_pos
    
    def pulses2wavelength(self, pulses:int):
        """ 
        Convert number of pulses to wavelength in nm.
        """
        res = 0.0018 # (deg/pulse)
        theta = -1 * pulses * res
        wavelength_in_nm = math.sin(theta / 180 * math.pi) / self.__coeff

        return wavelength_in_nm
    
    def getDeviceType(self):
        """ 
        Get the device type.
        """
        return self.__dev_type

    def changeWavelength(self, wavelength_in_nm:float):
        """ 
        Change the wavelength of the SPG120. See Page 17 of the manual M818-0129.
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

    def getCurrentActualWavelength(self):
        """ 
        Get the current actual wavelength.
        """
        return self.__current_actual_wavelength_in_nm

    def getCurrentNominalWavelength(self):
        """ 
        Get the current nominal wavelength.
        """
        return self.__current_nominal_wavelength_in_nm

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

        # We assume that SPG120 is connected to the first port of the controller and AT-120FLC is connected to the second port.
        # Min/Max speeds are 200/10000 pps and acceleration time is 200 ms for the first port
        # Min/Max speeds are 100/400 pps and acceleration time is 200 ms for the second port
        # See Table 6.1 of the sample software manual M818-0126 by Shimadzu
        if not DISABLE_CONTROLLER:
            self.__shot702.setSpeed(200, 10000, 200, 100, 400, 200)

        self.__spg120 = SPG120(self.__shot702, dev, C1, C2)
        self.__at120flc = AT120FLC(self.__shot702)

    def __del__(self):
        """ 
        Destructor for the Controller class.
        """
        if not DISABLE_CONTROLLER:
            self.__shot702.close()

    def getSPG120(self):
        """ 
        Get the SPG120 object.
        """
        return self.__spg120

    def getAT120FLC(self):
        """ 
        Get the AT120FLC object.
        """
        return self.__at120flc

    def changeWaveLength(self, wavelength_in_nm):
        """ 
        Change the wavelength of the spectrometer.
        
        Parameters
        ----------
        wavelength_in_nm : float
            The wavelength in nm.
        """
        device_type = self.__spg120.getDeviceType()
        if device_type == DeviceType.S or device_type == DeviceType.UV:
            if 400 < wavelength_in_nm <= 600:
                next_filter = 2 # VIS1
            elif 600 < wavelength_in_nm < 900:
                next_filter = 3 # VIS2
            else:
                next_filter = 1
        elif device_type == DeviceType.IR:
            if 700 < wavelength_in_nm <= 900:
                next_filter = 2 # VIS2
            elif 900 < wavelength_in_nm <= 1200:
                next_filter = 3 # NIR1
            elif 1200 < wavelength_in_nm <= 1700:
                next_filter = 4 # NIR2
            elif 1700 < wavelength_in_nm <= 2600:
                next_filter = 5 # NIR3
            else:
                next_filter = 1

        self.__at120flc.changeFilter(next_filter)
        self.__spg120.changeWavelength(wavelength_in_nm)
