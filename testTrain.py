#Import Libraries 
import json
import pandas as pd
import numpy


##################-- declaring global variables--#########################################
torqueX = []
arr =[]
torqueArr =[]
arrObj =[]

tcArr = []
trArr = []
finalArr = []
efficiencyArr = []
diffArr = []

mappedArr = []

speedTimeArr = []

#############################--Initial Declarations--#########################################################
# reading torque vs current csv
# df = pd.read_csv('./csv torque vs current.csv')  
# result = df.to_json(orient="records")

# reading the calculated torque csv
dt = pd.read_csv('./calculated torque.csv')     # Update the file path as required.
calculatedTorque = dt.to_json(orient="records")

ds = pd.read_csv('./d1.csv')
speedTime = ds.to_json(orient="records")

# reading torque vs rpm csv
# dr = pd.read_csv('./csv torque vs rpm.csv')
# rpm = dr.to_json(orient="records")

dg = pd.read_csv('./countour.csv')
graph = dg.to_json(orient="records")

drc = pd.read_csv('./csv torque vs rpm vs current.csv')
rpmCurrent = drc.to_json(orient="records")

# Converting read csv files to JSON
# finalJ = json.loads(result)
finalTorque = json.loads(calculatedTorque)
# finalR = json.loads(rpm)
finalG = json.loads(graph)
finalRpmCurrent = json.loads(rpmCurrent)
finalSpeedtime = json.loads(speedTime)

# print(finalRpmCurrent[0])
# print(finalTorque[0]['motor torque'])


# function to remove #DIV/0 from the motor torque csv

            
#################################--FUNCTIONS--#####################################################

def acceleration():
    for i in range(len(finalSpeedtime)):
        tempAccelerationArr = []
        if(finalSpeedtime[i]['t(s)'] == 0):
            print()

def removeDiv():
    for i in range(len(finalTorque)):
        if(finalTorque[i]['motor torque'] == '#DIV/0!'):
            finalTorque[i]['motor torque'] = 0

# function to map torque with RPM
# def torqueRpm():
#   for i in range(len(finalTorque)):
#     for j in range(len(finalR)):
#         if(float(finalTorque[i]['motor torque']) == finalR[j]['Torque']):
#             tempArr =[]
#             # print(finalTj[i]['motor torque'], finalR[j]['RPM'])
#             # print( finalR[j]['RPM'])
#             # print(finalTj[i]['motor torque'])
#             tempArr.append(float(finalTorque[i]['motor torque']))
#             tempArr.append(finalR[j]['RPM'])
#             # print(tempArr)
#             trArr.append(tempArr)

#         # else:
#         #     print('not equal')
        
        
# function to map torque with current       
# def torqueCurrent():
#     for i in range(len(finalTorque)):
#         for j in range(len(finalJ)):
#             if(float(finalTorque[i]['motor torque'])== finalJ[j]['Torque']):
#                 tempArr2 =[]
#                 # print(finalTj[i]['motor torque'], finalJ[j]['Current'])
#                 # print(finalJ[j]['Current'])
#                 # print(finalTj[i]['motor torque'])
#                 tempArr2.append(float(finalTorque[i]['motor torque']))
#                 tempArr2.append(finalJ[j]['Current'])
#                 tcArr.append(tempArr2)
#         # else:
#             # print('not equal')
        
    
def roundArrayValues():
    for x in finalTorque:  
        arr.append(round(x,1))  

def mapRpmCurrent():
    for i in range(len(finalTorque)):
        for j in range(len(finalRpmCurrent)):
            tempArr69 = []
            if(float(finalTorque[i]['motor torque']) == finalRpmCurrent[j]['Torque']):
                tempArr69.append(float(finalTorque[i]['motor torque']))
                tempArr69.append(finalRpmCurrent[j]['RPM'])
                tempArr69.append(finalRpmCurrent[j]['Current'])
                mappedArr.append(tempArr69)
    
mapRpmCurrent()
print((mappedArr[2]))
        
# Calling functions 

# removeDiv()

# torqueRpm()
# torqueCurrent()

# print(len(tcArr))
# print(len(trArr))


# ######### below code is for mapping efficiency

