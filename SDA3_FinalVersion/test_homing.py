import threading
import DoBotArm as Dbt
import time
from serial.tools import list_ports
import platform
print(platform.architecture())

def port_selection():
    # Choosing port
    available_ports = list_ports.comports()
    print('Available COM-ports:')
    for i, port in enumerate(available_ports):
        print(f"  {i}: {port.description}")

    choice = int(input('Choose port by typing a number followed by [Enter]: '))
    return available_ports[choice].device

def homing_prompt():
    while (True):
        response = input("Do you wanna home? (y/n)")
        if(response == "y") :
            return True
        elif (response == "n"):
            return False
        else:
            print("Unrecognised response")

#--Main Program--
def main():
    #List selected ports for selection
    port = port_selection()
        
    # Preprogrammed sequence
    homeX, homeY, homeZ = 120, 0, 60
    print("Connecting")
    print("Homing")
    ctrlBot = Dbt.DoBotArm(port, homeX, homeY, homeZ, home = True) #Create DoBot Class Object with home position x,y,z

    print("Disconnecting")

#class doHoming:
#    homeX, homeY, homeZ = 0, -140, 60
#    port = 'COM9'
#    ctrlBot= Dbt.DoBotArm(port, homeX, homeY, homeZ, home = True)


class doHoming:
    def __init__(self, port):
        self.port = port
        self.ctrlBot = None

    def move_to_home(self):
        homeX, homeY, homeZ = 0, -140, 60
        self.ctrlBot = Dbt.DoBotArm(self.port, homeX, homeY, homeZ, home=True)

# Specify the port for the Dobot
port = 'COM9'

# Create an instance of the doHoming class and move to the home coordinates
homing_instance = doHoming(port)
homing_instance.move_to_home()



#if __name__ == "__main__":
#    main()
