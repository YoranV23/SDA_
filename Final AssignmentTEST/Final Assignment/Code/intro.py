import DoBotArm as dbt
import time
import DobotDllType as dType

# instantiating an object that represents the physical Dobot
homeX, homeY, homeZ = 250, 0, 50
ctrlDobot = dbt.DoBotArm("COM8", homeX, homeY, homeZ, home= False)

# move the dobot end effector in the xy plane
#dType.SetQueuedCmdClear(ctrlDobot.api)
ctrlDobot.moveArmXY(x= 200, y= 200)
print('line 8 successful') 
time.sleep(2)
# move in the xy plane relative to current position
ctrlDobot.moveArmRelXY(xrel= 10, yrel= 10)
print('line 12 successful')
time.sleep(2)
#dType.SetQueuedCmdStartExec(ctrlDobot.api)
# move the dobot to a given 3D coordinate
ctrlDobot.moveArmXYZ(x= 200, y= 10, z= 60)
print('line 17 successful')
time.sleep(2)

# move the dobot to a given 3D coordinate relative to current pos
ctrlDobot.moveArmRelXYZ(xrel= 45, yrel= -200, zrel= 10)
print('line 21 successful')
time.sleep(2)

ctrlDobot.pickToggle(itemHeight= 10)
ctrlDobot.toggleSuction()
ctrlDobot.pickToggle(itemHeight= 10)
ctrlDobot.toggleSuction()

ctrlDobot.SetConveyor(enabled= True, speed= -10000)
time.sleep(1)
ctrlDobot.SetConveyor(enabled= False)

ctrlDobot.dobotDisconnect()
