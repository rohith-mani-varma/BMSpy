from bms.signals.functions import Sinus
from bms.core import Variable, DynamicSystem
from bms.blocks.custom import AmplifyLPFSaturate


sine = Sinus(name="SineInput", amplitude=1.0, w=2*3.1415, phase=0, offset=0)
cosine = Sinus(name="CosineInput", amplitude=1.0, w=2*3.1415, phase=3.1415/2, offset=0)
output = Variable("Output")
cosOutput = Variable("CosineOutput")


block = AmplifyLPFSaturate(sine, output)
# block.com(i2c)
block2 = AmplifyLPFSaturate(cosine, cosOutput, "config.json")


system = DynamicSystem(2.0, 1000, [block,block2])
system.Simulate()

# Plot
import matplotlib.pyplot as plt
plt.plot(system.t, output.values)
plt.plot(system.t, cosOutput.values)
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.title("Amplify + LPF + Saturate Output (Custom BMSpy Block)")
plt.grid(True)
plt.show()