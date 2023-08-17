import json
import pandas as pd

#################-- Global Constants --#######################
mass = 200
g = 9.81    # acceleration due to gravity
Cr = 0.013  # rolling friction constant
Cd = 1.1    # track constant
Af =0.5     # Frontal Area
row = 1.2   # Air Density
fdr = 5.2   # final drive ratio
Rw = 0.227  # Wheel Radius
Nt = 0.94   # Transmission Efficiency
p = 2.4     # tire pressure in bars

##################-- initialisations --########################
speedTimeArr = []
calculationsArr = []
calculatedRpm = 0.0
nt=0.0
rpm = 0.0

ds = pd.read_csv('./rtms.csv')
speedTime = ds.to_json(orient="records")

finalSpeedtime = json.loads(speedTime)

# print(finalSpeedtime)

#####################-- functions --############################
def calculations():
    for i in range(len(finalSpeedtime)):
        tempAccelerationArr = []
        calTorqueArr = []
        nt = 0.0
        rpm = 0.0

        
        if(int(finalSpeedtime[i]['Speed(kmph)'] == 0)):
            acceleration = 0
            aeroForce = 0
            Aforce = 0   ## Aforce is acceleration force
            Nforce = 0   ## Nforce is the net force
            Tw=0         ## where Tw is the wheel torque
            Tf=0         ## Final wheel torque
            motorTorque=0
            calculatedRpm = 0
            friction = 0
            rpm=0
            frictionCoeff = 0
        else:
            # friction = mass*g*Cr /
           
            
            t1 = float(finalSpeedtime[i-1]['Time(s)'])
            v1 = float(finalSpeedtime[i-1]['Speed(kmph)'])/3.6 
            t2 =  float(finalSpeedtime[i]['Time(s)'])
            v2 = float(finalSpeedtime[i]['Speed(kmph)'])/3.6
            
            print(v2)
            
            frictionCoeff = (0.0085 + (0.018/p) +((1.59*v2*v2)/(p*1000000)))
            friction = frictionCoeff*mass*g
            
            acceleration = (v2 - v1)/(t2 - t1)
            if(acceleration > 0.9):
                acceleration = 0
            
            calculatedRpm = (v2*60)/(2*3.14*Rw)
            
            rpm = calculatedRpm * fdr
            
            if(v1 < 11.11):
                aeroForce = 0
            else:
                aeroForce = 0.5*row*Cd*Af*v1*v1
            
            if(acceleration <= 0 ):
                Aforce = 0
                # Nforce = (Aforce - (friction + aeroForce))
                Nforce = 0
                acceleration = 0
                # if(Nforce < 0):
                #     Nforce = -(Nforce)
            else:
                Aforce = mass*acceleration
                Nforce = (Aforce- (friction + aeroForce))
                if(Nforce < 0):
                    Nforce = -(Nforce)
             
                
            Tw = Nforce*Rw 
            
            nt = (1 - Nt)*Tw
            
            # Tf = Tw + (Tw*(1-Nt))  
            
            Tf = Tw + nt
            
            motorTorque = Tf / fdr
            
        
        tempAccelerationArr.append(float(finalSpeedtime[i]['Time(s)']))
        tempAccelerationArr.append(float(finalSpeedtime[i]['Speed(kmph)']))
        tempAccelerationArr.append(float(finalSpeedtime[i]['Speed(kmph)'])/3.6)
        tempAccelerationArr.append(acceleration)
        tempAccelerationArr.append(Aforce)
        tempAccelerationArr.append(friction)
        tempAccelerationArr.append(aeroForce)
        tempAccelerationArr.append(Nforce)
        tempAccelerationArr.append(Tw)
        tempAccelerationArr.append(nt)
        tempAccelerationArr.append(Tf)
        tempAccelerationArr.append(round(motorTorque,1))
        tempAccelerationArr.append(round(rpm,1))
        
        speedTimeArr.append(tempAccelerationArr)
        
        calTorqueArr.append(round(motorTorque,1))
        calTorqueArr.append(round(calculatedRpm,1))
        calculationsArr.append(calTorqueArr)
        
        
        
