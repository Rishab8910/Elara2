import time
from agent.modbus_comm import ModbusController
from agent.robot_comm import RobotInterface

if __name__ == '__main__':
    print("Starting Elara Agent...")
    robot = RobotInterface()
    modbus = ModbusController()
    while True:
        robot.check_commands()
        modbus.ping()
        time.sleep(1)
