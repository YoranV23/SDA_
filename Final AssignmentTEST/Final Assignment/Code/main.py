from state_machine import *

system = SystemOperations()
print(system.state)
system.trigger('start_system')
print(system.state)