calculations()

print(len(speedTimeArr))

# for i in range(len(speedTimeArr)):
#     if(speedTimeArr[i][11] > 37.5):
#         print(speedTimeArr[i][11])
#     else:
#         print("all good")
#############################################################################

################## -- declaring global variables-- #########################################
torqueX = []
roundArr = []
torqueArr = []
arrObj = []
tcArr = []
trArr = []
finalArr = []
efficiencyArr = []
diffArr = []
mappedArr = []
neArrray = []
diffTemp = []

fileName = input("Enter file name: ")

#################### --Initial Declarations-- ##############################################

# Update the file path as required for below methods.

# dt = pd.read_csv('./motor torque for indian drive cycle.csv')  # reading calculated torque csv
# calculatedTorque = dt.to_json(orient="records")

dg = pd.read_csv('./countour.csv') # reading efficiency csv
graph = dg.to_json(orient="records")

drc = pd.read_csv('./csv torque vs rpm vs current.csv')  # reading torque-current-rpm csv
rpmCurrent = drc.to_json(orient="records")

# finalTorque = json.loads(calculatedTorque)
finalG = json.loads(graph)
finalRpmCurrent = json.loads(rpmCurrent)




######################## --FUNCTIONS-- #####################################################

# ("function to remove #DIV/0 from the motor torque csv ,x is the JSON that is to be passed as argument") 

def removeDiv(x):
    for i in range(len(x)):
        if (x[i]['motor torque'] == '#DIV/0!'):
            x[i]['motor torque'] = 0


# function to round values|| a is the array and bis the rounding constant represent the number of decimal points
def roundArrayValues(a, b):
    for x in a:
        roundArr.append(round(x, b))


# def mapRpmCurrent():
#     for i in range(len(speedTimeArr)):
#         for j in range(len(finalRpmCurrent)):
#             tempArr69 = []
#             if (speedTimeArr[i][11]) == finalRpmCurrent[j]['Torque']:
#                 # tempArr69.append(float(speedTimeArr[i][11]))
#                 # tempArr69.append(float(speedTimeArr[i][12]))
#                 tempArr69.append(float(speedTimeArr[i][0]))
#                 tempArr69.append(float(speedTimeArr[i][1]))
#                 tempArr69.append(float(speedTimeArr[i][2]))
#                 tempArr69.append(float(speedTimeArr[i][3]))
#                 tempArr69.append(float(speedTimeArr[i][4]))
#                 tempArr69.append(float(speedTimeArr[i][5]))
#                 tempArr69.append(float(speedTimeArr[i][6]))
#                 tempArr69.append(float(speedTimeArr[i][7]))
#                 tempArr69.append(float(speedTimeArr[i][8]))
#                 tempArr69.append(float(speedTimeArr[i][9]))
#                 tempArr69.append(float(speedTimeArr[i][10]))
#                 tempArr69.append(float(speedTimeArr[i][11]))
#                 tempArr69.append(float(speedTimeArr[i][12]))
#                 # tempArr69.append(finalRpmCurrent[j]['RPM'])
#                 # tempArr69.append(finalRpmCurrent[j]['Current'])
#                 mappedArr.append(tempArr69)                             

# mapRpmCurrent()

def function():
    print('function triggered')
    for i in range(len(speedTimeArr)):
        tempArr69 = []
        tempArr69.append(float(speedTimeArr[i][0]))
        tempArr69.append(float(speedTimeArr[i][1]))
        tempArr69.append(float(speedTimeArr[i][2]))
        tempArr69.append(float(speedTimeArr[i][3]))
        tempArr69.append(float(speedTimeArr[i][4]))
        tempArr69.append(float(speedTimeArr[i][5]))
        tempArr69.append(float(speedTimeArr[i][6]))
        tempArr69.append(float(speedTimeArr[i][7]))
        tempArr69.append(float(speedTimeArr[i][8]))
        tempArr69.append(float(speedTimeArr[i][9]))
        tempArr69.append(float(speedTimeArr[i][10]))
        tempArr69.append(float(speedTimeArr[i][11]))
        tempArr69.append(float(speedTimeArr[i][12]))
        
        # tempArr69.append(finalRpmCurrent[j]['RPM'])
        # tempArr69.append(finalRpmCurrent[j]['Current'])
        mappedArr.append(tempArr69)
        
