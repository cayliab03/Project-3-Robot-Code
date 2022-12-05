import sys
sys.path.append('../')
from Common.project_library import *

# Modify the information below according to you setup and uncomment the entire section

# 1. Interface Configuration
project_identifier = 'P3B' # enter a string corresponding to P0, P2A, P2A, P3A, or P3B
ip_address = '192.168.7.30' # enter your computer's IP address
hardware = False # True when working with hardware. False when working in the simulation

# 2. Servo Table configuration
short_tower_angle = 270 # enter the value in degrees for the identification tower 
tall_tower_angle = 0 # enter the value in degrees for the classification tower
drop_tube_angle = 180#270# enter the value in degrees for the drop tube. clockwise rotation from zero degrees

# 3. Qbot Configuration
bot_camera_angle = -21.5 # angle in degrees between -21.5 and 0

# 4. Bin Configuration
# Configuration for the colors for the bins and the lines leading to those bins.
# Note: The line leading up to the bin will be the same color as the bin 

bin1_offset = 0.20 # offset in meters
bin1_color = [1,0,0] # e.g. [1,0,0] for red
bin2_offset = 0.20
bin2_color = [0,1,0]
bin3_offset = 0.20
bin3_color = [0,0,1]
bin4_offset = 0.20
bin4_color = [0.63,0.23,0.78]

#--------------- DO NOT modify the information below -----------------------------

if project_identifier == 'P0':
    QLabs = configure_environment(project_identifier, ip_address, hardware).QLabs
    bot = qbot(0.1,ip_address,QLabs,None,hardware)
    
elif project_identifier in ["P2A","P2B"]:
    QLabs = configure_environment(project_identifier, ip_address, hardware).QLabs
    arm = qarm(project_identifier,ip_address,QLabs,hardware)

elif project_identifier == 'P3A':
    table_configuration = [short_tower_angle,tall_tower_angle,drop_tube_angle]
    configuration_information = [table_configuration,None, None] # Configuring just the table
    QLabs = configure_environment(project_identifier, ip_address, hardware,configuration_information).QLabs
    table = servo_table(ip_address,QLabs,table_configuration,hardware)
    arm = qarm(project_identifier,ip_address,QLabs,hardware)
    
elif project_identifier == 'P3B':
    table_configuration = [short_tower_angle,tall_tower_angle,drop_tube_angle]
    qbot_configuration = [bot_camera_angle]
    bin_configuration = [[bin1_offset,bin2_offset,bin3_offset,bin4_offset],[bin1_color,bin2_color,bin3_color,bin4_color]]
    configuration_information = [table_configuration,qbot_configuration, bin_configuration]
    QLabs = configure_environment(project_identifier, ip_address, hardware,configuration_information).QLabs
    table = servo_table(ip_address,QLabs,table_configuration,hardware)
    arm = qarm(project_identifier,ip_address,QLabs,hardware)
    bins = bins(bin_configuration)
    bot = qbot(0.1,ip_address,QLabs,bins,hardware)
    

#---------------------------------------------------------------------------------
# STUDENT CODE BEGINS
#---------------------------------------------------------------------------------

import random
def random_num():
    global num
    num = random.randint(1,6)
    
masslist = []
def dispense(bottle_number):
    masslist.append(table.dispense_container(bottle_number,True)[1])
#dispensing a ramdom container, determine its mass and append it to the masslist

    
#this function will command the Q-Arm to load the container onto the hopper
def load():
    arm.home()
    arm.rotate_shoulder(39)
    arm.rotate_elbow(-19)
    arm.control_gripper(40)
    #ajusting positioning of the arm to pick up container
    time.sleep(1)
    #putting sleep steps between actions prevents skipping by giving
    #arm time to process
    arm.move_arm(0.406,0.0, 0.483)
    #coordinates of home position
    time.sleep(1)
    arm.rotate_elbow(-8)
    time.sleep(1)
    arm.rotate_base(-90)
    time.sleep(1)
    arm.rotate_shoulder(5)
    time.sleep(1)
    arm.rotate_elbow(8)
    time.sleep(1)
    arm.control_gripper(-38)
    #comanding the arm to load container onto hopper attached to Q-Bot
    time.sleep(1)
    arm.rotate_elbow(-12)
    time.sleep(1)
    arm.home() 


