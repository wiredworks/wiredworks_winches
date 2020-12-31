#!python

import numpy as np

from scipy.optimize import root
from scipy.interpolate import interp1d
import math

class Calc_Default_Profile:
    def __init__(self, length, maxAcc, maxVel, riseTime, JHeight):
        self.Length        = length
        self.accS          = maxAcc
        self.velS          = maxVel
        self.JH            = JHeight 
        self.Jrk_T_D       = [[],[]]
        self.Acc_T_D       = [[],[]]
        self.Vel_T_D       = [[],[]]
        self.Pos_T_D       = [[],[]]
        self.Vel_P_D       = [[],[]]
        

        if self.Length > 0  and self.accS > 0 and self.velS > 0:
            self.Pulses = []
            (self.T, self.t1, self.JH, self.t2, self.t3, self.time) = self.CalcTimes( self.Length, self.JH, self.accS, self.velS)        
            Puls = ( 0, self.t1, self.T, self.t1)
            self.starttime = Puls[0]
            self.endtime   = Puls[0] + Puls[1] +  Puls[2] +  Puls[3]

            self.InitCurveData()
            self.AssembleFuncData()            
            self.CalcDrawFcurves()

    def GetData(self):
        Jrk = [[],[]]
        Jrk[0] = np.asarray(self.Jrk_T_D[0])
        Jrk[1] = np.asarray(self.Jrk_T_D[1])
        return Jrk, self.Acc_T_D, self.Vel_T_D, self.Pos_T_D, self.Vel_P_D 

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
        
        #print( 'Delta JH: %3.4f Delta Acc: %3.4f Adjusted Vel: %3.4f'%(JerkHeightS-JerkHeight,accS-acc,velS-vel))                            
        #print( '                  With Acc: %3.4f      and Vel: %3.4f ---> Time: %3.4f Length: %3.4f'%(acc , vel, Time, Length))
       
        return (T, t1, JerkHeight, t2, t3, Time)

    def AssembleFuncData(self):
        # rauf index = 0 
        Puls = ( 0, self.t1, self.T, self.t1, self.t2)         
        self.Pulses.append(Puls)                
        self.Jerk( self.Pulses[0], JH = self.JH)
        # grad index = 1
        Puls1 = (self.Pulses[0][0] + self.Pulses[0][1] + self.Pulses[0][2] + self.Pulses[0][3] , 0.0, self.t2, 0.0)
        self.Pulses.append(Puls1)           
        self.Jerk( self.Pulses[1], JH = 0) 
        self.AppendCurveData(1)
        # runter index = 2
        Puls2 = (self.Pulses[1][0] + self.Pulses[1][1] + self.Pulses[1][2] + self.Pulses[1][3] , self.t1, self.T, self.t1)
        self.Pulses.append(Puls2)             
        self.Jerk( self.Pulses[2], -self.JH) 
        self.AppendCurveData(2)
        # grad index = 3
        Puls3 = (self.Pulses[2][0] + self.Pulses[2][1] + self.Pulses[2][2] + self.Pulses[2][3] , 0, self.t3, 0.0)
        self.Pulses.append(Puls3)             
        self.Jerk( self.Pulses[3], JH = 0) 
        self.AppendCurveData(3)
        # runter index = 4
        Puls4 = (self.Pulses[3][0] + self.Pulses[3][1] + self.Pulses[3][2] + self.Pulses[3][3] , self.t1, self.T, self.t1)
        self.Pulses.append(Puls4)             
        self.Jerk( self.Pulses[4], -self.JH) 
        self.AppendCurveData(4)
        # grad index = 5
        Puls5 = (self.Pulses[4][0] + self.Pulses[4][1] + self.Pulses[4][2] + self.Pulses[4][3] , 0, self.t2, 0.0)
        self.Pulses.append(Puls5)             
        self.Jerk( self.Pulses[5], JH = 0) 
        self.AppendCurveData(5)
        # rauf index = 6
        Puls6 = (self.Pulses[5][0] + self.Pulses[5][1] + self.Pulses[5][2] + self.Pulses[5][3] , self.t1, self.T, self.t1)
        self.Pulses.append(Puls6)             
        self.Jerk( self.Pulses[6], JH = self.JH) 
        self.AppendCurveData(6)

    def InitCurveData(self):
        Teilung = 501
        self.X     = np.linspace(self.starttime , self.endtime, num = Teilung, retstep = False, dtype = np.double)
        self.dX    = self.X[1] - self.X[0]
        self.JrkC  = np.zeros(Teilung, dtype = np.double)
        self.AccC  = np.zeros(Teilung, dtype = np.double)
        self.VelC  = np.zeros(Teilung, dtype = np.double)
        self.PosC  = np.zeros(Teilung, dtype = np.double) 

    def AppendCurveData(self,i):
        Teilung = 501
        start = self.Pulses[i][0]
        end   = self.Pulses[i][0] + self.Pulses[i][1] +self.Pulses[i][2] +self.Pulses[i][3]
        self.X    = np.append(self.X, np.linspace(start , end, num = Teilung, retstep = False, dtype = np.double))
        self.JrkC = np.append(self.JrkC, np.zeros(Teilung, dtype = np.double))
        self.AccC = np.append(self.AccC, np.zeros(Teilung, dtype = np.double))
        self.VelC = np.append(self.VelC, np.zeros(Teilung, dtype = np.double))
        self.PosC = np.append(self.PosC, np.zeros(Teilung, dtype = np.double))   
            
    def interp_Jerk(self,x):
        f = interp1d(self.Jrk_T_D[0],self.Jrk_T_D[1], kind ='linear')
        return f(x)

    def CalcDrawFcurves(self):
        self.Acc_T_D[0].append( 0.0 )
        self.Acc_T_D[1].append( 0.0 )
        for i in range(1, len(self.X)):
            self.Acc_T_D[0].append( self.X[i])
            self.JrkC[i] = self.interp_Jerk(self.X[i])
            self.Acc_T_D[1].append( self.Acc_T_D[1][-1] + self.JrkC[i] * (self.X[i]-self.X[i-1]))

        self.Vel_T_D[0].append( 0.0 )
        self.Vel_T_D[1].append( 0.0 )
        for i in range(1, len(self.X)):
            self.Vel_T_D[0].append( self.X[i] )
            self.Vel_T_D[1].append( self.Vel_T_D[1][-1] + self.Acc_T_D[1][i] * (self.X[i]-self.X[i-1]))
  
        self.Pos_T_D[0].append( 0.0 )
        self.Pos_T_D[1].append( 0.0 )
        for i in range(1, len(self.X)):
            self.Pos_T_D[0].append( self.X[i] )
            self.Pos_T_D[1].append( self.Pos_T_D[1][-1] + self.Vel_T_D[1][i] * (self.X[i]-self.X[i-1]))

        self.Acc_T_D[0] = np.array(self.Acc_T_D[0])
        self.Acc_T_D[1] = np.array(self.Acc_T_D[1])

        self.Vel_T_D[0] = np.array(self.Vel_T_D[0])
        self.Vel_T_D[1] = np.array(self.Vel_T_D[1])

        self.Pos_T_D[0] = np.array(self.Pos_T_D[0])
        self.Pos_T_D[1] = np.array(self.Pos_T_D[1])

        t = [[],[]]
        for i in range(0,len(self.X)):
            v = self.eval_Vel_T_D(self.X[i]).tolist()
            p = self.eval_Pos_T_D(self.X[i]).tolist()
            t[0].append(p)
            t[1].append(v)
        self.Vel_P_D[0]= np.asarray(t[0])
        self.Vel_P_D[1]= np.asarray(t[1])

    def eval_Vel_T_D(self, x):
        f = interp1d(self.Vel_T_D[0], self.Vel_T_D[1])
        return f(x)

    def eval_Pos_T_D(self, x):
        f = interp1d(self.Pos_T_D[0], self.Pos_T_D[1])
        return f(x)

    def Jerk(self, Puls, JH):
        '''Append Jerk Times and Heights to self.JerkD'''
        Jer0  = 0
        Jer1  = JH
        Jer2  = JH
        Jer3  = 0

        Jert0    = Puls[0]
        Jert1    = Puls[0] +  Puls[1]
        Jert2    = Puls[0] +  Puls[1] +  Puls[2]
        Jert3    = Puls[0] +  Puls[1] +  Puls[2] +  Puls[3]

        self.Jrk_T_D[0].append(Jert0)
        self.Jrk_T_D[1].append(Jer0)
        self.Jrk_T_D[0].append(Jert1)
        self.Jrk_T_D[1].append(Jer1)
        self.Jrk_T_D[0].append(Jert2)
        self.Jrk_T_D[1].append(Jer2)
        self.Jrk_T_D[0].append(Jert3)
        self.Jrk_T_D[1].append(Jer3)