import json
import pandas as pd

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

dt = pd.read_csv('./motor torque artimes drivecycle.csv')  # reading calculated torque csv
calculatedTorque = dt.to_json(orient="records")

dg = pd.read_csv('./countour.csv') # reading efficiency csv
graph = dg.to_json(orient="records")

drc = pd.read_csv('./csv torque vs rpm vs current.csv')  # reading torque-current-rpm csv
rpmCurrent = drc.to_json(orient="records")

finalTorque = json.loads(calculatedTorque)
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


def mapRpmCurrent():
    for i in range(len(finalTorque)):
        for j in range(len(finalRpmCurrent)):
            tempArr69 = []
            if (float(finalTorque[i]['motor torque']) == finalRpmCurrent[j]['Torque']):
                tempArr69.append(float(finalTorque[i]['motor torque']))
                tempArr69.append(finalRpmCurrent[j]['RPM'])
                tempArr69.append(finalRpmCurrent[j]['Current'])
                mappedArr.append(tempArr69)
            
                                


mapRpmCurrent()

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
        Tm = (((100 - finalG[differenceArr.index(min(differenceArr))]
              ['efficiency'])/100)*mappedArr[i][0]) + mappedArr[i][0]
        efficiencyArray.append(
            finalG[differenceArr.index(min(differenceArr))]['efficiency'])
        efficiencyArray.append(Tm)
        neArrray.append(efficiencyArray)

efficiencyMapper()

def mapMotorTorqueToCurrent():
    for i in range(len(neArrray)):
        for j in range(len(finalRpmCurrent)):
            if (round(neArrray[i][3], 1) > 37.4):
                neArrray[i][3] = 37.4
            if (round(neArrray[i][3], 1) == finalRpmCurrent[j]['Torque']):
                neArrray[i].append(finalRpmCurrent[j]['Current'])
            

mapMotorTorqueToCurrent()

#####################-- Dump Data into CSV  - #########################################

# df = pd.DataFrame(neArrray)
# column_names = ["Torque", "RPM", "Efficiency", "Motor-Torque", "Motor-Current"]
# df.columns = column_names

# df.to_excel(excel_writer="C: %s.xlsx" % fileName)  
