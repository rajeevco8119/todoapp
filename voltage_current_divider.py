import PySpice.Logging.Logging as Logging
logger = Logging.setup_logging()

from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *

circuit = Circuit('Voltage Divider')
circuit.V('input', 1, circuit.gnd, 10@u_V)
circuit.R(1, 1, 2, 2@u_kΩ)
circuit.R(2, 2, circuit.gnd, 1@u_kΩ)

simulator = circuit.simulator(temperature=25, nominal_temperature=25)
analysis = simulator.operating_point()

for node in analysis.nodes.values():
    print('Node {}: {:5.2f} V'.format(str(node), float(node)))

circuit = Circuit('Current Divider')

circuit.I('input', 1, circuit.gnd, 1@u_A) # Fixme: current value
circuit.R(1, 1, circuit.gnd, 2@u_kΩ)
circuit.R(2, 1, circuit.gnd, 1@u_kΩ)

for resistance in (circuit.R1,circuit.R2):
    resistance.minus.add_current_probe(circuit)

simulator = circuit.simulator(temperature=25, nominal_temperature=25)
analysis = simulator.operating_point()

for node in analysis.branches.values():
    print('Node {}: {:5.2f} A'.format(str(node), float(node)))