# for i in range(len(tcArr)):
#     for j in range(len(trArr)):
#         tempArr3 = []
#         if(tcArr[i][0] == trArr[j][0]):
#             tempArr3.append(tcArr[i][0])
#             tempArr3.append(tcArr[i][1])
#             tempArr3.append(trArr[j][1])
#             finalArr.append(tempArr3)
#             # print(tempArr3)
#             # print('matched')

# print(len(finalArr))
neArrray = []
diffTemp = []

for i in range(len(mappedArr)):
    differenceArr = []
    efficiencyArray = []
    for j in range(len(finalG)):
        if(mappedArr[i][1] > finalG[j]['rpm']):
            diffRpm = mappedArr[i][1] - finalG[j]['rpm']
        if(finalG[j]['rpm'] > mappedArr[i][1]):
            diffRpm = finalG[j]['rpm'] - mappedArr[i][1]
        if(mappedArr[i][1] == finalG[j]['rpm']):
            diffRpm = 0
        if(mappedArr[i][0] > finalG[j]['torque']):
            diffTor = mappedArr[i][0] - finalG[j]['torque']
        if(finalG[j]['torque'] > mappedArr[i][0]):
            diffTor = finalG[j]['torque'] - mappedArr[i][0]
        if(mappedArr[i][0] == finalG[j]['torque'] ):
            diffTor = 0
        
        totalDiff = diffTor + diffRpm    
        differenceArr.append(totalDiff)
        
    # print(finalG[differenceArr.index(min(differenceArr))]['efficiency'])
    efficiencyArray.append(mappedArr[i][0])
    efficiencyArray.append(mappedArr[i][1]) 
    # efficiencyArray.append(mappedArr[i][2]) 
    Tm =   (((100 - finalG[differenceArr.index(min(differenceArr))]['efficiency'])/100)*mappedArr[i][0]) + mappedArr[i][0]
    efficiencyArray.append(finalG[differenceArr.index(min(differenceArr))]['efficiency'])  
    efficiencyArray.append(Tm)
    neArrray.append(efficiencyArray)   
    
# print(neArrray) 

def mapMotorTorqueToCurrent():
    for i in range(len(neArrray)):
        for j in range(len(finalRpmCurrent)):
            if(round(neArrray[i][3],1) == finalRpmCurrent[j]['Torque']):
                neArrray[i].append(finalRpmCurrent[j]['Current'])
                
mapMotorTorqueToCurrent()

# print(len(neArrray))
                

df = pd.DataFrame(neArrray)

#df = pd.DataFrame(toq_count,columns=['500','1000','1500','2000','2500','3000','3500','4000','4500','5000','Total%'])

#df = pd.DataFrame({'500':toq_count[0:31][0]})

column_names = ["Torque", "RPM", "Efficiency", "Motor-Torque", "Motor-Current"]
df.columns = column_names

df.to_excel(excel_writer = "C: test.xlsx")
          
# for i in range(len(finalArr)):
#     diffTemp = []
#     for j in range(len(finalG)):
#         k = finalArr[i][]
        
        # if(finalArr[i][2] > finalG[j]['rpm']):
        #     diffRpm = finalArr[i][2] - finalG[j]['rpm']
        # if(finalG[j]['rpm'] > finalArr[i][2]):
        #     diffRpm = finalG[j]['rpm'] - finalArr[i][2]
        # if(finalG[j]['rpm'] == finalArr[i][2]):
        #     diffRpm = 0
        # if(finalArr[i][0] > finalG[j]['torque']):
        #     diffTor = finalArr[i][0] - finalG[j]['torque']
        # if(finalG[j]['torque'] > finalArr[i][0]):
        #     diffTor =  finalG[j]['torque'] - finalArr[i][0]
        # if(finalG[j]['torque'] == finalArr[i][0]):
        #     diffTor = 0

        # totalDiff = diffRpm + diffTor
        # diffTemp.append(diffRpm)
        # diffTemp.append(diffTor)
        # diffTemp.append(totalDiff)
    #print(diffTemp.index(min(diffTemp)))
    #print(finalG[diffTemp.index(min(diffTemp))])

    # finalArr[i].append(finalG[diffTemp.index(min(diffTemp))]['efficiency'])
    #print(finalArr[i])




        # diffTemp.append(finalG[j]['efficiency'])
        # diffTemp.append(finalArr[i][0])
        # diffTemp.append(finalArr[i][2])
        # diffArr.append(diffTemp)
        # for x in range(len(diffArr)):


# print(diffArr)
        

        