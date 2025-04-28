from bms.signals.functions import Sinus
from bms.core import Variable, DynamicSystem
from bms.blocks.custom import AmplifyLPFSaturate

# Create input
sine = Sinus(name="SineInput", amplitude=1.0, w=2*3.1415, phase=0, offset=0)
output = Variable("Output")

# Create custom block
block = AmplifyLPFSaturate(sine, output, gain=50.0, cutoff_freq=0.5, saturation_limit=20.0)

# Create DynamicSystem
system = DynamicSystem(2.0, 1000, blocks=[block])
system.Simulate()

# Plot
import matplotlib.pyplot as plt
plt.plot(system.t, output.values)
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.title("Amplify + LPF + Saturate Output (Custom BMSpy Block)")
plt.grid(True)
plt.show()