#this function will get the Q-Bot to move around the yellow line by configuring it
#to the sensors as well as depositing the container into the bin
def transfer(bottle_number):
    i = 0
    #while loop because we want an infinite loop
    while i <= 1:
        ir_sensor = bot.line_following_sensors()
        left_sensor = ir_sensor[0]
        right_sensor = ir_sensor[1]
        if left_sensor == 1 and right_sensor == 0:
            bot.set_wheel_speed([0,0.1])
        elif left_sensor == 0 and right_sensor == 1:
            bot.set_wheel_speed([0.1,0])
        else:
            bot.set_wheel_speed([0.07,0.07])
            bot.activate_color_sensor()
            color = bot.read_color_sensor()
            position = bot.position()

#each of these if statements is a condition configured to the coordinate points
#of each bin, making it so that based on the random bottle dispensed, the bot
#will go to the correct container
            if bottle_number == 1:
                p1 = (0.1,-0.8,0.0008)
                p2 = (-0.1,-0.6,0.0007)
                if color[0] == [0,0,1] and p2<=position<=p1:
                    break
            elif bottle_number == 2 or bottle_number == 5:
                p1 = (1.1,0.7,0.0008)
                p2 = (1.06,0.6,0.0007)
                if color[0] == [1,0,0] and p2<=position<=p1:
                    
                    break
            elif bottle_number == 4 or bottle_number == 6:
                p1 = (1.2,-0.6,0.0008)
                p2 = (0.8,-0.7,0.0007)
                if color[0] == [0.63,0.23,0.78] and p2<=position<=p1:
                    
                    break

            elif bottle_number == 3:
                p1 = (0.1,0.8,0.0008)
                p2 = (0,0.7,0.0007)
                if color[0] == [0,1,0] and p2 <=position <= p1:
                    
                    break
            else:
                pass
            
                  
def deposit():
    time.sleep(2)
    bot.stop
    bot.rotate(-90)
    bot.forward_distance(0.14)
    time.sleep(1)
    bot.rotate(90)
    time.sleep(1)
    bot.activate_linear_actuator()
    bot.dump()
    bot.stop()
    
#this function will have the Q-Bot return home after depositing the container
#as well as stopping it in the home position
def return_home():
    i = 0
    #while loop because we want it to be able to run in an infinite loop
    while i < 1:
        ir_sensor = bot.line_following_sensors()
        left = ir_sensor[0]
        right = ir_sensor[1]
        if left == 1 and right == 0:
            bot.set_wheel_speed([0,0.1])
        elif left == 0 and right == 1:
            bot.set_wheel_speed([0.1,0])
        else:
            bot.set_wheel_speed([0.07,0.07])
            position = bot.position()
            p1 = (1.4, -2.5, 0.0007)
            p2 = (1.5, -2.4, 0.0008)
            if p1 < position < p2:
                bot.stop()
                bot.rotate(10)
                bot.forward_distance(0.38)
                bot.rotate(-90)
                bot.forward_distance(0.1)
                bot.rotate(90)
                break


list = []
def main():
    random_num()
    #select a random number 
    dispense(num)
    #dispense it on the sorting station
    print("the bottle number on the sorting station is" + "  " + str(num))
    list.append(num)
    #append this number to the new empty list
    i = 0
    while i <1:
        #start an infinite loop
        load()
        #load it to the qbot
        random_num()
        #select a new random number
        dispense(num)
        #dispense it on sorting station
        print("the bottle number on the sorting station is" + "  " + str(num))
        list.append(num)
        #append this number to the list
        print("the total weight is "+str(masslist[-1]+masslist[-2]))
        if num == list[-2]  and masslist[-1] +masslist[-2] <=90:
            #check if the current random number equals to the penultimate one in the list(the penultimate one is the previous random number and the total mass)
            load()
            random_num()
            #select a new random number
            dispense(num)
            #dispense it to the sorting station
            print("the bottle number on the sorting station is" + "  " + str(num))
            list.append(num)
            print("the total weight is "+str(masslist[-1]+masslist[-2]+masslist[-3]))
            #add it to the list
            if num == list[-2] and masslist[-1]+masslist[-2]+masslist[-3] <= 90:
            #check if the current random number equals to the penultimate one in the list(the penultimate one is the previous random number and the total mass)
                load()
                random_num()
                dispense(num)
                pass
            else:
                pass
        else:
            pass
        transfer(list[-2])
        #transfer to the corresponding bins for the penultimate bottle
        #the penultimate bottle is certainly on the qbot
        deposit()
        return_home()
main()

    
#---------------------------------------------------------------------------------
# STUDENT CODE ENDS
#---------------------------------------------------------------------------------
