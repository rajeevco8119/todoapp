import PySpice.Logging.Logging as Logging
logger = Logging.setup_logging()

from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *

circuit = Circuit('Voltage Divider')

circuit.V('input','in',circuit.gnd,10@u_V)
circuit.R(1,'in','out', 9@u_kΩ)
circuit.R(2, 'out', circuit.gnd, 1@u_kΩ)

simulator = circuit.simulator(temperature=25, nominal_temperature=25)

analysis = simulator.operating_point()
for node in (analysis['in'],analysis.out):
    print('Node {}: {} V'.format(str(node), float(node)))

# Node in: 10.0 V
# Node out: 1.0 V