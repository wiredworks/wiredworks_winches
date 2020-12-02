import bpy
import math
import numpy as np
from scipy.integrate import simps
from scipy.integrate import quad
from scipy.optimize import root

class SFX_Calc_Default_Move:
    ''' Calculates Acc, Vel, and Pos Graphs by taking Length, JerkHeight, Proportion of T to t1''' 
    def __init__ (self, Dataobject, length, maxAcc, maxVel ):

        self.Dataobject = Dataobject
        self.Length     = length
        self.accS        = maxAcc
        self.velS       = maxVel
        self.JH         = 10.0 
        if self.Length > 0  and self.accS >0 and self.velS > 0:
            self.Pulses = []       
            (self.T, self.t1, self.JH, self.t2, self.t3) = self.CalcTimes( self.Length, self.JH, self.accS, self.velS)        
            Puls = ( 0, self.t1, self.T, self.t1)
            self.starttime = Puls[0]
            self.endtime   = Puls[0] + Puls[1] +  Puls[2] +  Puls[3]
            
            self.InitCurves()
            self.InitData()
            self.func()
     
                
    def CalcTimes(self, LengthS, JerkHeightS, accS, velS):
        ''' T = 10t 
            acc = (T+t)*JerkHeight
            vel = 2*(T² + 3Tt + 2t²)*JerkHeight
            len = 2*(2t+T)²(t+T)*JerkHeight '''
        JerkHeight = JerkHeightS; t2 = 0; t3 = 0
        
        T = (10.0/11.0)*(accS/JerkHeight)
        t1 = T / 10.0
        if t1 < 0.02 :
            t1 = 0.02
            T  = 10 * t1
            JerkHeight = accS/(T+t1)
            
        acc = JerkHeight*(T+t1)
        vel =  JerkHeight*(T*T + 3*T*t1 + 2*t1*t1 + t2*t2)
        Length = vel*(4*T + 8*t1 + 2*t2 + 2*t3) / 2.0 
                   
        if vel > velS:
            T = math.sqrt((25*velS)/(33*JerkHeight))
            t1 = T / 10.0
            if t1 < 0.02 :
                t1 = 0.02
                T  = 10 * t1
                while t1 <= 0.02 :
                    JerkHeight = JerkHeight/2
                    T = math.sqrt((25*velS)/(33*JerkHeight))
                    t1 = T / 10.0
               
        if vel < velS:
            t2 = (velS-vel)/acc
            
        acc = JerkHeight*(T+t1)
        vel = JerkHeight*(T*T + 3*T*t1 + 2*t1*t1 )+acc*t2
        Length = vel*(4*T + 8*t1 + 2*t2 + 2*t3) / 2.0
        
        if Length > LengthS:
            LengthLambda = lambda x: (2*LengthS-(JerkHeight*(T*T+3*T*t1+2*t1*t1)+acc*x)*(4*T+ 8*t1+ 2*x))
            t2=(root(LengthLambda,[0,]).x[0])               
            if t2 <0:
                t2=0
                T = math.pow((LengthS*125/(396.0 * JerkHeight)),(1/3.0))
                t1 = T / 10.0
                if t1 < 0.02 :
                    t1 = 0.02
                    T  = 10 * t1
                    while t1 <= 0.02 :
                        JerkHeight = JerkHeight/2
                        T = math.pow((LengthS*125/(396.0 * JerkHeight)),(1/3.0))
                        t1 = T / 10.0

        if Length < LengthS:
            try:
                t3 = (LengthS-Length)/vel    
            except ZeroDivisionError:
                print('Zero Division Error')
                t3 = 0
        acc = JerkHeight*(T+t1)                   
        vel = JerkHeight*(T*T + 3*T*t1 + 2*t1*t1 )+acc*t2
        Length = vel*(4*T + 8*t1 + 2*t2 + 2*t3 ) / 2.0#
        Time = 4*T + 8*t1 + 2*t2 +t3 
        
        # print( 'Delta JH: %3.4f Delta Acc: %3.4f Adjusted Vel: %3.4f'%(JerkHeightS-JerkHeight,accS-acc,velS-vel))                            
        # print( '                  With Acc: %3.4f      and Vel: %3.4f ---> Time: %3.4f Length: %3.4f'%(acc , vel, Time, Length))
       
        return (T, t1, JerkHeight, t2, t3)

    def func(self):
        
        # rauf index = 0 
        Puls = ( 0, self.t1, self.T, self.t1, self.t2)         
        self.Pulses.append(Puls)                
        self.Jerk( self.Pulses[0], JH = self.JH)
        # grad index = 1
        Puls1 = (self.Pulses[0][0] + self.Pulses[0][1] + self.Pulses[0][2] + self.Pulses[0][3] , 0.0, self.t2, 0.0)
        self.Pulses.append(Puls1)           
        self.Jerk( self.Pulses[1], JH = 0) 
        self.AppendData(1)
        # runter index = 2
        Puls2 = (self.Pulses[1][0] + self.Pulses[1][1] + self.Pulses[1][2] + self.Pulses[1][3] , self.t1, self.T, self.t1)
        self.Pulses.append(Puls2)             
        self.Jerk( self.Pulses[2], -self.JH) 
        self.AppendData(2)
        # grad index = 3
        Puls3 = (self.Pulses[2][0] + self.Pulses[2][1] + self.Pulses[2][2] + self.Pulses[2][3] , 0, self.t3, 0.0)
        self.Pulses.append(Puls3)             
        self.Jerk( self.Pulses[3], JH = 0) 
        self.AppendData(3)
        # runter index = 4
        Puls4 = (self.Pulses[3][0] + self.Pulses[3][1] + self.Pulses[3][2] + self.Pulses[3][3] , self.t1, self.T, self.t1)
        self.Pulses.append(Puls4)             
        self.Jerk( self.Pulses[4], -self.JH) 
        self.AppendData(4)
        # grad index = 5
        Puls5 = (self.Pulses[4][0] + self.Pulses[4][1] + self.Pulses[4][2] + self.Pulses[4][3] , 0, self.t2, 0.0)
        self.Pulses.append(Puls5)             
        self.Jerk( self.Pulses[5], JH = 0) 
        self.AppendData(5)
        # rauf index = 6
        Puls6 = (self.Pulses[5][0] + self.Pulses[5][1] + self.Pulses[5][2] + self.Pulses[5][3] , self.t1, self.T, self.t1)
        self.Pulses.append(Puls6)             
        self.Jerk( self.Pulses[6], JH = self.JH) 
        self.AppendData(6)        

        self.CalcDraw()

    
    def AppendData(self,i):
        Teilung = 101
        start = self.Pulses[i][0]
        end   = self.Pulses[i][0] + self.Pulses[i][1] +self.Pulses[i][2] +self.Pulses[i][3]
        self.X    = np.append(self.X, np.linspace(start , end, num = Teilung, retstep = False, dtype = np.double))
        self.JrkC = np.append(self.JrkC, np.zeros(Teilung, dtype = np.double))
        self.AccC = np.append(self.AccC, np.zeros(Teilung, dtype = np.double))
        self.VelC = np.append(self.VelC, np.zeros(Teilung, dtype = np.double))
        self.PosC = np.append(self.PosC, np.zeros(Teilung, dtype = np.double))
                
            
        #return [self.maxRuck-self.maxJrk , self.maxGesch-self.maxVel]
    def InitData(self):            
        Teilung = 101
        self.X     = np.linspace(self.starttime , self.endtime, num = Teilung, retstep = False, dtype = np.double)
        self.dX    = self.X[1] - self.X[0]
        self.JrkC  = np.zeros(Teilung, dtype = np.double)
        self.AccC  = np.zeros(Teilung, dtype = np.double)
        self.VelC  = np.zeros(Teilung, dtype = np.double)
        self.PosC  = np.zeros(Teilung, dtype = np.double)
        
    def InitCurves(self):
                
        self.Dataobject['Pos'] = 0
        self.Dataobject['Vel'] = 0
        self.Dataobject['Acc'] = 0
        self.Dataobject['Jrk'] = 0 
        try:
            self.Dataobject.driver_remove('["Jrk"]')
            self.Dataobject.driver_remove('["Acc"]')
            self.Dataobject.driver_remove('["Vel"]')
            self.Dataobject.driver_remove('["Pos"]')
        except:
             pass
        self.Jrkcurve = self.Dataobject.driver_add('["Jrk"]')
        # THX to Philipp Oeser (lichtwerk)
        # to edit the driver fcurve with keyframes, you'll have to remove the fmodifier
        try:
            self.Jrkcurve.modifiers.remove(self.Jrkcurve.modifiers[0])
        except IndexError:
            pass
        self.Acccurve = self.Dataobject.driver_add('["Acc"]')
        try:
            self.Acccurve.modifiers.remove(self.Acccurve.modifiers[0])
        except IndexError:
            pass
        self.Velcurve = self.Dataobject.driver_add('["Vel"]')
        try:
            self.Velcurve.modifiers.remove(self.Velcurve.modifiers[0])
        except IndexError:
            pass
        self.Poscurve = self.Dataobject.driver_add('["Pos"]')
        try:
            self.Poscurve.modifiers.remove(self.Poscurve.modifiers[0])
        except IndexError:
            pass
            
    def CalcDraw(self):
        self.Acccurve.keyframe_points.insert( 0 , 0) 
        for i in range(1, len(self.X)):
            self.JrkC[i] = self.Jrkcurve.evaluate(self.X[i])
            self.AccC[i] = self.AccC[i-1] + self.JrkC[i] * (self.X[i]-self.X[i-1])            
        for i in range(1,len(self.AccC)):
            self.Acccurve.keyframe_points.insert( self.X[i] , self.AccC[i], options ={'FAST'}) 
        for i in range(1, len(self.X)):
            #self.AccC[i] = self.Acccurve.evaluate(self.X[i])
            self.VelC[i] = self.VelC[i-1] + self.AccC[i] * (self.X[i]-self.X[i-1])             
        for i in range(0,len(self.VelC)):
            self.Velcurve.keyframe_points.insert( self.X[i] , self.VelC[i], options ={'FAST'})
            
        for i in range(1, len(self.X)):
            #VelC[i] = Velcurve.evaluate(X[i])
            self.PosC[i] = self.PosC[i-1] + self.VelC[i] * (self.X[i]-self.X[i-1]) 
        for i in range(0,len(self.PosC)):
            self.Poscurve.keyframe_points.insert( self.X[i] , self.PosC[i], options ={'FAST'})
                        
        self.Acccurve.update()
        self.Velcurve.update()
        self.Poscurve.update()        
        
        self.maxJrk = max(abs(self.JrkC))
        self.maxAcc = max(abs(self.AccC))
        self.maxVel = max((self.VelC))
        self.maxPos = max(abs(self.PosC))
        self.maxTime = self.X[-1]
            
    def Jerk(self, Puls, JH):

        Jer0  = 0
        Jer1  = JH
        Jer2  = JH
        Jer3  = 0

        Jert0    = Puls[0]
        Jert1    = Puls[0] +  Puls[1]
        Jert2    = Puls[0] +  Puls[1] +  Puls[2]
        Jert3    = Puls[0] +  Puls[1] +  Puls[2] +  Puls[3]

        self.Jrkcurve.keyframe_points.insert( Jert0 , Jer0)
        self.Jrkcurve.keyframe_points.insert( Jert1 , Jer1)
        self.Jrkcurve.keyframe_points.insert( Jert2 , Jer2)
        self.Jrkcurve.keyframe_points.insert( Jert3 , Jer3)
        
        for i in range(0, len(self.Jrkcurve.keyframe_points)):
            try:
                self.Jrkcurve.keyframe_points[i].handle_left  = (self.Jrkcurve.keyframe_points[i].co[0],self.Jrkcurve.keyframe_points[i].co[1])
                self.Jrkcurve.keyframe_points[i].handle_right = (self.Jrkcurve.keyframe_points[i].co[0],self.Jrkcurve.keyframe_points[i].co[1])  
            except IndexError:
                pass
