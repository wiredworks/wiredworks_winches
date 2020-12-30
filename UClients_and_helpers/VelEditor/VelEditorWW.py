import wx
from wx import xrc
import sys

import numpy as np
import matplotlib

#import matplotlib.pyplot as plt
import mpl_toolkits.axisartist as AA

from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
#from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg, wxc
from scipy.interpolate import splev, splrep, splint, interp1d, BPoly, splprep
from scipy.integrate import quad,simps
from scipy.optimize import root

from simplification.cutil import simplify_coords_idx

import math
from math import copysign

import time
import os
import copy

import pickle
import json

#import inspect
# curframe = inspect.currentframe()
# calframe = inspect.getouterframes(curframe, 2)
# print('caller name:', calframe[1][3])

ID_Menu_OpenVelFile = 5005
ID_Menu_SaveVelFile = 5006
ID_Menu_Exit        = 5008
ID_Menu             = 5011

class Simplify:
    def __init__(self):
        pass

    def main(self, Kurve, Ableitung, error):
        splineVerts = []
        for i in range(0, len(Kurve[0])):
            splineVerts.append(np.array([Kurve[0][i],Kurve[1][i]]))

        newVerts = self.Visvalingam(splineVerts, error)

        X_Values  = np.zeros(len(newVerts))
        Y_Values  = np.zeros(len(newVerts))
        k_Values  = np.zeros(len(newVerts))

        for i in range(0,len(newVerts)):
            X_Values[i]  = Kurve[0][newVerts[i]]
            Y_Values[i]  = Kurve[1][newVerts[i]]
            k_Values[i]  = Ableitung[1][newVerts[i]]
        return [X_Values, Y_Values, k_Values]

    def Visvalingam(self,splineVerts, error):
        return simplify_coords_idx(splineVerts, 0.01)

class Calc_Default_Profile:
    def __init__(self, length, maxAcc, maxVel):
        self.Length        = length
        self.accS          = maxAcc
        self.velS          = maxVel
        self.JH            = 10.0 
        self.Jrk_T_D       = [[],[]]
        self.Acc_T_D       = [[],[]]
        self.Vel_T_D       = [[],[]]
        self.Pos_T_D       = [[],[]]
        self.Vel_P_D       = [[],[]]
        

        if self.Length > 0  and self.accS > 0 and self.velS > 0:
            self.Pulses = []
            self.JH = 10.0      
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