function()

print(len(mappedArr))

# print(len(mappedArr))

def efficiencyMapper():
    for i in range(len(mappedArr)):
        differenceArr = []
        efficiencyArray = []
        
        for j in range(len(finalG)):
            if (mappedArr[i][1] > finalG[j]['rpm']):
                diffRpm = mappedArr[i][1] - finalG[j]['rpm']
            if (finalG[j]['rpm'] > mappedArr[i][1]): 
                diffRpm = finalG[j]['rpm'] - mappedArr[i][1]
            if (mappedArr[i][1] == finalG[j]['rpm']):
                diffRpm = 0
            if (mappedArr[i][0] > finalG[j]['torque']):
                diffTor = mappedArr[i][0] - finalG[j]['torque']
            if (finalG[j]['torque'] > mappedArr[i][0]):
                diffTor = finalG[j]['torque'] - mappedArr[i][0]
            if (mappedArr[i][0] == finalG[j]['torque']):

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
                diffTor = 0

            totalDiff = diffTor + diffRpm
            differenceArr.append(totalDiff)

        efficiencyArray.append(mappedArr[i][0])
        efficiencyArray.append(mappedArr[i][1])
        efficiencyArray.append(mappedArr[i][11])
        
        # efficiencyArray.append(mappedArr[i][0])
        # efficiencyArray.append(mappedArr[i][0])
        
        Tm = (((100 - finalG[differenceArr.index(min(differenceArr))]
              ['efficiency'])/100)*mappedArr[i][11]) + mappedArr[i][11]
        efficiencyArray.append(
            finalG[differenceArr.index(min(differenceArr))]['efficiency'])
        efficiencyArray.append(Tm)
        
        neArrray.append(efficiencyArray)
        mappedArr[i].append(finalG[differenceArr.index(min(differenceArr))]['efficiency'])
        mappedArr[i].append(Tm)
        # mappedArr[i].append(rpm)
        
efficiencyMapper()


# def mapMotorTorqueToCurrent():
#     for i in range(len(neArrray)):
#         for j in range(len(finalRpmCurrent)):
#             # if (round(neArrray[i][4], 1) > 37.4):
#             #     neArrray[i][3] = 37.4
#             if (round(neArrray[i][4], 1) == finalRpmCurrent[j]['Torque']):
#                 neArrray[i].append(finalRpmCurrent[j]['Current'])
                
def mapMotorTorqueToCurrent():
    for i in range(len(mappedArr)):
        for j in range(len(finalRpmCurrent)):
            # if (round(neArrray[i][4], 1) > 37.4):
            #     neArrray[i][3] = 37.4
            if (round(mappedArr[i][14], 1) == finalRpmCurrent[j]['Torque']):
                mappedArr[i].append(finalRpmCurrent[j]['Current'])
                
            

mapMotorTorqueToCurrent()

#####################-- Dump Data into CSV  - #########################################

# df = pd.DataFrame(neArrray)
# column_names = ["Torque", "RPM", "Efficiency", "Motor-Torque", "Motor-Current"]

df = pd.DataFrame(mappedArr)
column_names = ["time", "speed", "speed(m/s)", "Acceleration", "Af", "Friction", "Aero Force", "Net Force", "Wheel Torque", "Trans Effi", "Final WTorque", "Motor Torque", "Motor-RPM", "Efficiency", "final Motor Torque", "Current"]
df.columns = column_names

df.to_excel(excel_writer="C: %s.xlsx" % fileName)  
