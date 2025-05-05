from bms.core import Variable, Block
import json
import numpy as np
# Custom Block: Amplify + Low Pass Filter + Saturate
# This block amplifies the input signal, applies a low pass filter, and saturates the output.

# Power array : [+5,3.3,voffset,vref,-5]
# Communication : I2C,I2S, USB, SPI
# Control signal : 16 component array



import json
from bms.core import Variable, Block
import numpy as np

class I2CDevice:
    """
    Represents an I2C device with its address and data value.
    Used for communication with I2C peripheral devices.
    """
    def __init__(self, address: int = 0, data: int = 0):
        self._address: int = address
        self._data: int = data

    @property
    def address(self) -> int:
        return self._address

    @address.setter
    def address(self, value: int) -> None:
        if not 0 <= value <= 127:  # Standard I2C address range
            raise ValueError("I2C address must be between 0 and 127")
        self._address = value

    @property
    def data(self) -> int:
        return self._data

    @data.setter
    def data(self, value: int) -> None:
        self._data = value



class AmplifyLPFSaturate(Block):
    gain = 1.0
    offset = 0.0
    i2caddress = 0x68
    def __init__(self, input_signal, output_signal, config_path):
        super().__init__([input_signal], [output_signal], max_input_order=1, max_output_order=1)

        self.input_signal = input_signal
        self.output_signal = output_signal
        self.config = self._load_config(config_path)

        # Parse configuration
        self.power = self.config.get("power", [])
        self.communication = self.config.get("communication", [])
        self.control = self.config.get("control", [0] * 16)

        # Class-level signal processing parameters
        self.gain = self._determine_gain()  # Stub, can be dynamic later
        self.offset = self._determine_offset()  # Stub, not used yet
        self.cutoff_freq = 1.0  # Hz (hardcoded for now)
        self.saturation_limit = 2.0  # volts (hardcoded for now)

        # Derived
        self.tau = 1 / (2 * 3.1415 * self.cutoff_freq)  # time constant for LPF

        # Internal state for LPF
        self.y = 0.0

    def _load_config(self, path):
        try:
            with open(path, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading config file: {e}")
            return {}

    def _determine_gain(self, comm):
        # Gain
        # if (i2caddress == comm.i2c.address):
        #     if (comm.i2c.data.param = 0x15)
        #         gain = comm.i2c.data.value
                
            # Example logic to determine gain based on I2C address

        return 5.0

    def _determine_offset(self):
        # Offset
        return 0.0

    def Evaluate(self, it, ts):
        u = self.input_signal._values[it]


        amplified = u * self.gain


        self.y += (ts / self.tau) * (amplified - self.y)


        saturated = max(-self.saturation_limit, min(self.saturation_limit, self.y))

        return [saturated]



# class AmplifyLPFSaturate(Block):
#     #To store : Gain and offset
#     def __init__(self, input_signal, output_signal, gain=5.0, cutoff_freq=1.0, saturation_limit=2.0,power =1.0,i2c= '0x68'):
#         """
#         input_signal : Signal
#         output_signal : Variable
#         gain : float
#         cutoff_freq : Hz
#         saturation_limit : float
#         """
#         super().__init__([input_signal], [output_signal], max_input_order=1, max_output_order=1)
#
#         self.input_signal = input_signal
#         self.output_signal = output_signal
#
#         self.gain = gain
#         self.tau = 1 / (2 * 3.1415 * cutoff_freq)  # time constant for LPF
#         self.saturation_limit = saturation_limit
#
#         # Internal state
#         self.y = 0.0  # LPF memory
#
#     def Evaluate(self, it, ts):
#         """
#         Called by BMSpy simulation engine at each timestep
#         it : current time index
#         ts : sampling time step
#         """
#         u = self.input_signal._values[it]  # Input value at current step
#
#         # Step 1: Amplification
#         amplified = u * self.gain
#
#         # Step 2: Low Pass Filtering (discrete time integration)
#         self.y += (ts / self.tau) * (amplified - self.y)
#
#         # Step 3: Saturation
#         saturated = max(-self.saturation_limit, min(self.saturation_limit, self.y))
#
#         # Return as single output
#         return [saturated]