class Diagramm(wx.Panel):
    def __init__(self, parent,id= 1,dpi=None, **kwargs):
        wx.Panel.__init__(self, parent,id= 1, **kwargs)
        self.clickpoint = [0,0]
        self.hpoint=0
        self.parent = parent
        self.figure = Figure(figsize=(12, 36))
        self.dpi    = self.figure.get_dpi()
        self.figure.subplots_adjust(left=0.05,right=0.95,bottom=0.05,top=0.95,wspace=0.1,hspace=0.1)
        # with axisartist 
        self.axes   = AA.Subplot(self.figure,2,1,1)
        self.axesT  = AA.Subplot(self.figure,2,1,2)
        self.figure.add_subplot(self.axes)
        self.figure.add_subplot(self.axesT)
        self.PrepareAxes()
        
        self.canvas = FigureCanvas(self,-1,self.figure)
        self.canvas.callbacks.connect('button_press_event',   self.OnMouseDown)
        self.canvas.callbacks.connect('motion_notify_event',  self.OnMouseMotion)
        self.canvas.callbacks.connect('button_release_event', self.OnMouseUp)
        self.canvas.callbacks.connect('key_press_event',      self.OnKeyPress)
        self.canvas.callbacks.connect('key_release_event',    self.OnKeyRelease)
        self.canvas.callbacks.connect('scroll_event',         self.OnScroll)
        
        self.sizer  = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas,1, wx.LEFT | wx.TOP | wx.GROW)
        self.SetSizer(self.sizer)        
        self.Fit()
        
        self.Bind(wx.EVT_PAINT,self.OnPaint)        
        self.Bind(wx.EVT_SIZE,self.OnSize)
        self.InitVars()

    def PrepareAxes(self):
        # make some axis invisible
        #self.axes.set_xlim(-0.5,18.5)
        ## make an new axis along the first axis axis (x-axis) which pass  through y=0.
        #self.axes.axis["0"] = self.axes.new_floating_axis(nth_coord=0, value=0, axis_direction="bottom")
        #self.axes.axis["0"].toggle(all=True)
        #self.axes.axis["0"].major_ticklabels.set_fontsize(8)
        #self.axes.axis["0"].minor_ticklabels.set_fontsize(8)        
        #self.axes.axis["0"].major_ticks.set_color("white")
        #self.axes.axis["0"].minor_ticks.set_color("white")
        #self.axes.axis["0"].line.set_color("white")       
      
        self.axes.axis["bottom", "left", "top", "right"].major_ticklabels.set_fontsize(8)
        self.axes.axis["bottom", "left", "top", "right"].minor_ticklabels.set_fontsize(8)
        self.axes.axis["bottom", "left", "top", "right"].major_ticks.set_color("white")
        self.axes.axis["bottom", "left", "top", "right"].minor_ticks.set_color("white")        
        self.axes.axis["bottom", "left", "top", "right"].line.set_color("white")       
        self.axes.axis["bottom", "left", "top", "right"].major_ticks.set_color("white")
        self.axes.axis["bottom", "left", "top", "right"].minor_ticks.set_color("white")
        #self.axes.axis["bottom", "left"].label.set_color("darkgray")
        
        #self.axesT.axis["0"] = self.axes.new_floating_axis(nth_coord=0, value=0, axis_direction="bottom")
        #self.axesT.axis["0"].toggle(all=True)
        #self.axesT.axis["0"].major_ticklabels.set_fontsize(8)
        #self.axesT.axis["0"].minor_ticklabels.set_fontsize(8)        
        #self.axesT.axis["0"].major_ticks.set_color("white")
        #self.axesT.axis["0"].minor_ticks.set_color("white")
        #self.axesT.axis["0"].line.set_color("white") 
              
        #self.axesT.set_xlim(-0.5,18.5)
        self.axesT.axis["bottom", "left", "top", "right"].major_ticklabels.set_fontsize(8)
        self.axesT.axis["bottom", "left", "top", "right"].minor_ticklabels.set_fontsize(8)
        self.axesT.axis["bottom", "left", "top", "right"].major_ticks.set_color("white")
        self.axesT.axis["bottom", "left", "top", "right"].minor_ticks.set_color("white")        
        self.axesT.axis["bottom", "left", "top", "right"].line.set_color("white")       
        self.axesT.axis["bottom", "left", "top", "right"].major_ticks.set_color("white")
        self.axesT.axis["bottom", "left", "top", "right"].minor_ticks.set_color("white")
        #self.axesT.axis["bottom", "left"].label.set_color("darkgray")        

        rect        = self.figure.patch
        rect.set_facecolor('darkgrey')
        rect        = self.axes.patch
        rect.set_facecolor('darkgrey')
        rect        = self.axesT.patch
        rect.set_facecolor('darkgrey')        
        
        self.axes.grid(True,color = 'white', zorder= 0)
        self.axesT.grid(True,color = 'white', zorder= 0)

    def InitVars(self):
        pass
        self.VelEditorFrame = self.GetGrandParent().GetGrandParent().GetParent()
        self.MouseDeltaYPoint = 0.0
        self.modifyP          = 'none' 
        
        self.xzoom = True
        self.yzoom = True 
        
        self.mousezoom = False
        self.rezoom = False
        
        self.press = None
        self.cur_xlim = None
        self.cur_ylim = None
        self.x0 = None
        self.y0 = None
        self.x1 = None
        self.y1 = None
        self.xpress = None
        self.ypress = None 
        
        self.pressT = None
        self.cur_xlimT = None
        self.cur_ylimT = None
        self.x0T = None
        self.y0T = None
        self.x1T = None
        self.y1T = None
        self.xpressT = None
        self.ypressT = None 
        self.scaleP = 1
        self.scaleT = 1         
        
        self.TTPoints   = []
        self.TPPoints   = []
        self.fillP      = []
        self.fillT      = []
        
        self.PosSkalierung2 = 1.

        self.Action_ID          = 0
        self.Action_Name        = ''
        self.Action_Saved       = False
        self.Action_Path        = ''
        self.Action_MinPos      = 0.0
        self.Action_MaxPos      = 0.0
        self.Action_MaxAcc      = 0.0
        self.Action_MaxVel      = 0.0
        self.Action_Length      = 0.0
        self.Action_Jrk              = [[],[]]
        self.Action_Acc              = [[],[]]
        self.Action_Vel              = [[],[]]
        self.Action_Pos              = [[],[]]
        self.Action_VelInPos         = [[],[]]
        self.Jrk_T_D_L        = [[],[]]
        self.Acc_T_D_L        = [[],[]]
        self.Vel_T_D_L        = [[],[]]
        self.Pos_T_D_L        = [[],[]]
        self.Vel_P_D_L        = [[],[]]
        self.Jrk_T_D          = [[],[]]
        self.Acc_T_D          = [[],[]]
        self.Vel_T_D          = [[],[]]
        self.Pos_T_D          = [[],[]]
        self.Vel_P_D          = [[],[]]
        self.CP_T_Points      = [[],[],[]]
        self.CP_M_Points      = [[],[],[]]
        self.CP_P_Points      = [[],[],[]]
        self.Vel_Conv_Points  = [[],[],[]]
        self.Vel_Conv         = [[],[]]
        self.intAcc_Conv      = [[],[]]
        self.intVel_Conv      = [[],[]]

        self.Acc_Conv         = [[],[]]

        self.Action_Description      = ''
        self.Action_Signed           = False

        self.PrepareGraphs()

    def ClearVarsEntryUnsigned(self):
        ''' Clear Variables'''
        self.CP_P_Points_Limit = [[],[],[]] # Limit Control Points In Pos Domain   [[x-Values],[y-Values],[tangent]]
        self.CP_P_Points       = [[],[],[]] # Control Points In Pos Domain         [[x-Values],[y-Values],[tangent]]
        self.CP_T_Points       = [[],[],[]] # Control Points In Time Domain        [[x-Values],[y-Values],[tangent]]
        self.CP_M_Points       = [[],[],[]] # Control points Master InTime         [[x-Values],[y-Values],[tangent]]
        self.CP_T_Points_Limit = [[],[],[]] # Limit Control Points In Time Domain  [[x-Values],[y-Values],[tangent]]
        
        self.Vel_P_Limit       = [[],[]]
        self.Vel_P             = [[],[]]
        self.Acc_T             = [[],[]]
        self.Vel_T             = [[],[]]
        self.Vel_T_Limit       = [[],[]]

        self.Jrk_T_D_L   = [[],[]]
        self.Acc_T_D_L   = [[],[]]
        self.Vel_T_D_L   = [[],[]]
        self.Pos_T_D_L   = [[],[]]
        self.Vel_P_D_L   = [[],[]]

        self.TimeScaling    =1.0
        self.TimeScalingAbs =1.0
        try:
            for i in range(len(self.VelInTime_markers)):
                self.axesT.lines.remove(self.VelInTime_markers[i])
                self.axesT.lines.remove(self.VelInTime_tangents[i])
            for i in range (len(self.fillT)):
                self.axesT.patches.remove(self.fillT[i])
            for i in range(len(self.VelInPos_markers)):
                self.axes.lines.remove(self.VelInPos_markers[i])
                #self.axes.lines.remove(self.VelInPos_tangents[i])
            for i in range (len(self.fillP)):
                self.axes.patches.remove(self.fillP[i])
            for i in range (len(self.fillT)):
                self.axesT.patches.remove(self.fillT[i])
        except :#AttributeError:
            pass

        self.fillP              = []
        self.fillT              = [] 
        self.VelInPos_markers   = []
        self.VelInPos_tangents  = []
        self.VelInTime_markers  = []
        self.VelInTime_tangents = []
        self.Vel_Conv_markers   = []   

    def ClearVarsEntrySigned(self):
        ''' Clear Variables'''

        self.Vel_P_Limit       = [[],[]]
        self.Vel_P             = [[],[]]
        self.Acc_T             = [[],[]]
        self.Vel_T             = [[],[]]
        self.Vel_T_Limit       = [[],[]]

        try:
            for i in range(len(self.VelInTime_markers)):
                self.axesT.lines.remove(self.VelInTime_markers[i])
                self.axesT.lines.remove(self.VelInTime_tangents[i])
            for i in range (len(self.fillT)):
                self.axesT.patches.remove(self.fillT[i])
            for i in range(len(self.VelInPos_markers)):
                self.axes.lines.remove(self.VelInPos_markers[i])
                #self.axes.lines.remove(self.VelInPos_tangents[i])
            for i in range (len(self.fillP)):
                self.axes.patches.remove(self.fillP[i])
            for i in range (len(self.fillT)):
                self.axesT.patches.remove(self.fillT[i])
        except :#AttributeError:
            pass

        self.fillP              = []
        self.fillT              = [] 
        self.VelInPos_markers   = []
        self.VelInPos_tangents  = []
        self.VelInTime_markers  = []
        self.VelInTime_tangents = []
        self.Vel_Conv_markers   = []

    def ClearVarsGenerate(self):
        ''' Clear Variables'''
        self.CP_P_Points_Limit = [[],[],[]] # Limit Control Points In Pos Domain   [[x-Values],[y-Values],[tangent]]
        self.CP_P_Points       = [[],[],[]] # Control Points In Pos Domain         [[x-Values],[y-Values],[tangent]]
        self.CP_T_Points       = [[],[],[]] # Control Points In Time Domain        [[x-Values],[y-Values],[tangent]]
        self.CP_M_Points       = [[],[],[]] # Control points Master InTime         [[x-Values],[y-Values],[tangent]]
        self.CP_T_Points_Limit = [[],[],[]] # Limit Control Points In Time Domain  [[x-Values],[y-Values],[tangent]]
        
        self.Vel_P_Limit       = [[],[]]
        self.Vel_P             = [[],[]]
        self.Acc_T             = [[],[]]
        self.Vel_T             = [[],[]]
        self.Vel_T_Limit       = [[],[]]

        self.Jrk_T_D   = [[],[]]
        self.Acc_T_D   = [[],[]]
        self.Vel_T_D   = [[],[]]
        self.Pos_T_D   = [[],[]]
        self.Vel_P_D   = [[],[]]

        self.TimeScaling    =1.0
        self.TimeScalingAbs =1.0
        try:
            for i in range(len(self.VelInTime_markers)):
                self.axesT.lines.remove(self.VelInTime_markers[i])
                #Set to Comment as Smoothing makes Tangent Editing obsolete
                #self.axesT.lines.remove(self.VelInTime_tangents[i])
            for i in range (len(self.fillT)):
                self.axesT.patches.remove(self.fillT[i])
            for i in range(len(self.VelInPos_markers)):
                self.axes.lines.remove(self.VelInPos_markers[i])
                #self.axes.lines.remove(self.VelInPos_tangents[i])
            for i in range (len(self.fillP)):
                self.axes.patches.remove(self.fillP[i])
            for i in range (len(self.fillT)):
                self.axesT.patches.remove(self.fillT[i])
        except :#AttributeError:
            pass

        self.fillP              = []
        self.fillT              = [] 
        self.VelInPos_markers   = []
        self.VelInPos_tangents  = []
        self.VelInTime_markers  = []
        self.VelInTime_tangents = []

    def Entry(self):
        ''' Setup of Controlpoints and the BPolys'''
                
        self.VelEditorFrame.btnGenerate.Enable(True)
        Vel_T_D_S_09 =[[],[],[]]
        self.Length = float(self.VelEditorFrame.txtUsrLength.GetValue())        
        self.Time_Pos_Values      = np.zeros(1000)

        if not(self.Action_Signed):
            self.ClearVarsEntryUnsigned()
            self.Jrk_T_D_L,\
            self.Acc_T_D_L,\
            self.Vel_T_D_L,\
            self.Pos_T_D_L,\
            self.Vel_P_D_L   = self.Calc_Profile(float(self.VelEditorFrame.txtSetupLength.GetValue()),\
                                               float(self.VelEditorFrame.txtSetupMaxAcc.GetValue()),\
                                               float(self.VelEditorFrame.txtSetupMaxVel.GetValue()))

            self.Samples = len(self.Vel_T_D_L[0])
            self.X_Time_Values         = np.linspace(0., self.Vel_T_D_L[0][-1],  self.Samples, dtype= np.double)
            self.X_Pos_Values          = np.linspace(0., self.Length,            self.Samples, dtype= np.double)

            Vel_T_D_S = self.SimplifyProfile(self.Vel_T_D_L,self.Acc_T_D_L, 0.01)

            self.VelEditorFrame.txtSetupTime.SetValue(str(Vel_T_D_S[0][-1]))
            
            Vel_T_D_S_09[0] = Vel_T_D_S[0]
            Vel_T_D_S_09[1] = Vel_T_D_S[1]*(self.Action_UsrVel/self.Action_MaxVel)
            Vel_T_D_S_09[2] = Vel_T_D_S[2]*(self.Action_UsrVel/self.Action_MaxVel)**2.0

            
            self.Jrk_T_D = self.Jrk_T_D_L
            self.Acc_T_D = self.Acc_T_D_L
            self.Vel_T_D = self.Vel_T_D_L
            self.Pos_T_D = self.Pos_T_D_L
            self.Vel_P_D = self.Vel_P_D_L

            self.init_CP_T_Points(Vel_T_D_S_09)
            self.init_T_BPoly()

            self.Vel_T[0] = self.X_Time_Values
            self.Vel_T[1] = self.eval_CP_T_Points(self.X_Time_Values,True)

            self.init_CP_P_Points(Vel_T_D_S_09)            
            self.init_P_BPoly()

            self.Vel_Conv_Points[0] = copy.copy(self.CP_M_Points[0]) 
            self.Vel_Conv_Points[1] = copy.copy(self.CP_M_Points[1])
            self.Vel_Conv_Points[2] = copy.copy(self.CP_M_Points[2])  

            self.RecalcMove(init = True)
        else:
            print('Signed File')
            self.ClearVarsEntrySigned()

            self.Samples = len(self.Vel_T_D_L[0])
            self.X_Time_Values         = np.linspace(0., self.CP_T_Points[0][-1] ,  self.Samples, dtype= np.double)
            self.X_Pos_Values          = np.linspace(0., self.Length,            self.Samples, dtype= np.double)

            self.init_T_BPoly()            

            self.Vel_T[0] = self.X_Time_Values
            self.Vel_T[1] = self.eval_CP_T_Points(self.X_Time_Values,True)

            self.init_P_BPoly()

            self.Vel_P_Limit = self.Vel_P_D

            self.Vel_Conv_Points[0] = copy.copy(self.CP_M_Points[0]) 
            self.Vel_Conv_Points[1] = copy.copy(self.CP_M_Points[1])
            self.Vel_Conv_Points[2] = copy.copy(self.CP_M_Points[2])  
           
            self.RecalcMove(init = False)
        
        self.rezoom          = True
        self.Plot(init       = True)

    def GenerateProfile(self,Length, Acc, Vel):
        self.Action_Signed      = False
        self.ClearVarsGenerate()
        self.canvas.draw()

        self.VelEditorFrame.chkSmoothing.SetValue(False)
        self.VelEditorFrame.chkSmoothingII.SetValue(False)

        self.Length = float(self.VelEditorFrame.txtUsrLength.GetValue())        
        self.Time_Pos_Values      = np.zeros(1000)

        self.Jrk_T_D,\
        self.Acc_T_D,\
        self.Vel_T_D,\
        self.Pos_T_D,\
        self.Vel_P_D   = self.Calc_Profile(Length, Acc, Vel)

        self.Samples = len(self.Vel_T_D[0])
        self.X_Time_Values         = np.linspace(0., self.Vel_T_D[0][-1],  self.Samples, dtype= np.double)
        self.X_Pos_Values          = np.linspace(0., self.Length,          self.Samples, dtype= np.double)

        Vel_T_D_S = self.SimplifyProfile(self.Vel_T_D,self.Acc_T_D, 0.01)

        self.init_CP_T_Points(Vel_T_D_S)
        self.init_T_BPoly()

        self.Vel_T[0] = self.X_Time_Values
        self.Vel_T[1] = self.eval_CP_T_Points(self.X_Time_Values,True)

        self.init_CP_P_Points(Vel_T_D_S)            
        self.init_P_BPoly()

        self.Vel_Conv_Points[0] = copy.copy(self.CP_M_Points[0]) 
        self.Vel_Conv_Points[1] = copy.copy(self.CP_M_Points[1])
        self.Vel_Conv_Points[2] = copy.copy(self.CP_M_Points[2])

        self.RecalcMove(init = True)

        if self.VelEditorFrame.chkSmoothing.GetValue() == False:
            self.Smooth()
        if self.VelEditorFrame.chkSmoothingII.GetValue() == False:
            self.SmoothII()

        self.Refresh()
        self.rezoom          = True
        self.Plot(init       = True)

    def Calc_Profile(self,Length, Acc, Vel):   
        A = Calc_Default_Profile(Length, Acc, Vel)
        Jrk, Acc, Vel, Pos,Pos_P = A.GetData()
        return Jrk, Acc, Vel, Pos,Pos_P

    def SimplifyProfile(self,Profile, Ableitung, error):
        B = Simplify()
        Profile_S = B.main(Profile, Ableitung, error)
        return Profile_S
       
    def T_2_P(self, x):
        f=interp1d( self.Pos_T_D[0] * self.TimeScalingAbs, self.Pos_T_D[1], kind ='slinear',bounds_error=False, fill_value=np.nan)
        return f(x)

    def P_2_T(self, x):
        f=interp1d(self.Pos_T_D[1],self.Pos_T_D[0]* self.TimeScalingAbs, kind ='slinear',bounds_error=False, fill_value=np.nan)
        return f(x)

    def init_CP_P_Points(self, P_Points):
        '''Init the Controlpoints in P-Domain'''
        self.CP_P_Points = self.init_CP_P(P_Points[0],P_Points[1]* 0.9)

    def init_CP_P(self, X_Values, Y_Values):
        ''' Init Limits in P-Domain'''
        CP_P_Points = [[],[],[]]
        if not(self.Action_Signed):
            CP_P_Points[0] = self.T_2_P(copy.copy(X_Values))
        else:
            CP_P_Points[0] = copy.copy(X_Values)
        CP_P_Points[1] = copy.copy(Y_Values)
        k = (CP_P_Points[1][1]-CP_P_Points[1][0])/(CP_P_Points[0][1]-CP_P_Points[0][0])
        CP_P_Points[2].append(k)    
        for i in range (1,len(CP_P_Points[0])):
            k= (CP_P_Points[1][i]-CP_P_Points[1][i-1])/(CP_P_Points[0][i]-CP_P_Points[0][i-1])
            CP_P_Points[2].append(k)
        return [CP_P_Points[0], CP_P_Points[1], CP_P_Points[2]]

    def init_P_BPoly(self):
        ''' Init BPolys in P-Domain'''
        y  = self.eval_CP_P_Points(0.1,True)

    def init_CP_T_Points(self, T_Points):
        '''Init Controlpoints in T-Domain'''
        self.CP_T_Points       = self.init_CP_T(T_Points[0], T_Points[1], T_Points[2])
        self.CP_M_Points       = self.init_CP_T(T_Points[0], T_Points[1], T_Points[2])

    def init_CP_T(self, X_Values, Y_Values, k_Values):
        ''' Init Master Controlpoint in T-Domain'''
        CP_T_Points =[[],[],[],[]]
        if not(self.Action_Signed): 
            CP_T_Points[0]       = copy.copy(X_Values)
        else:
            CP_T_Points[0]       = self.P_2_T(copy.copy(X_Values))
        CP_T_Points[1]       = copy.copy(Y_Values)
        CP_T_Points[2]       = copy.copy(k_Values)

        return [CP_T_Points[0], CP_T_Points[1], CP_T_Points[2]]

    def init_T_BPoly(self):
        '''Init BPolys in T-Domain'''
        v  = self.eval_CP_T_Points(0.1,True)
        w  = self.eval_CP_M_Points(0.1,True)

    def eval_Grenz_P_Points(self,x,refresh):
        f=interp1d(self.Vel_P_Limit[0],self.Vel_P_Limit[1], kind ='slinear',bounds_error=False, fill_value=np.nan)
        return f(x)

    def eval_CP_P_Points(self,x,refresh):
        if refresh == True:
            xC = self.T_2_P(self.X_Time_Values)
            yC = self.Vel_T[1]
            self.eval_CP_P=interp1d(xC,yC, kind ='slinear',bounds_error=False, fill_value=np.nan)
        return self.eval_CP_P(x)
     
    def eval_CP_M_Points(self,x,refresh):
        '''BPoly for MasterVel in T-Domain'''
        if refresh == True:
            yi = [[self.CP_M_Points[1][0],self.CP_M_Points[2][0]]]
            for i in range(1,len(self.CP_M_Points[0])):
                yi.append([self.CP_M_Points[1][i],self.CP_M_Points[2][i]])
            order = 3
            self.CP_M_BPoly = BPoly.from_derivatives(self.CP_M_Points[0],yi,orders = order)
        return self.CP_M_BPoly(x)

    def eval_PosToTime_Line(self,x):
        '''P-Domain (PosValues) to T-Domain (TimeValues) Interpolation
           x-Axis: Positions in P-Domain; y-Axis: Integral of Vel over Pos '''
        f=interp1d(self.X_Pos_Values,self.Time_Pos_Values, kind ='slinear',bounds_error=False, fill_value=np.nan)
        return f(x)

    def eval_CP_T_Points(self,x,refresh):
        '''BPoly für Vel in T-Domain'''
        if refresh:
            yi = [[self.CP_T_Points[1][0],self.CP_T_Points[2][0]]]
            for i in range(1,len(self.CP_T_Points[0])):
                yi.append([self.CP_T_Points[1][i],self.CP_T_Points[2][i]])
            order = 3
            self.CP_T_BPoly =BPoly.from_derivatives(self.CP_T_Points[0],yi,orders = order)
        return self.CP_T_BPoly(x)

    def eval_Grenz_T_Points(self, x):
        f=interp1d(self.Vel_T_Limit[0],self.Vel_T_Limit[1], kind ='slinear',bounds_error=False, fill_value=np.nan)
        return f(x)
    
    def PrepareGraphs(self): 
        self.axes.clear()
        self.axesT.clear()
        self.PrepareAxes()
        self._xInit           = np.linspace(0., 1000. , 1001)
        self.Null             = np.zeros(len(self._xInit))
        self.lines = []
        self.lines += self.axes.plot(self._xInit,self.Null, color = "black",              linewidth = 0.5,  linestyle = "-.",       pickradius = 0) # Vel_P_limit  [0]
        self.lines += self.axes.plot(self._xInit,self.Null, color = "darkred",            linewidth = 1.0,  linestyle = "-",        pickradius = 0) # Vel_P        [1]
        self.lines += self.axes.plot(self._xInit,self.Null, color = "black",              linewidth = 1.0,  linestyle = "-.",       pickradius = 0) # Vel_P_D_L    [2]
      # self.lines += self.axes.plot(self._xInit,self.Null, color = "darkgreen",          linewidth = 1.0,  linestyle = "-",        pickradius = 0)
      # self.lines += self.axes.plot(self._xInit,self.Null, color = "darkblue",           linewidth = 1.0,  linestyle = "-.",       pickradius = 0)
      # self.lines += self.axes.plot(self._xInit,self.Null, color = "darkred",            linewidth = 1.4,  linestyle = "-",        pickradius = 0)
      # self.lines += self.axes.plot(self._xInit,self.Null, color = "darkgreen",          linewidth = 1.4,  linestyle = "-",        pickradius = 0)
      # self.lines += self.axes.plot(self._xInit,self.Null, color = "darkblue",           linewidth = 1.4,  linestyle = "-",        pickradius = 0)
      # self.lines += self.axes.plot(self._xInit,self.Null, color = "xkcd:grass green",   linewidth = 1.4,  linestyle = "--",       pickradius = 0)
      # self.lines += self.axes.plot(self._xInit,self.Null, color = "xkcd:kelly green",   linewidth = 1.4,  linestyle = "--",       pickradius = 0)
      # self.lines += self.axes.plot(self._xInit,self.Null, color = "black",              linewidth = 1.4,  linestyle = "-",        pickradius = 0)
      # self.lines += self.axes.plot(self._xInit,self.Null, color = "black",              linewidth = 1.4,  linestyle = "-.",       pickradius = 0)
      # self.lines += self.axes.plot(self._xInit,self.Null, color = "yellow",             linewidth = 0.4,  linestyle = "-",        pickradius = 0)
      # self.lines += self.axes.plot(self._xInit,self.Null, color = "green",              linewidth = 0.4,  linestyle = "-",        pickradius = 0
      # self.lines += self.axes.plot(self._xInit,self.Null, color = "blue",               linewidth = 0.4,  linestyle = "-",        pickradius = 0)        
        self.linesT = []
        self.linesT += self.axesT.plot(self._xInit,self.Null,  color = "black",           linewidth = 1.0,  linestyle = "-.",       pickradius = 0) # Vel_T_limit [0]
        self.linesT += self.axesT.plot(self._xInit,self.Null,  color = "darkred",         linewidth = 1.0,  linestyle = "-",        pickradius = 0) # Vel_T       [1]
        self.linesT += self.axesT.plot(self._xInit,self.Null,  color = "darkblue",        linewidth = 0.5,  linestyle = "-.",       pickradius = 0) # Acc_T       [2]    
        self.linesT += self.axesT.plot(self._xInit,self.Null,  color = "darkblue",        linewidth = 0.5,  linestyle = "-.",       pickradius = 0) # Acc_T_D_L   [3]
        self.linesT += self.axesT.plot(self._xInit,self.Null,  color = "black",           linewidth = 0.5,  linestyle = "-.",       pickradius = 0) # Vel_T_D_L   [4]       
        self.linesT += self.axesT.plot(self._xInit,self.Null,  color = "darkblue",        linewidth = 0.5,  linestyle = "-",        pickradius = 0) # Acc_Conv    [5]
        self.linesT += self.axesT.plot(self._xInit,self.Null,  color = "darkred",         linewidth = 0.5,  linestyle = "--",       pickradius = 0) # Vel_Conv    [6]
        self.linesT += self.axesT.plot(self._xInit,self.Null,  color = "m",               linewidth = 0.8,  linestyle = "-",        pickradius = 0)
     #  self.linesT += self.axesT.plot(self._xInit,self.Null,  color = "darkgreen",       linewidth = 0.5,  linestyle = "-.",       pickradius = 0)

    def Plot(self, init = True):        
        #self.rezoom = True

        self.lines[0].set( xdata = self.Vel_P_D_L[0],      ydata=self.Vel_P_D_L[1])
        self.lines[1].set( xdata = self.Vel_P[0],          ydata=self.Vel_P[1])
        self.lines[2].set( xdata = self.Vel_P_Limit[0],    ydata=self.Vel_P_Limit[1])  
 
        for i in range (len(self.fillP)):
            self.axes.patches.remove(self.fillP[i])
        self.fillP =[]       
        self.fillP =self.axes.fill(self.Vel_P_Limit[0],self.Vel_P_Limit[1], color="lightgreen", alpha = 0.1333,)
        self.fillP += self.axes.fill(self.Vel_P[0],self.Vel_P[1],           color="lightgreen", alpha = 0.1333,)
        self.fillP += self.axes.fill(self.Vel_P_D_L[0],self.Vel_P_D_L[1],   color="lightgreen", alpha = 0.1333,)
        for i in range(len(self.VelInPos_markers)):
            self.axes.lines.remove(self.VelInPos_markers[i])
            #self.axes.lines.remove(self.VelInPos_tangents[i])
        self.VelInPos_markers  = []    
        #self.VelInPos_tangents = []
        for i in range(0,len(self.CP_P_Points[0])):
            #s = 0.1 * self.scaleP * math.sin(math.atan(self.CP_P_Points[2][i]))
            #c = 0.1 * self.scaleP * math.cos(math.atan(self.CP_P_Points[2][i]))
            #x_data = [(self.CP_P_Points[0][i] - c),(self.CP_P_Points[0][i] + c)]
            #y_data = [(self.CP_P_Points[1][i] - s),(self.CP_P_Points[1][i] + s)]
            self.VelInPos_markers  += self.axes.plot(self.CP_P_Points[0][i],self.CP_P_Points[1][i],marker ='x',markersize = 7*self.scaleP , color = 'darkred')
            #self.VelInPos_tangents += self.axes.plot(x_data,y_data, linewidth=1.0, linestyle="-",  marker ='o',markersize = 4*self.scaleP , color = 'g', fillstyle = 'none')

        self.linesT[0].set( xdata = self.Vel_T_Limit[0],  ydata=self.Vel_T_Limit[1])
        self.linesT[1].set( xdata = self.Vel_T[0],        ydata=self.Vel_T[1])
        self.linesT[2].set( xdata = self.Acc_T[0],        ydata=self.Acc_T[1])
        self.linesT[3].set( xdata = self.Acc_T_D_L[0],    ydata=self.Acc_T_D_L[1])
        self.linesT[4].set( xdata = self.Vel_T_D_L[0],    ydata=self.Vel_T_D_L[1])
        self.linesT[5].set( xdata = self.Acc_Conv[0],     ydata=self.Acc_Conv[1])
        self.linesT[6].set( xdata = self.Vel_Conv[0],     ydata=self.Vel_Conv[1])
        self.linesT[7].set( xdata = self.intVel_Conv[0],  ydata=self.intVel_Conv[1])          

        for i in range (len(self.fillT)):
            self.axesT.patches.remove(self.fillT[i])
        self.fillT =[] 
        self.fillT += self.axesT.fill(self.Vel_T_Limit[0], self.Vel_T_Limit[1] , color="lightgreen", alpha = 0.2,)               
        self.fillT += self.axesT.fill(self.Vel_T[0],       self.Vel_T[1],        color="lightgreen", alpha = 0.2,)

        if init:
            for i in range(len(self.VelInTime_markers)):
                self.axesT.lines.remove(self.VelInTime_markers[i])
                # Set to Comment as Smoothing makes Tangent Editing obsolete
                #self.axesT.lines.remove(self.VelInTime_tangents[i])
                #self.axesT.lines.remove(self.Vel_Conv_markers[i])
            self.VelInTime_markers  = []
            # Set to Comment as Smoothing makes Tangent Editing obsolete
            #self.VelInTime_tangents = []
            #self.Vel_Conv_markers   = []
            for i in range(0,len(self.CP_T_Points[0])):
                s = 0.125 * self.scaleT * math.sin(math.atan(self.CP_T_Points[2][i]))
                c = 0.125 * self.scaleT * math.cos(math.atan(self.CP_T_Points[2][i]))
                x_data = [(self.CP_T_Points[0][i] - c),(self.CP_T_Points[0][i] + c)]
                y_data = [(self.CP_T_Points[1][i] - s),(self.CP_T_Points[1][i] + s)]
                self.VelInTime_markers  += self.axesT.plot(self.CP_T_Points[0][i],self.CP_T_Points[1][i],marker ='x',markersize = 7*self.scaleT , color = 'darkred')
                # Set to Comment as Smoothing makes Tangent Editing obsolete
                #self.VelInTime_tangents += self.axesT.plot(x_data,y_data, linewidth=1.0, linestyle="-",  marker ='o',markersize = 3*self.scaleT , color = 'g', fillstyle = 'none')
                #self.Vel_Conv_markers   += self.axesT.plot(self.Vel_Conv_Points[0],self.Vel_Conv_Points[1], marker ='o',markersize = 3*self.scaleT , color = 'b', fillstyle = 'none')
        else:
            for i in range(len(self.VelInTime_markers)):
                s = 0.1 * self.scaleT * math.sin(math.atan(self.CP_T_Points[2][i]))
                c = 0.1 * self.scaleT * math.cos(math.atan(self.CP_T_Points[2][i]))
                x_data = [(self.CP_T_Points[0][i] - c),(self.CP_T_Points[0][i] + c)]
                y_data = [(self.CP_T_Points[1][i] - s),(self.CP_T_Points[1][i] + s)]
                self.VelInTime_markers[i].set(xdata=self.CP_T_Points[0][i],ydata=self.CP_T_Points[1][i])
                #self.Vel_Conv_markers[i].set(xdata=self.Vel_Conv_Points[0][i],ydata=self.Vel_Conv_Points[1][i])
                # Set to Comment as Smoothing makes Tangent Editing obsolete
                #self.VelInTime_tangents[i].set(xdata=x_data,ydata=y_data)

        self.Refresh()

    def OnPaint(self,evt):
        #self.Plot(init = False)
        if  self.rezoom == True: 
            minlimx = self.CP_P_Points[0][0]-0.05 
            maxlimx = float(self.VelEditorFrame.txtSetupLength.GetValue())+0.05
            self.axes.set_xlim(minlimx,maxlimx)
            m = max(float(self.VelEditorFrame.txtSetupMaxAcc.GetValue()),float(self.VelEditorFrame.txtSetupMaxVel.GetValue())) 
            self.axes.set_ylim(-0.5,m*1.2)
        if self.modifyP == 'TPoint' or self.rezoom == True:
            minlimTx = self.Vel_T[0][0]-0.05
            maxlimTx = self.Vel_T[0][-1]+0.05
            self.axesT.set_xlim(minlimTx,maxlimTx)
            ma = max(float(self.VelEditorFrame.txtSetupMaxAcc.GetValue()),float(self.VelEditorFrame.txtSetupMaxVel.GetValue()))
            mi = min(-float(self.VelEditorFrame.txtSetupMaxAcc.GetValue()),-float(self.VelEditorFrame.txtSetupMaxVel.GetValue()))
            self.axesT.set_ylim(mi * 1.2, ma * 1.2)
            self.rezoom = False

        size =  self.parent.GetClientSize()
        self.figure.set_size_inches(size[0]/self.dpi,size[1]/self.dpi)
        self.canvas.SetSize(size)
        self.canvas.draw()
        evt.Skip()
                           
    def MovePointTimeDomain(self):
        if self.modifyP == 'TPoint':
            flag = ''
            x1 = self.VelInTime_markers[self.hpoint-1].get_xdata()
            y2 = self.VelInTime_markers[self.hpoint].get_ydata()
            x3 = self.VelInTime_markers[self.hpoint+1].get_xdata()
            MDX = self.MouseDeltaXPoint
            MDY = self.MouseDeltaYPoint

            if (x1+0.1 < self.ThpointX-MDX and
                self.ThpointX-MDX < x3-0.1):        
                x = self.ThpointX-MDX
            else:
                flag = 'exit' 
                if MDX < 0 :
                    x= x3-0.1
                else:
                    x= x1+0.1

            if (self.eval_Grenz_T_Points(x) > self.ThpointY-MDY):
                y= max((self.ThpointY-MDY),0)
            else:
                flag = 'exit'
                y = max((self.eval_Grenz_T_Points(x)),0) 

            if flag == 'exit':
                self.modifyP == 'none'               
                self.VelInTime_markers[self.hpoint].set(color='r')
            else:
                self.VelInTime_markers[self.hpoint].set(color='darkred')

            if (np.max(self.Acc_T[1]) <=  float(self.VelEditorFrame.txtSetupMaxAcc.GetValue()) and
                abs(np.min(self.Acc_T[1])) <= float(self.VelEditorFrame.txtSetupMaxAcc.GetValue())):
                self.CP_M_Points[0][self.hpoint] = x
                self.CP_M_Points[1][self.hpoint] = y
            
            self.RecalcMove(init = False)

            self.Refresh()
            self.rezoom = False
            self.Plot(init = False)
        pass    
       
    def OnSize(self,evt):
        evt.Skip()  
    
    def OnMouseDown(self, evt):
        self.cur_xlim = self.axes.get_xlim()
        self.cur_ylim = self.axes.get_ylim()
        self.cur_xlimT = self.axesT.get_xlim()
        self.cur_ylimT = self.axesT.get_ylim()        
        self.press = self.x0, self.y0, evt.xdata, evt.ydata
        self.x0, self.y0, self.xpress, self.ypress = self.press

        if evt.button == 1:
            self.VelEditorFrame.chkSmoothing.SetValue(False)
            self.VelEditorFrame.chkSmoothingII.SetValue(False)
            if evt.inaxes == self.axes :
                for i in range(0,len(self.VelInPos_markers)):
                    if self.VelInPos_markers[i].contains(evt)[0]:
                        self.hpoint=i
                        self.PhpointX = self.VelInPos_markers[self.hpoint].get_xdata()
                        self.PhpointY = self.VelInPos_markers[self.hpoint].get_ydata()
                        self.VelInPos_markers[self.hpoint].set( color='b')
                        self.modifyP = 'PPoint'
                        self.VelInTime_markers[self.hpoint].set( color= 'b')
                        break
                    else:
                        self.modifyP = 'PI'
            elif evt.inaxes == self.axesT :
                self.rezoom = False
                for i in range(1,len(self.VelInTime_markers)-1):
                    if self.VelInTime_markers[i].contains(evt)[0]:
                        self.hpoint=i
                        self.ThpointX = self.VelInTime_markers[self.hpoint].get_xdata()
                        self.ThpointY = self.VelInTime_markers[self.hpoint].get_ydata()
                        self.VelInTime_markers[self.hpoint].set( color='b')
                        self.modifyP = 'TPoint'
                        self.VelInPos_markers[self.hpoint].set( color= 'b')
                        break
                    # Set to Comment as Smoothing makes Tangent Editing obsolete
                    # if self.VelInTime_tangents[i].contains(evt)[0]:
                    #     self.hpoint=i
                    #     self.ThpointX = self.VelInTime_tangents[self.hpoint].get_xdata()
                    #     self.ThpointY = self.VelInTime_tangents[self.hpoint].get_ydata()
                    #     self.VelInTime_tangents[self.hpoint].set( color='b')
                    #     self.modifyP = 'TTangentPoint'
                    #     break
                    else:
                        self.modifyP = 'TI'
            self.MouseDeltaXPoint = 0.0
            self.MouseDeltaYPoint = 0.0

            self.clickpoint = [evt.xdata, evt.ydata]
            self.Refresh()
        elif evt.button == 3:
            self.Pan(evt)
        pass
    
    def OnMouseMotion(self, evt):
        xdata = evt.xdata 
        ydata = evt.ydata 
        if(xdata is None):
            return()
        if(ydata is None):
            return()
        if self.VelEditorFrame:
            self.VelEditorFrame.txtMouseXPos.SetValue('%3.3f'%(evt.xdata))
            self.VelEditorFrame.txtMouseYPos.SetValue('%3.3f'%(evt.ydata))
        if evt.button == 1 and self.mousezoom == False:
            x, y = evt.xdata, evt.ydata 
            if x and y:
                self.MouseDeltaXPoint = self.clickpoint[0]-x
                self.MouseDeltaYPoint = self.clickpoint[1]-y                
                if self.modifyP == 'PPoint':
                    self.MovePointPosDomain()
                elif self.modifyP == 'TPoint':
                    self.MovePointTimeDomain()
                elif self.modifyP == 'TTangentPoint':
                    self.MoveTangentTimeDomain()
        elif evt.button == 3:
            self.Pan(evt)
        pass

    def MoveTangentTimeDomain(self):
        ''' Set to Comment as Smoothing makes Tangent Editing obsolete'''
        # MarkerX = (self.ThpointX[0]+self.ThpointX[1])/2.0
        # MarkerY = (self.ThpointY[0]+self.ThpointY[1])/2.0
        # if self.clickpoint[0]< self.CP_T_Points[0][self.hpoint] :
        #     #Left
        #     VPX =(self.ThpointX[0]-self.MouseDeltaXPoint) - MarkerX
        #     VPY =(self.ThpointY[0]-self.MouseDeltaYPoint) - MarkerY 
        #     k = VPY/VPX 
        # else: 
        #     #Right
        #     VPX =(self.ThpointX[0]+self.MouseDeltaXPoint) - MarkerX
        #     VPY =(self.ThpointY[0]+self.MouseDeltaYPoint) - MarkerY 
        #     k = VPY/VPX 
        # self.CP_T_Points[2][self.hpoint] = k
        # self.CP_M_Points[2][self.hpoint] = k
        # self.RecalcMove(init = False)
        # self.Refresh()
        # self.Plot(init = False)
        pass    

    def MovePointPosDomain(self):
        if self.modifyP == 'PPoint':
            flag = ''
            if self.hpoint > 1 and self.hpoint < len(self.CP_M_Points[0]):
                x1 = self.VelInPos_markers[self.hpoint-1].get_xdata()
                y2 = self.VelInPos_markers[self.hpoint].get_ydata()
                x3 = self.VelInPos_markers[self.hpoint+1].get_xdata()
                MDX = self.MouseDeltaXPoint
                MDY = self.MouseDeltaYPoint
                
                if (x1+0.1 < self.PhpointX-MDX and
                    self.PhpointX-MDX < x3-0.1):
                    x = self.PhpointX-MDX
                else:
                    flag = 'exit' 
                    if MDX < 0 :
                        x= x3-0.1
                    else:
                        x= x1+0.1

                if (self.eval_Grenz_P_Points(x,False) > self.PhpointY-MDY ):
                    y=max((self.PhpointY-MDY),0.1)
                else:
                    flag = 'exit'
                    y = max(self.eval_Grenz_P_Points(x,False),0.1) 

                if flag == 'exit':
                    self.modifyP == 'none'               
                    self.VelInPos_markers[self.hpoint].set(color='r')
                else:
                    self.VelInPos_markers[self.hpoint].set(color='darkred')

                if (np.max(self.Acc_T[1]) <=  float(self.VelEditorFrame.txtSetupMaxAcc.GetValue()) and
                    abs(np.min(self.Acc_T[1])) <= float(self.VelEditorFrame.txtSetupMaxAcc.GetValue())):
                    if (self.P_2_T(x) > self.CP_M_Points[0][self.hpoint-1] and
                        self.P_2_T(x) < self.CP_M_Points[0][self.hpoint+1]):
                        self.CP_M_Points[0][self.hpoint] = self.P_2_T(x)
                        self.CP_M_Points[1][self.hpoint] = y
                
                self.RecalcMove(init = False)

                self.Refresh()
                self.Plot(init = False)

    def RecalcMove(self, init):
        #print('Recalc')
        if init:
            for i in range(0, len(self.X_Pos_Values)):
                self.Vel_P_Limit[0].append(self.T_2_P(self.Vel_T_D[0][i]))
                self.Vel_P_Limit[1].append(self.Vel_T_D[1][i])

        u = self.eval_CP_M_Points(0.1,True)
        pint = self.CP_M_BPoly.antiderivative(1)        
        PosI = pint(self.CP_T_Points[0][-1])

        self.TimeScaling           = self.Length / PosI
        self.X_Time_Values         = self.X_Time_Values        * self.TimeScaling        
        self.CP_M_Points[0]        = self.CP_M_Points[0]       * self.TimeScaling
        self.TimeScalingAbs        = self.X_Time_Values[-1] / self.Pos_T_D[0][-1]

        u = self.eval_CP_M_Points(0.1,True)
        pint = self.CP_M_BPoly.antiderivative(1)

        self.CP_T_Points[0] = copy.copy(self.CP_M_Points[0])
        self.CP_T_Points[1] = copy.copy(self.CP_M_Points[1])
        self.CP_T_Points[2] = copy.copy(self.CP_M_Points[2])

        self.CP_P_Points[0] = copy.copy(self.T_2_P(self.CP_M_Points[0]))
        self.CP_P_Points[1] = copy.copy(self.CP_M_Points[1])
        self.CP_P_Points[2] = copy.copy(self.CP_M_Points[2])

        self.Vel_T[0] = self.X_Time_Values
        self.Vel_T[1] = self.eval_CP_T_Points(self.X_Time_Values,True)

        self.Vel_P[0] = self.X_Pos_Values
        self.Vel_P[1] = self.eval_CP_P_Points(self.X_Pos_Values,True)

        self.Vel_T_Limit[0]= self.Vel_T_D[0] * self.TimeScalingAbs
        self.Vel_T_Limit[1]= self.Vel_T_D[1]

        pdt  = self.CP_T_BPoly.derivative(1)
        self.Acc_T[0] = self.X_Time_Values
        self.Acc_T[1] = pdt(self.X_Time_Values)

        if self.VelEditorFrame:
            maxAcc = abs(max(self.Acc_T[1]))
            maxDcc = abs(min(self.Acc_T[1]))
            self.VelEditorFrame.txtUsrDuration.SetValue('%3.3f'% self.CP_M_Points[0][-1])
            self.VelEditorFrame.txtUsrTimeFactor.SetValue('%3.3f'% \
                (float(self.VelEditorFrame.txtUsrDuration.GetValue())/float(self.VelEditorFrame.txtSetupTime.GetValue())))
            self.VelEditorFrame.txtProfileMaxAcc.SetValue('%3.3f'% maxAcc)
            self.VelEditorFrame.txtProfileMaxDcc.SetValue('%3.3f'% maxDcc)

            if maxAcc <= 0.9 * float(self.VelEditorFrame.txtSetupMaxAcc.GetValue()):
                self.VelEditorFrame.txtProfileMaxAcc.SetBackgroundColour((0,204,0))
            elif 0.9 * float(self.VelEditorFrame.txtSetupMaxAcc.GetValue()) < maxAcc <= float(self.VelEditorFrame.txtSetupMaxAcc.GetValue()):
                self.VelEditorFrame.txtProfileMaxAcc.SetBackgroundColour((255,128,0))
            elif maxAcc > float(self.VelEditorFrame.txtSetupMaxAcc.GetValue()):
                self.VelEditorFrame.txtProfileMaxAcc.SetBackgroundColour((204,0,0))
            else:
                self.VelEditorFrame.txtProfileMaxAcc.SetBackgroundColour((225,225,225))

            if abs(maxDcc) <= 0.9 * float(self.VelEditorFrame.txtSetupMaxAcc.GetValue()):
                self.VelEditorFrame.txtProfileMaxDcc.SetBackgroundColour((0,204,0))
            elif 0.9 * float(self.VelEditorFrame.txtSetupMaxAcc.GetValue()) < abs(maxDcc) <= float(self.VelEditorFrame.txtSetupMaxAcc.GetValue()):
                self.VelEditorFrame.txtProfileMaxDcc.SetBackgroundColour((255,128,0))
            elif abs(maxDcc) >  float(self.VelEditorFrame.txtSetupMaxAcc.GetValue()):
                self.VelEditorFrame.txtProfileMaxDcc.SetBackgroundColour((204,0,0))
            else:
                self.VelEditorFrame.txtProfileMaxDcc.SetBackgroundColour((225,225,225))

    def Smooth(self):
        for i in range(1,len(self.CP_M_Points[0])-1):
            kl = (self.CP_M_Points[1][i]-self.CP_M_Points[1][i-1])/(self.CP_M_Points[0][i]-self.CP_M_Points[0][i-1])
            kr = (self.CP_M_Points[1][i+1]-self.CP_M_Points[1][i])/(self.CP_M_Points[0][i+1]-self.CP_M_Points[0][i])
            km = (self.CP_M_Points[1][i+1]-self.CP_M_Points[1][i-1])/(self.CP_M_Points[0][i+1]-self.CP_M_Points[0][i-1])
            self.CP_M_Points[2][i] = ( kl + kr + km ) / 3.0

        self.VelEditorFrame.chkSmoothing.SetValue(True)

        self.RecalcMove(init = False)        
        self.rezoom          = True
        self.Plot(init       = False)

    def SmoothII(self):
        length = int(self.Samples / 35)
        mask = np.ones((1,length))/length
        mask = mask[0,:]
        self.Acc_Conv[1] = np.convolve(self.Acc_T[1],mask, mode ='same')
        self.Acc_Conv[0] = self.Acc_T[0]

        self.integrate_Acc_Conv()

        for i in range(0, len(self.CP_M_Points[0])):
            self.Vel_Conv_Points[0][i] = (self.CP_M_Points[0][i])
            self.Vel_Conv_Points[1][i] = (self.interpVel_Conv(self.CP_M_Points[0][i]))            
            self.Vel_Conv_Points[2][i] = (self.interpAcc_Conv(self.CP_M_Points[0][i]))

        self.Vel_Conv[0] = self.X_Time_Values
        self.Vel_Conv[1] = self.eval_Vel_Conv_Points(self.X_Time_Values,True)

        self.CP_M_Points[0] = copy.copy(self.Vel_Conv_Points[0])
        self.CP_M_Points[1] = copy.copy(self.Vel_Conv_Points[1])
        self.CP_M_Points[2] = copy.copy(self.Vel_Conv_Points[2])

        self.integrate_Vel_Conf()

        self.VelEditorFrame.chkSmoothingII.SetValue(True)

        self.RecalcMove(init = False)        
        self.rezoom          = True
        self.Plot(init       = False)

    def integrate_Vel_Conf(self):
        self.intVel_Conv[0] = self.X_Time_Values
        self.intVel_Conv[1] = [0]
        SV = 0
        for i in range(1,len(self.X_Time_Values)):
            V = (((self.Vel_Conv[1][i-1]+self.Vel_Conv[1][i])/2)* (self.X_Time_Values[i]-self.X_Time_Values[i-1]))
            SV += V
            self.intVel_Conv[1].append(SV)        

    def integrate_Acc_Conv(self):
        self.intAcc_Conv[0] = self.X_Time_Values
        self.intAcc_Conv[1] = [0]
        SV = 0
        for i in range(1,len(self.X_Time_Values)):
            V = (((self.Acc_Conv[1][i-1]+self.Acc_Conv[1][i])/2)* (self.X_Time_Values[i]-self.X_Time_Values[i-1]))
            SV += V
            self.intAcc_Conv[1].append(SV)

    def interpVel_Conv(self,x):
        f=interp1d(self.intAcc_Conv[0],self.intAcc_Conv[1], kind ='slinear',bounds_error=False, fill_value=np.nan)
        return f(x)

    def interpAcc_Conv(self,x):
        f=interp1d(self.Acc_Conv[0],self.Acc_Conv[1], kind ='slinear',bounds_error=False, fill_value=np.nan)
        return f(x)

    def eval_Vel_Conv_Points(self,x,refresh):
        '''BPoly '''
        if refresh:
            yi = [[self.Vel_Conv_Points[1][0],self.Vel_Conv_Points[2][0]]]
            for i in range(1,len(self.Vel_Conv_Points[0])):
                yi.append([self.Vel_Conv_Points[1][i],self.Vel_Conv_Points[2][i]])
            order = 3
            self.Vel_Conv_BPoly =BPoly.from_derivatives(self.Vel_Conv_Points[0],yi,orders = order)
        return self.Vel_Conv_BPoly(x)

    def Pan(self, evt):
        if self.press is None: return
        if evt.inaxes == self.axes :
            dx = evt.xdata - self.xpress
            dy = evt.ydata - self.ypress
            self.cur_xlim -= dx
            self.cur_ylim -= dy
            self.axes.set_xlim(self.cur_xlim)
            self.axes.set_ylim(self.cur_ylim)
        else:
            dx = evt.xdata - self.xpress
            dy = evt.ydata - self.ypress            
            self.cur_xlimT -= dx
            self.cur_ylimT -= dy    
            self.axesT.set_xlim(self.cur_xlimT)
            self.axesT.set_ylim(self.cur_ylimT)            
            
        self.axes.figure.canvas.draw()
        self.Refresh()

    def OnScroll(self, evt):
        base_scale = .7
        cur_xlim = self.axes.get_xlim()
        cur_ylim = self.axes.get_ylim()
        cur_xlimT = self.axesT.get_xlim()
        cur_ylimT = self.axesT.get_ylim()        
    
        xdata = evt.xdata 
        ydata = evt.ydata 
        if(xdata is None):
            return()
        if(ydata is None):
            return()

        if evt.button == 'down':
            # deal with zoom in
            scale_factor = 1 / base_scale
        elif evt.button == 'up':
            # deal with zoom out
            scale_factor = base_scale
        else:
            scale_factor = 1
                
        if evt.inaxes == self.axes :
            self.scaleP = scale_factor
            new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor
            new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor 
            relx = (cur_xlim[1] - xdata)/(cur_xlim[1] - cur_xlim[0])
            rely = (cur_ylim[1] - ydata)/(cur_ylim[1] - cur_ylim[0])
            if(self.xzoom):
                self.axes.set_xlim([xdata - new_width * (1-relx), xdata + new_width * (relx)])
            if(self.yzoom):
                self.axes.set_ylim([ydata - new_height * (1-rely), ydata + new_height * (rely)]) 
        else:
            self.scaleT = scale_factor
            new_widthT = (cur_xlimT[1] - cur_xlimT[0]) * scale_factor
            new_heightT = (cur_ylimT[1] - cur_ylimT[0]) * scale_factor
            relxT = (cur_xlimT[1] - xdata)/(cur_xlimT[1] - cur_xlimT[0])
            relyT = (cur_ylimT[1] - ydata)/(cur_ylimT[1] - cur_ylimT[0])
            if(self.xzoom):
                self.axesT.set_xlim([xdata - new_widthT * (1-relxT), xdata + new_widthT * (relxT)])
            if(self.yzoom):
                self.axesT.set_ylim([ydata - new_heightT * (1-relyT), ydata + new_heightT * (relyT)])            
        
        self.axes.figure.canvas.draw()
        self.Refresh()
        pass
        
    def OnMouseUp(self, evt):
        for i in range(len(self.VelInPos_markers)):
            self.VelInPos_markers[self.hpoint].set(color='darkred')
        for i in range(len(self.VelInTime_markers)):
            self.VelInTime_markers[self.hpoint].set(color='darkred')
            # Set to Comment as Smoothing makes Tangent Editing obsolete
            #self.VelInTime_tangents[self.hpoint].set(color='g')
        self.modifyP = 'none'
        if self.VelEditorFrame.chkSmoothing.GetValue() == False:
            self.Smooth()
        if self.VelEditorFrame.chkSmoothingII.GetValue() == False:
            self.SmoothII()

        self.Refresh()

    def OnKeyPress(self,evt):
        if evt.key == 'd':
            if (self.modifyP == 'TPoint' or self.modifyP == 'PPoint') and len(self.CP_P_Points[0]) >= 4:                
                self.CP_P_Points      = np.delete(self.CP_P_Points,self.hpoint,axis=1)
                self.CP_T_Points      = np.delete(self.CP_T_Points,self.hpoint,axis=1)
                self.CP_M_Points      = np.delete(self.CP_M_Points,self.hpoint,axis=1)
                self.Vel_Conv_Points  = np.delete(self.Vel_Conv_Points,self.hpoint,axis=1)
                self.modifyP = 'none'
                self.RecalcMove(init = False)
                self.Plot(init = True)
                self.Refresh()                
        elif evt.key == 'i' and self.modifyP == 'TI':
            if self.clickpoint[0] > 0.1:
                y = self.eval_CP_M_Points(self.clickpoint[0],False)
                i = np.searchsorted(self.CP_M_Points[0],self.clickpoint[0])
                self.CP_M_Points     = np.insert(self.CP_M_Points,i,[self.clickpoint[0],y,0],axis =1)
                self.CP_T_Points     = np.insert(self.CP_T_Points,i,[self.clickpoint[0],y,0],axis =1)
                self.CP_P_Points     = np.insert(self.T_2_P(self.CP_P_Points),i,[self.clickpoint[0],y,0],axis =1)
                self.Vel_Conv_Points = np.insert(self.Vel_Conv_Points,i,[self.clickpoint[0],y,0],axis =1)
                self.RecalcMove(init = False)
                self.Plot(init = True)
                self.Refresh()                
        elif evt.key == 'i' and self.modifyP == 'PI':
            pass
            if self.clickpoint[0] > 0.1:
                y = self.eval_CP_P_Points((self.clickpoint[0]),False)
                i = np.searchsorted(self.CP_M_Points[0],self.P_2_T(self.clickpoint[0]))
                self.CP_M_Points     = np.insert(self.CP_M_Points,i,[self.P_2_T(self.clickpoint[0]),y,0],axis =1)
                self.CP_T_Points     = np.insert(self.CP_T_Points,i,[self.P_2_T(self.clickpoint[0]),y,0],axis =1)
                self.CP_P_Points     = np.insert(self.CP_P_Points,i,[self.clickpoint[0],y,0],axis =1)
                self.Vel_Conv_Points = np.insert(self.Vel_Conv_Points,i,[self.P_2_T(self.clickpoint[0]),y,0],axis =1)
                self.RecalcMove(init = False)
                self.Plot(init = True)
                self.Refresh()                
        elif evt.key == 'z':
            self.axes.relim()
            self.axes.autoscale(enable=True, axis='both')
            self.axesT.relim()
            self.axesT.autoscale(enable=True, axis='both')            
            self.axes.figure.canvas.draw()
            self.axesT.figure.canvas.draw()
            #self.axes.figure.canvas.flush_events 
        elif evt.key == "x":
            self.xzoom = True
            self.yzoom = False
        elif evt.key == 'y':
            self.xzoom = False
            self.yzoom = True
        elif evt.key == 'm':
            self.mousezoom = True
        pass
            
    def OnKeyRelease(self,evt):
        self.xzoom = True
        self.yzoom = True 
        self.mousezoom = False
        pass

