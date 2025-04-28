from bms.core import Variable, Block
import numpy as np

class AmplifyLPFSaturate(Block):
    def __init__(self, input_signal, output_signal, gain=5.0, cutoff_freq=1.0, saturation_limit=2.0):
        """
        input_signal : Signal
        output_signal : Variable
        gain : float
        cutoff_freq : Hz
        saturation_limit : float
        """
        super().__init__([input_signal], [output_signal], max_input_order=1, max_output_order=1)

        self.input_signal = input_signal
        self.output_signal = output_signal

        self.gain = gain
        self.tau = 1 / (2 * 3.1415 * cutoff_freq)  # time constant for LPF
        self.saturation_limit = saturation_limit

        # Internal state
        self.y = 0.0  # LPF memory

    def Evaluate(self, it, ts):
        """
        Called by BMSpy simulation engine at each timestep
        it : current time index
        ts : sampling time step
        """
        u = self.input_signal._values[it]  # Input value at current step

        # Step 1: Amplification
        amplified = u * self.gain

        # Step 2: Low Pass Filtering (discrete time integration)
        self.y += (ts / self.tau) * (amplified - self.y)

        # Step 3: Saturation
        saturated = max(-self.saturation_limit, min(self.saturation_limit, self.y))

        # Return as single output
        return [saturated]