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

friction = mass*g*Cr 

##################-- initialisations --########################
speedTimeArr = []
calTorqueArr = []

ds = pd.read_csv('./d1.csv')
speedTime = ds.to_json(orient="records")

finalSpeedtime = json.loads(speedTime)

# print(finalSpeedtime)

#####################-- functions --############################
def calculations():
    for i in range(len(finalSpeedtime)):
        tempAccelerationArr = []
        
        if(int(finalSpeedtime[i]['t(s)']) == 0 & int(finalSpeedtime[i]['v(kmph)'] == 0)):
            acceleration = 0
            aeroForce = 0
            Aforce = 0   ## Aforce is acceleration force
            Nforce = 0   ## Nforce is the net force
            Tw=0         ## where Tw is the wheel torque
            Tf=0         ## Final wheel torque
            motorTorque=0
        else:
            
            t1 = float(finalSpeedtime[i-1]['t(s)'])
            v1 = float(finalSpeedtime[i-1]['v(kmph)'])/3.6 
            t2 =  float(finalSpeedtime[i]['t(s)']) 
            v2 = float(finalSpeedtime[i]['v(kmph)'])/3.6
            
            acceleration = (v2 - v1)/(t2 - t1)
            
            if(acceleration < 0):
                Aforce = 0
                Nforce =0
            else:
                Aforce = mass*acceleration
                Nforce = (Aforce- (friction + aeroForce))
                if(Nforce < 0):
                    Nforce = -(Nforce)
            
            if(v1 < 11.11):
                aeroForce = 0
            else:
                aeroForce = 0.5*row*Cd*Af*v1*v1
                
            Tw = Nforce*Rw  
            
            Tf = Tw + (Tw*(1-Nt))  
            
            motorTorque = Tf / fdr
            
        
        tempAccelerationArr.append(float(finalSpeedtime[i]['t(s)']))
        tempAccelerationArr.append(float(finalSpeedtime[i]['v(kmph)']))
        tempAccelerationArr.append(acceleration)
        tempAccelerationArr.append(friction)
        tempAccelerationArr.append(aeroForce)
        tempAccelerationArr.append(Aforce)
        tempAccelerationArr.append(Nforce)
        tempAccelerationArr.append(Tw)
        tempAccelerationArr.append(Tf)
        tempAccelerationArr.append(round(motorTorque,1))
        speedTimeArr.append(tempAccelerationArr)
        
        calTorqueArr.append(round(motorTorque,1))
        
        
calculations()


# df = pd.DataFrame(speedTimeArr)
# column_names = ["time", "velocity","acceleration","friction","aero force", "Acceleration- force", "net force", "Wheel Torque", "Final Torqe", "motor-torque"]
# df.columns = column_names

# df.to_excel(excel_writer="C: testt.xlsx")  




# print(speedTimeArr[1])