class VelEditor4C(wx.App):
    #def __init__(self):
        #self.OnInit()

    def OnInit(self):        
        self.res = xrc.XmlResource('VelEditorWW.xrc')
        self.KeyPointWindow                       = self.res.LoadFrame(None,'ID_WXFRAME')
        self.KeyPointWindow.panelMainPanel        = xrc.XRCCTRL(self.KeyPointWindow,'MainPanel')         
        self.KeyPointWindow.panelOne              = xrc.XRCCTRL(self.KeyPointWindow.panelMainPanel,'PanelOne')
        self.KeyPointWindow.panelVelPath          = xrc.XRCCTRL(self.KeyPointWindow.panelOne,'panelVelPath')        
        self.KeyPointWindow.Diagramm              = Diagramm(self.KeyPointWindow.panelVelPath)        
        self.KeyPointWindow.txtSetupLength        = xrc.XRCCTRL(self.KeyPointWindow,'txtSetupLength')
        self.KeyPointWindow.txtSetupTime          = xrc.XRCCTRL(self.KeyPointWindow,'txtSetupTime')       
        self.KeyPointWindow.txtSetupMaxAcc        = xrc.XRCCTRL(self.KeyPointWindow,'txtSetupMaxAcc')
        self.KeyPointWindow.txtSetupMaxVel        = xrc.XRCCTRL(self.KeyPointWindow,'txtSetupMaxVel')
        self.KeyPointWindow.txtUsrAcc             = xrc.XRCCTRL(self.KeyPointWindow,'txtUsrAcc')
        self.KeyPointWindow.txtUsrVel             = xrc.XRCCTRL(self.KeyPointWindow,'txtUsrVel')
        self.KeyPointWindow.txtUsrLength          = xrc.XRCCTRL(self.KeyPointWindow,'txtUsrLength')
        self.KeyPointWindow.txtUsrDuration        = xrc.XRCCTRL(self.KeyPointWindow,'txtUsrDuration')
        self.KeyPointWindow.txtMouseXPos          = xrc.XRCCTRL(self.KeyPointWindow,'txtMouseXPos')
        self.KeyPointWindow.txtMouseYPos          = xrc.XRCCTRL(self.KeyPointWindow,'txtMouseYPos')
        self.KeyPointWindow.txtProfileMaxAcc      = xrc.XRCCTRL(self.KeyPointWindow,'txtProfileMaxAcc')
        self.KeyPointWindow.txtProfileMaxDcc      = xrc.XRCCTRL(self.KeyPointWindow,'txtProfileMaxDcc')
        self.KeyPointWindow.btnGenerate           = xrc.XRCCTRL(self.KeyPointWindow,'btnGenerate')
        self.KeyPointWindow.txtUsrTimeFactor      = xrc.XRCCTRL(self.KeyPointWindow,'txtUsrTimeFactor')  
        self.KeyPointWindow.btnSign               = xrc.XRCCTRL(self.KeyPointWindow,'btnSign')
        self.KeyPointWindow.txtDescription        = xrc.XRCCTRL(self.KeyPointWindow,'txtDescription')
        self.KeyPointWindow.txtName               = xrc.XRCCTRL(self.KeyPointWindow,'txtName')
        self.KeyPointWindow.chkSign               = xrc.XRCCTRL(self.KeyPointWindow,'chkSign')
        self.KeyPointWindow.chkSmoothing          = xrc.XRCCTRL(self.KeyPointWindow,'chkSmoothing')
        self.KeyPointWindow.chkSmoothingII          = xrc.XRCCTRL(self.KeyPointWindow,'chkSmoothingII')

        #self.KeyPointWindow.txtMaxTime.Enable(False)
        self.KeyPointWindow.txtMouseXPos.Enable(False)
        self.KeyPointWindow.txtMouseYPos.Enable(False)
        self.KeyPointWindow.btnGenerate.Enable(False)
        
        self.Bind(wx.EVT_BUTTON        , self.OnButtonGenerate,      self.KeyPointWindow.btnGenerate)
        self.Bind(wx.EVT_BUTTON        , self.OnButtonSign,          self.KeyPointWindow.btnSign)
        self.Bind(wx.EVT_CHECKBOX      , self.OnSmooth,              self.KeyPointWindow.chkSmoothing)
        self.Bind(wx.EVT_CHECKBOX      , self.OnSmoothII,            self.KeyPointWindow.chkSmoothingII)


        File = wx.Menu()
        openFile = File.Append(ID_Menu_OpenVelFile,'Open Vel File','This opens a VelFile for editing')
        saveFile = File.Append(ID_Menu_SaveVelFile,'Save Vel File','This saves a vel File')
        File.AppendSeparator()        
        exit = File.Append(ID_Menu_Exit,'Exit','This exits the Program without saving anything')

        self.Bind(wx.EVT_MENU              , self.OpenFile,                  openFile)
        self.Bind(wx.EVT_MENU              , self.SaveFile,                  saveFile)
        self.Bind(wx.EVT_MENU              , self.Exit    ,                  exit)

        self.menuBar = wx.MenuBar(ID_Menu)        
        self.menuBar.Append(File,'File')
        self.KeyPointWindow.SetMenuBar(self.menuBar)

        self.KeyPointWindow.Show()

        return True

    def OnSmooth(self, evt):
        self.KeyPointWindow.Diagramm.Smooth()

    def OnSmoothII(self, evt):
        self.KeyPointWindow.Diagramm.SmoothII()

    def OnButtonSign(self,evt):
        if (abs(float(self.KeyPointWindow.txtProfileMaxAcc.GetValue())) <= abs(float(self.KeyPointWindow.txtSetupMaxAcc.GetValue())) and
            abs(float(self.KeyPointWindow.txtProfileMaxDcc.GetValue())) <= abs(float(self.KeyPointWindow.txtSetupMaxAcc.GetValue()))):

            self.KeyPointWindow.chkSign.SetValue(True)

        else:
            dlg = wx.MessageDialog(None,'Invalid Data  Check Accelerations', 'Invalid', wx.OK)
            dlg.ShowModal()
            print('Invalid Data')
        pass

    def OnButtonGenerate(self,evt):
        if (float(self.KeyPointWindow.txtSetupMaxAcc.GetValue()) >= float(self.KeyPointWindow.txtUsrAcc.GetValue()) and
            float(self.KeyPointWindow.txtSetupMaxVel.GetValue()) >= float(self.KeyPointWindow.txtUsrVel.GetValue())  and
            float(self.KeyPointWindow.txtSetupLength.GetValue()) >= float(self.KeyPointWindow.txtUsrLength.GetValue())):

            self.KeyPointWindow.Diagramm.GenerateProfile(float(self.KeyPointWindow.txtUsrLength.GetValue()),\
                                                     float(self.KeyPointWindow.txtUsrAcc.GetValue()),\
                                                     float(self.KeyPointWindow.txtUsrVel.GetValue()))
            self.KeyPointWindow.chkSign.SetValue(False)

        else:
            dlg = wx.MessageDialog(None,'Invalid Data Check Usr Limits', 'Invalid Data', wx.OK)
            dlg.ShowModal()
            print('Invalid Data')
        pass
        
    def OpenFile(self,evt):
        with wx.FileDialog(None, "Open Vel file", wildcard="Vel files (*.sfxact)|*.sfxact",
                       style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return     # the user changed their mind

            # Proceed loading the file chosen by the user
            pathname = fileDialog.GetPath()
            try:
                with open(pathname, 'r', encoding='utf-8') as file:
                    self.LoadData(file)
            except IOError:
                wx.LogError("Cannot open file '%s'." % newfile)

    def SaveFile(self,evt):
        if self.KeyPointWindow.chkSign.GetValue():
            self.CompileData()
            with wx.FileDialog(None, "Save Vel file", wildcard="Vel files (*.sfxact)|*.sfxact",
                        style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:

                if fileDialog.ShowModal() == wx.ID_CANCEL:
                    return     # the user changed their mind

                # save the current contents in the file
                pathname = fileDialog.GetPath()
                try:
                    with open(pathname, 'w') as file:
                        self.SaveData(file)
                except IOError:
                    wx.LogError("Cannot save current data in file '%s'." % pathname)
        else:  
            dlg = wx.MessageDialog(None,'The Profile has to be Signed','Invalid Data',  wx.OK)
            dlg.ShowModal()
            print('Invalid Data')       
        pass

    def SaveData(self,file):
        file.write(json.dumps(self.SData))
        file.close()

    def CompileData(self):        
        self.SData =[ "Action ID"                                                     + ';' +     # 0
                self.KeyPointWindow.Diagramm.Action_Name                              + ';' +     # 1
                self.KeyPointWindow.Diagramm.Action_Saved                             + ';' +     # 2
                self.KeyPointWindow.Diagramm.Action_Path                              + ';' +     # 3
                str(self.KeyPointWindow.Diagramm.Action_MinPos)                       + ';' +     # 4
                str(self.KeyPointWindow.Diagramm.Action_MaxPos)                       + ';' +     # 5
                str(self.KeyPointWindow.Diagramm.Action_MaxAcc)                       + ';' +     # 6
                str(self.KeyPointWindow.Diagramm.Action_MaxVel)                       + ';' +     # 7
                str(self.KeyPointWindow.Diagramm.Action_Length)                       + ';' +     # 8
                json.dumps(self.KeyPointWindow.Diagramm.Action_Jrk[0].tolist())       + ';' +     # 9
                json.dumps(self.KeyPointWindow.Diagramm.Action_Jrk[1].tolist())       + ';' +     # 10
                json.dumps(self.KeyPointWindow.Diagramm.Action_Acc[0].tolist())       + ';' +     # 11
                json.dumps(self.KeyPointWindow.Diagramm.Action_Acc[1].tolist())       + ';' +     # 12
                json.dumps(self.KeyPointWindow.Diagramm.Action_Vel[0].tolist())       + ';' +     # 13
                json.dumps(self.KeyPointWindow.Diagramm.Action_Vel[1].tolist())       + ';' +     # 14
                json.dumps(self.KeyPointWindow.Diagramm.Action_Pos[0].tolist())       + ';' +     # 15
                json.dumps(self.KeyPointWindow.Diagramm.Action_Pos[1].tolist())       + ';' +     # 16
                json.dumps(self.KeyPointWindow.Diagramm.Action_VelInPos[0].tolist())  + ';' +     # 17
                json.dumps(self.KeyPointWindow.Diagramm.Action_VelInPos[1].tolist())  + ';' +     # 18
                self.KeyPointWindow.txtDescription.GetValue()                         + ';' +     # 19
                json.dumps((self.KeyPointWindow.Diagramm.Jrk_T_D_L[0]).tolist())      + ';' +     # 20
                json.dumps((self.KeyPointWindow.Diagramm.Jrk_T_D_L[1]).tolist())      + ';' +     # 21
                json.dumps((self.KeyPointWindow.Diagramm.Acc_T_D_L[0]).tolist())      + ';' +     # 22
                json.dumps((self.KeyPointWindow.Diagramm.Acc_T_D_L[1]).tolist())      + ';' +     # 23
                json.dumps((self.KeyPointWindow.Diagramm.Vel_T_D_L[0]).tolist())      + ';' +     # 24
                json.dumps((self.KeyPointWindow.Diagramm.Vel_T_D_L[1]).tolist())      + ';' +     # 25
                json.dumps((self.KeyPointWindow.Diagramm.Pos_T_D_L[0]).tolist())      + ';' +     # 26
                json.dumps((self.KeyPointWindow.Diagramm.Pos_T_D_L[1]).tolist())      + ';' +     # 27
                json.dumps((self.KeyPointWindow.Diagramm.Vel_P_D_L[0]).tolist())      + ';' +     # 28
                json.dumps((self.KeyPointWindow.Diagramm.Vel_P_D_L[1]).tolist())      + ';' +     # 29
                json.dumps((self.KeyPointWindow.Diagramm.Jrk_T_D[0]).tolist())        + ';' +     # 30
                json.dumps((self.KeyPointWindow.Diagramm.Jrk_T_D[1]).tolist())        + ';' +     # 31
                json.dumps((self.KeyPointWindow.Diagramm.Acc_T_D[0]).tolist())        + ';' +     # 32
                json.dumps((self.KeyPointWindow.Diagramm.Acc_T_D[1]).tolist())        + ';' +     # 33
                json.dumps((self.KeyPointWindow.Diagramm.Vel_T_D[0]).tolist())        + ';' +     # 34
                json.dumps((self.KeyPointWindow.Diagramm.Vel_T_D[1]).tolist())        + ';' +     # 35
                json.dumps((self.KeyPointWindow.Diagramm.Pos_T_D)[0].tolist())        + ';' +     # 36
                json.dumps((self.KeyPointWindow.Diagramm.Pos_T_D)[1].tolist())        + ';' +     # 37
                json.dumps((self.KeyPointWindow.Diagramm.Vel_P_D[0]).tolist())        + ';' +     # 38
                json.dumps((self.KeyPointWindow.Diagramm.Vel_P_D[1]).tolist())        + ';' +     # 39
                json.dumps((self.KeyPointWindow.Diagramm.CP_T_Points[0]).tolist())    + ';' +     # 40
                json.dumps((self.KeyPointWindow.Diagramm.CP_T_Points[1]).tolist())    + ';' +     # 41
                json.dumps((self.KeyPointWindow.Diagramm.CP_T_Points[2]).tolist())    + ';' +     # 42
                json.dumps((self.KeyPointWindow.Diagramm.CP_P_Points[0]).tolist())    + ';' +     # 43
                json.dumps((self.KeyPointWindow.Diagramm.CP_P_Points[1]).tolist())    + ';' +     # 44
                json.dumps((self.KeyPointWindow.Diagramm.CP_P_Points[2]).tolist())    + ';' +     # 45
                json.dumps((self.KeyPointWindow.Diagramm.CP_M_Points[0]).tolist())    + ';' +     # 46
                json.dumps((self.KeyPointWindow.Diagramm.CP_M_Points[1]).tolist())    + ';' +     # 47
                json.dumps((self.KeyPointWindow.Diagramm.CP_M_Points[2]).tolist())    + ';' +     # 48
                str(self.KeyPointWindow.Diagramm.Action_Signed)                       + ';' +     # 49
                str(self.KeyPointWindow.txtUsrAcc.GetValue())                         + ';' +     # 50
                str(self.KeyPointWindow.txtUsrVel.GetValue())                         + ';' +     # 51
                str(self.KeyPointWindow.txtUsrLength.GetValue())                      + ';' +     # 52
                str(self.KeyPointWindow.txtSetupTime.GetValue())                      + ';' +     # 53
                str(self.KeyPointWindow.Diagramm.TimeScaling)                         + ';' +     # 54
                str(self.KeyPointWindow.Diagramm.TimeScalingAbs)                      + ';' ]     # 55

    def Exit(self,evt):
        sys.exit()

    def LoadData(self,file):
        data = file.read()
        file.close()
        self.CP_P_Points_Limit = [[],[],[]] 
        self.CP_P_Points       = [[],[],[]]
        self.CP_T_Points       = [[],[],[]]
        self.CP_M_Points       = [[],[],[]]
        self.CP_T_Points_Limit = [[],[],[]]
        self.Jrk_T_D_L         = [[],[]]
        self.Acc_T_D_L         = [[],[]]
        self.Vel_T_D_L         = [[],[]]
        self.Pos_T_D_L         = [[],[]]
        self.Vel_P_D_L         = [[],[]]
        self.Jrk_T_D           = [[],[]]
        self.Acc_T_D           = [[],[]]
        self.Vel_T_D           = [[],[]]
        self.Pos_T_D           = [[],[]]
        self.Vel_P_D           = [[],[]]
        
        Data = data.split(';')
        if len(Data) == 57:
            self.KeyPointWindow.Diagramm.Action_ID            = Data[0]
            self.KeyPointWindow.Diagramm.Action_Name          = Data[1]
            self.KeyPointWindow.Diagramm.Action_Saved         = Data[2]
            self.KeyPointWindow.Diagramm.Action_Path          = Data[3]
            self.KeyPointWindow.Diagramm.Action_MinPos        = float(Data[4])
            self.KeyPointWindow.Diagramm.Action_MaxPos        = float(Data[5])
            self.KeyPointWindow.Diagramm.Action_MaxAcc        = float(Data[6])
            self.KeyPointWindow.Diagramm.Action_MaxVel        = float(Data[7])
            self.KeyPointWindow.Diagramm.Action_Length        = float(Data[8])
            self.KeyPointWindow.Diagramm.Action_Jrk[0]        = np.asarray(json.loads(Data[9]))
            self.KeyPointWindow.Diagramm.Action_Jrk[1]        = np.asarray(json.loads(Data[10]))
            self.KeyPointWindow.Diagramm.Action_Acc[0]        = np.asarray(json.loads(Data[11]))
            self.KeyPointWindow.Diagramm.Action_Acc[1]        = np.asarray(json.loads(Data[12]))
            self.KeyPointWindow.Diagramm.Action_Vel[0]        = np.asarray(json.loads(Data[13]))
            self.KeyPointWindow.Diagramm.Action_Vel[1]        = np.asarray(json.loads(Data[14]))
            self.KeyPointWindow.Diagramm.Action_Pos[0]        = np.asarray(json.loads(Data[15]))
            self.KeyPointWindow.Diagramm.Action_Pos[1]        = np.asarray(json.loads(Data[16]))
            self.KeyPointWindow.Diagramm.Action_VelInPos[0]   = np.asarray(json.loads(Data[17]))
            self.KeyPointWindow.Diagramm.Action_VelInPos[1]   = np.asarray(json.loads(Data[18]))
            self.KeyPointWindow.Diagramm.Action_Description   = Data[19]
            self.KeyPointWindow.Diagramm.Jrk_T_D_L[0]         = np.asarray(json.loads(Data[20]))
            self.KeyPointWindow.Diagramm.Jrk_T_D_L[1]         = np.asarray(json.loads(Data[21]))
            self.KeyPointWindow.Diagramm.Acc_T_D_L[0]         = np.asarray(json.loads(Data[22]))
            self.KeyPointWindow.Diagramm.Acc_T_D_L[1]         = np.asarray(json.loads(Data[23]))
            self.KeyPointWindow.Diagramm.Vel_T_D_L[0]         = np.asarray(json.loads(Data[24]))
            self.KeyPointWindow.Diagramm.Vel_T_D_L[1]         = np.asarray(json.loads(Data[25]))
            self.KeyPointWindow.Diagramm.Pos_T_D_L[0]         = np.asarray(json.loads(Data[26]))
            self.KeyPointWindow.Diagramm.Pos_T_D_L[1]         = np.asarray(json.loads(Data[27]))
            self.KeyPointWindow.Diagramm.Vel_P_D_L[0]         = np.asarray(json.loads(Data[28]))
            self.KeyPointWindow.Diagramm.Vel_P_D_L[1]         = np.asarray(json.loads(Data[29]))
            self.KeyPointWindow.Diagramm.Jrk_T_D[0]           = np.asarray(json.loads(Data[30]))
            self.KeyPointWindow.Diagramm.Jrk_T_D[1]           = np.asarray(json.loads(Data[31]))
            self.KeyPointWindow.Diagramm.Acc_T_D[0]           = np.asarray(json.loads(Data[32]))
            self.KeyPointWindow.Diagramm.Acc_T_D[1]           = np.asarray(json.loads(Data[33]))
            self.KeyPointWindow.Diagramm.Vel_T_D[0]           = np.asarray(json.loads(Data[34]))
            self.KeyPointWindow.Diagramm.Vel_T_D[1]           = np.asarray(json.loads(Data[35]))
            self.KeyPointWindow.Diagramm.Pos_T_D[0]           = np.asarray(json.loads(Data[36]))
            self.KeyPointWindow.Diagramm.Pos_T_D[1]           = np.asarray(json.loads(Data[37]))
            self.KeyPointWindow.Diagramm.Vel_P_D[0]           = np.asarray(json.loads(Data[38]))
            self.KeyPointWindow.Diagramm.Vel_P_D[1]           = np.asarray(json.loads(Data[39]))
            self.KeyPointWindow.Diagramm.CP_T_Points[0]       = np.asarray(json.loads(Data[40]))
            self.KeyPointWindow.Diagramm.CP_T_Points[1]       = np.asarray(json.loads(Data[41]))
            self.KeyPointWindow.Diagramm.CP_T_Points[2]       = np.asarray(json.loads(Data[42]))  
            self.KeyPointWindow.Diagramm.CP_P_Points[0]       = np.asarray(json.loads(Data[43]))
            self.KeyPointWindow.Diagramm.CP_P_Points[1]       = np.asarray(json.loads(Data[44]))
            self.KeyPointWindow.Diagramm.CP_P_Points[2]       = np.asarray(json.loads(Data[45]))
            self.KeyPointWindow.Diagramm.CP_M_Points[0]       = np.asarray(json.loads(Data[46]))
            self.KeyPointWindow.Diagramm.CP_M_Points[1]       = np.asarray(json.loads(Data[47]))
            self.KeyPointWindow.Diagramm.CP_M_Points[2]       = np.asarray(json.loads(Data[48]))
            self.KeyPointWindow.Diagramm.Action_Signed        = Data[49]
            self.KeyPointWindow.Diagramm.Action_UsrAcc        = float(Data[50])
            self.KeyPointWindow.Diagramm.Action_UsrVel        = float(Data[51])
            self.KeyPointWindow.Diagramm.Action_UsrLength     = float(Data[52])
            self.KeyPointWindow.Diagramm.Action_Duration      = float(Data[53])
            self.KeyPointWindow.Diagramm.TimeScaling          = float(Data[54])
            self.KeyPointWindow.Diagramm.TimeScalingAbs       = float(Data[55])    
            self.KeyPointWindow.txtName.SetValue            (Data[1])
            self.KeyPointWindow.txtSetupLength.SetValue     ('%3.3f'% float(Data[8]))
            self.KeyPointWindow.txtSetupMaxAcc.SetValue     ('%3.3f'% float(Data[6]))
            self.KeyPointWindow.txtSetupMaxVel.SetValue     ('%3.3f'% float(Data[7]))
            self.KeyPointWindow.txtDescription.SetValue     (Data[19])
            self.KeyPointWindow.txtUsrLength.SetValue       ('%3.3f'% float(Data[52]))
            self.KeyPointWindow.txtUsrAcc.SetValue          ('%3.3f'% float(Data[50]))
            self.KeyPointWindow.txtUsrVel.SetValue          ('%3.3f'% float(Data[51]))
            self.KeyPointWindow.txtSetupTime.SetValue       ('%3.3f'% float(Data[53]))
        elif len(Data) == 15:
            self.KeyPointWindow.Diagramm.Action_ID            = Data[0]
            self.KeyPointWindow.Diagramm.Action_Name          = Data[1]
            self.KeyPointWindow.Diagramm.Action_Saved         = Data[2]
            self.KeyPointWindow.Diagramm.Action_Path          = Data[3]
            self.KeyPointWindow.Diagramm.Action_MinPos        = float(Data[4])
            self.KeyPointWindow.Diagramm.Action_MaxPos        = float(Data[5])
            self.KeyPointWindow.Diagramm.Action_MaxAcc        = float(Data[6])
            self.KeyPointWindow.Diagramm.Action_MaxVel        = float(Data[7])
            self.KeyPointWindow.Diagramm.Action_Length        = float(Data[8])
            self.KeyPointWindow.Diagramm.Action_Description   = Data[14]
            self.KeyPointWindow.Diagramm.Action_UsrAcc        = float(Data[6]) * 0.9
            self.KeyPointWindow.Diagramm.Action_UsrVel        = float(Data[7]) * 0.9
            self.KeyPointWindow.Diagramm.Action_UsrLength     = float(Data[8]) 
            self.KeyPointWindow.Diagramm.Action_Signed        = False
        else:
            dlg = wx.MessageDialog(None,'File can not be decoded','Invalid Data',  wx.OK)
            dlg.ShowModal()
            print('Invalid Data')  
        self.KeyPointWindow.Diagramm.Entry()

if __name__ == "__main__":
    app = VelEditor4C()
    app.MainLoop()