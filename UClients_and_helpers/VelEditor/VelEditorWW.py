import wx
from wx import xrc
import sys

import numpy as np
import matplotlib

import matplotlib.pyplot as plt
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
        return self.Jrk_T_D, self.Acc_T_D, self.Vel_T_D, self.Pos_T_D, self.Vel_P_D 

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

        # for i in range(0,len(self.X)):
        #     v = self.eval_Vel_T_D(self.X[i])
        #     p = self.eval_Pos_T_D(self.X[i])
        #     self.Vel_P_D[0].append(p)
        #     self.Vel_P_D[1].append(v)

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
        
        # self.GrenzDataX = np.linspace(0,10, num=10000, endpoint=True, retstep=False, dtype=np.double)        
        # self.GrenzDataY = np.zeros(10000) 
        
        # self.SBPolyVelTData = np.array([[0,1],[0,1]])
        # self.VelTData       = np.array([[0,1],[0,1]])
        # self.SBPolyAccTData = np.array([[0,1],[0,1]])

        self.Action_ID          = 0
        self.Action_Name        = ''
        self.Action_Saved       = False
        self.Action_Path        = ''
        self.Action_MinPos      = 1.0
        self.Action_MaxPos      = 1.0
        self.Action_MaxAcc      = 1.0
        self.Action_MaxVel      = 1.0
        self.Action_Length      = 1.0
        self.Action_Jrk              = [[],[]]
        self.Action_Acc              = [[],[]]
        self.Action_Vel              = [[],[]]
        self.Action_Vel_Active       = [[],[]]
        self.Action_Pos              = [[],[]]
        self.Action_VelInPos         = [[],[]]
        self.Action_VelInPos_Active  = [[],[]]
        self.Action_Description      = ''
        self.Action_Signed           = False

        self.PrepareGraphs()

    def ClearVars(self):
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
        self.VelDS  = [[],[]]

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

    def Entry(self):
        ''' Setup of Controlpoints and the BPolys'''
        self.ClearVars()        
        self.VelEditorFrame.btnGenerate.Enable(True)
        self.Length = float(self.VelEditorFrame.txtGenerateLength.GetValue())        
        self.Time_Pos_Values      = np.zeros(1000)

        if not(self.Action_Signed):
            self.Jrk_T_D,\
            self.Acc_T_D,\
            self.Vel_T_D,\
            self.Pos_T_D,\
            self.Vel_P_D   = self.Calc_Profile(float(self.VelEditorFrame.txtSetupLength.GetValue()),\
                                               float(self.VelEditorFrame.txtSetupMaxAcc.GetValue()),\
                                               float(self.VelEditorFrame.txtSetupMaxVel.GetValue()))

            self.Samples = len(self.Vel_T_D[0])
            self.X_Time_Values         = np.linspace(0., self.Vel_T_D[0][-1],  self.Samples, dtype= np.double)
            self.X_Pos_Values          = np.linspace(0., self.Length,          self.Samples, dtype= np.double)

            Vel_T_D_S = self.SimplifyProfile(self.Vel_T_D,self.Acc_T_D, 0.01)

            self.VelEditorFrame.txtSetupTime.SetValue(str(Vel_T_D_S[0][-1]))

            self.init_CP_T_Points(Vel_T_D_S)
            self.init_T_BPoly()
            self.init_CP_P_Points(Vel_T_D_S)            
            self.init_P_BPoly()

        else:
            self.X_Pos_Values         = np.linspace(0., self.Length , 1000, dtype= np.double)
            self.init_CP_P_Points(self.Action_VelInPos)
            self.init_P_BPoly()
            self.Time_Pos_Values = self.int_VelInPos_Line()
            self.X_Time_Values   = np.linspace(0., self.Time_Pos_Values[-1] , 1000, dtype= np.double)
            self.VelEditorFrame.txtSetupTime.SetValue(str(self.Time_Pos_Values[-1]))
            self.init_CP_T_Points(self.Action_VelInPos)
            self.init_T_BPoly()

        self.RecalcMove(init = True)
        self.rezoom          = True
        self.Plot(init       = True)

    def GenerateProfile(self,Length, Acc, Vel):
        self.Action_Signed      = False
        self.ClearVars()        
        self.Length = float(self.VelEditorFrame.txtGenerateLength.GetValue())        
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

        self.VelEditorFrame.txtSetupTime.SetValue(str(Vel_T_D_S[0][-1]))

        self.init_CP_T_Points(Vel_T_D_S)
        self.init_T_BPoly()
        self.init_CP_P_Points(Vel_T_D_S)            
        self.init_P_BPoly()

        self.RecalcMove(init = True)
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
        self.CP_T_Points       = self.init_CP_T(T_Points[0], T_Points[1]*0.9, T_Points[2]*0.81)
        self.CP_M_Points       = self.init_CP_T(T_Points[0], T_Points[1]*0.9, T_Points[2]*0.81)

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
        '''BPoly for Vel in P-Domain'''
        if refresh == True:
            yi = [[self.CP_P_Points[1][0],0]]  #self.CP_P_Points[2][0]]]
            for i in range(1,len(self.CP_P_Points[0])):
                yi.append([self.CP_P_Points[1][i],self.CP_P_Points[2][i]])
            order = 3
            if  math.isnan(self.CP_P_Points[0][-1]):
                self.CP_P_Points[0][-1] = self.CP_P_Points[0][-2]+0.0001
            self.CP_P_BPoly = BPoly.from_derivatives(self.CP_P_Points[0],yi,orders = order)

        return self.CP_P_BPoly(x)
     
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
        self.lines += self.axes.plot(self._xInit,self.Null, color="black",              linewidth=1.,  linestyle="-"              , pickradius = 0)   # VelLimit over Pos [0]
        self.lines += self.axes.plot(self._xInit,self.Null, color="darkred",          linewidth=1.0, linestyle="-"              , pickradius = 0)  # Vel  Beziers  [1]
        #self.lines += self.axes.plot(self._xInit,self.Null, color="darkred",            linewidth=1.0, linestyle="-"              , pickradius = 0)  # Vel  Beziers  [1]
        # self.lines += self.axes.plot(self._xInit,self.Null, color="darkgreen",          linewidth=1.0, linestyle="-",pickradius = 0)   # Acc  Beziers  [2]
        # self.lines += self.axes.plot(self._xInit,self.Null, color="darkblue",           linewidth=1.0, linestyle="-.",pickradius = 0)   # Jerk Beziers  [3]
        # self.lines += self.axes.plot(self._xInit,self.Null, color="darkred",            linewidth=1.4, linestyle="-",pickradius = 0)    # Vel           [4]
        # self.lines += self.axes.plot(self._xInit,self.Null, color="darkgreen",          linewidth=1.4, linestyle="-",pickradius = 0)    # Acc           [5]
        # self.lines += self.axes.plot(self._xInit,self.Null, color="darkblue",           linewidth=1.4, linestyle="-",pickradius = 0)   # Jerk          [9]
        
        #self.lines += self.axes.plot(self._xInit,self.Null, color="xkcd:grass green",  linewidth=1.4, linestyle="--",pickradius = 0)  # Unbalanced Vel    [10]
        #self.lines += self.axes.plot(self._xInit,self.Null, color="xkcd:kelly green",  linewidth=1.4, linestyle="--",pickradius = 0)  # Unbalanced Pos    [11]
        #self.lines += self.axes.plot(self._xInit,self.Null, color="black",             linewidth=1.4, linestyle="-",pickradius = 0)   # GrenzVelAccPara   [12]
        #self.lines += self.axes.plot(self._xInit,self.Null, color="black",             linewidth=1.4, linestyle="-.",pickradius = 0)  # GrenzVelAvePara   [13]
        #self.lines += self.axes.plot(self._xInit,self.Null, color="yellow",            linewidth=0.4, linestyle="-",pickradius = 0)  # aus Diff
        #self.lines += self.axes.plot(self._xInit,self.Null, color="green",             linewidth=0.4, linestyle="-",pickradius = 0)  # aus Diff 
        #self.lines += self.axes.plot(self._xInit,self.Null, color="blue",              linewidth=0.4, linestyle="-",pickradius = 0)  # aus Diff 
        
        self.linesT = []
        self.linesT += self.axesT.plot(self._xInit,self.Null,  color="black",           linewidth=1.,  linestyle="-"              ,pickradius = 0)   # VelLimit over Time [0]
        self.linesT += self.axesT.plot(self._xInit,self.Null,  color="darkred",         linewidth=1.0, linestyle="-"              ,pickradius = 0)   # Vel  [0]
        self.linesT += self.axesT.plot(self._xInit,self.Null,  color="darkblue",        linewidth=1.0, linestyle="-"              ,pickradius = 0)  # Pos  Beziers [3]
        
        #self.linesT += self.axesT.plot(self._xInit,self.Null,  color="darkgreen",       linewidth= 0.5, linestyle="-.",pickradius = 0 ) # Vel  Beziers [1]
        self.linesT += self.axesT.plot(self._xInit,self.Null,  color="darkblue",         linewidth= 0.5, linestyle="-.",pickradius = 0)  # Acc  Beziers [2]
        self.linesT += self.axesT.plot(self._xInit,self.Null,  color="black",            linewidth= 0.5, linestyle="-."              , pickradius = 0) # Vel  Points [1]
        
        #self.linesT += self.axesT.plot(self._xInit,self.Null,  color="black",           linewidth=1.5, linestyle="-.",pickradius = 0)   # Vel          [4]
        # self.linesT += self.axesT.plot(self._xInit,self.Null,  color="darkgreen",       linewidth=1.4, linestyle="-",pickradius = 0)   # Acc          [5]
        #self.linesT += self.axesT.plot(self._xInit,self.Null,  color="m",           linewidth=0.8, linestyle="-",pickradius = 0)   # Pos          [6] 

    def Plot(self, init = True):        
        #self.rezoom = True
        self.Refresh()
        self.lines[0].set( xdata = self.Vel_P_Limit[0],    ydata=self.Vel_P_Limit[1])
        self.lines[1].set( xdata = self.Vel_P[0],          ydata=self.Vel_P[1])        
 
        for i in range (len(self.fillP)):
            self.axes.patches.remove(self.fillP[i])
        self.fillP =[]       
        self.fillP =self.axes.fill(self.Vel_P_Limit[0],self.Vel_P_Limit[1], color="lightgreen", alpha = 0.2,)
        self.fillP += self.axes.fill(self.Vel_P[0],self.Vel_P[1], color="lightgreen", alpha = 0.2,)
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

        self.linesT[0].set( xdata = self.Vel_T_Limit[0], ydata=self.Vel_T_Limit[1])
        self.linesT[1].set( xdata = self.Vel_T[0],        ydata=self.Vel_T[1])
        self.linesT[2].set( xdata = self.Acc_T[0],        ydata=self.Acc_T[1])

        #self.linesT[3].set( xdata = self.Jrk_T_D[0],        ydata=self.Jrk_T_D[1])
        self.linesT[3].set( xdata = self.Acc_T_D[0],        ydata=self.Acc_T_D[1])
        self.linesT[4].set( xdata = self.Vel_T_D[0],        ydata=self.Vel_T_D[1])
        #self.linesT[6].set( xdata = self.Pos_T_D[0],        ydata=self.Pos_T_D[1])
          

        for i in range (len(self.fillT)):
            self.axesT.patches.remove(self.fillT[i])
        self.fillT =[] 
        self.fillT += self.axesT.fill(self.Vel_T_Limit[0], self.Vel_T_Limit[1] , color="lightgreen", alpha = 0.2,)               
        self.fillT += self.axesT.fill(self.Vel_T[0],       self.Vel_T[1],        color="lightgreen", alpha = 0.2,)
        if init:
            for i in range(len(self.VelInTime_markers)):
                self.axesT.lines.remove(self.VelInTime_markers[i])
                self.axesT.lines.remove(self.VelInTime_tangents[i])
            self.VelInTime_markers  = []
            self.VelInTime_tangents = []
            for i in range(0,len(self.CP_T_Points[0])):
                s = 0.1 * self.scaleT * math.sin(math.atan(self.CP_T_Points[2][i]))
                c = 0.1 * self.scaleT * math.cos(math.atan(self.CP_T_Points[2][i]))
                x_data = [(self.CP_T_Points[0][i] - c),(self.CP_T_Points[0][i] + c)]
                y_data = [(self.CP_T_Points[1][i] - s),(self.CP_T_Points[1][i] + s)]
                self.VelInTime_markers  += self.axesT.plot(self.CP_T_Points[0][i],self.CP_T_Points[1][i],marker ='x',markersize = 7*self.scaleT , color = 'darkred')
                self.VelInTime_tangents += self.axesT.plot(x_data,y_data, linewidth=1.0, linestyle="-",  marker ='o',markersize = 3*self.scaleT , color = 'g', fillstyle = 'none')
        else:
            for i in range(len(self.VelInTime_markers)):
                s = 0.1 * self.scaleT * math.sin(math.atan(self.CP_T_Points[2][i]))
                c = 0.1 * self.scaleT * math.cos(math.atan(self.CP_T_Points[2][i]))
                x_data = [(self.CP_T_Points[0][i] - c),(self.CP_T_Points[0][i] + c)]
                y_data = [(self.CP_T_Points[1][i] - s),(self.CP_T_Points[1][i] + s)]
                self.VelInTime_markers[i].set(xdata=self.CP_T_Points[0][i],ydata=self.CP_T_Points[1][i])
                self.VelInTime_tangents[i].set(xdata=x_data,ydata=y_data)

    def OnPaint(self,evt):
        if  self.rezoom == True:  
            minlimx = self.CP_P_Points[0][0]-0.05 
            maxlimx = self.CP_P_Points[0][-1]+0.05
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
                    if self.VelInTime_tangents[i].contains(evt)[0]:
                        self.hpoint=i
                        self.ThpointX = self.VelInTime_tangents[self.hpoint].get_xdata()
                        self.ThpointY = self.VelInTime_tangents[self.hpoint].get_ydata()
                        self.VelInTime_tangents[self.hpoint].set( color='b')
                        self.modifyP = 'TTangentPoint'
                        break
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
        MarkerX = (self.ThpointX[0]+self.ThpointX[1])/2.0
        MarkerY = (self.ThpointY[0]+self.ThpointY[1])/2.0
        if self.clickpoint[0]< self.CP_T_Points[0][self.hpoint] :
            #Left
            VPX =(self.ThpointX[0]-self.MouseDeltaXPoint) - MarkerX
            VPY =(self.ThpointY[0]-self.MouseDeltaYPoint) - MarkerY 
            k = VPY/VPX 
        else: 
            #Right
            VPX =(self.ThpointX[0]+self.MouseDeltaXPoint) - MarkerX
            VPY =(self.ThpointY[0]+self.MouseDeltaYPoint) - MarkerY 
            k = VPY/VPX 
        self.CP_T_Points[2][self.hpoint] = k
        self.CP_M_Points[2][self.hpoint] = k
        self.RecalcMove(init = False)
        self.Refresh()
        self.Plot(init = False)
        #self.rezoom = True
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
            pass

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

        for i in range(1,len(self.CP_P_Points[0])-1):
           self.CP_P_Points[2][i]=(self.CP_P_Points[1][i+1]-self.CP_P_Points[1][i-1])/(self.CP_P_Points[0][i+1]-self.CP_P_Points[0][i-1])

        self.Vel_P[0] = self.X_Pos_Values
        self.Vel_P[1] = self.eval_CP_P_Points(self.X_Pos_Values,True)

        if self.VelEditorFrame.chkAccSmooth.GetValue():	
            for i in range(1,len(self.CP_T_Points[0])-1):
                self.CP_T_Points[2][i]=(self.CP_T_Points[1][i+1]-self.CP_T_Points[1][i-1])/(self.CP_T_Points[0][i+1]-self.CP_T_Points[0][i-1])

        self.Vel_T[0] = self.X_Time_Values
        self.Vel_T[1] = self.eval_CP_T_Points(self.X_Time_Values,True)

        self.Vel_T_Limit[0]= self.Vel_T_D[0] * self.TimeScalingAbs
        self.Vel_T_Limit[1]= self.Vel_T_D[1]

        pdt  = self.CP_T_BPoly.derivative(1)
        self.Acc_T[0] = self.X_Time_Values
        self.Acc_T[1] = pdt(self.X_Time_Values)

        if self.VelEditorFrame:
            maxAcc = max(self.Acc_T[1])
            maxDcc = min(self.Acc_T[1])
            self.VelEditorFrame.txtGenerateDuration.SetValue('%3.3f'% self.CP_M_Points[0][-1])
            self.VelEditorFrame.txtGenerateTimeFactor.SetValue('%3.3f'% self.TimeScalingAbs)
            self.VelEditorFrame.txtProfileMaxAcc.SetValue('%3.3f'% maxAcc)
            self.VelEditorFrame.txtProfileMaxDcc.SetValue('%3.3f'% maxDcc)
            if maxAcc < 0.7 * float(self.Action_MaxAcc):
                self.VelEditorFrame.txtProfileMaxAcc.SetBackgroundColour((0,204,0))
            elif maxAcc < 0.9 * float(self.Action_MaxAcc):
                self.VelEditorFrame.txtProfileMaxAcc.SetBackgroundColour((255,128,0))
            else:
                self.VelEditorFrame.txtProfileMaxAcc.SetBackgroundColour((204,0,0))
            if abs(maxDcc) < 0.7 * float(self.Action_MaxAcc):
                self.VelEditorFrame.txtProfileMaxDcc.SetBackgroundColour((0,204,0))
            elif abs(maxDcc) < 0.9 * float(self.Action_MaxAcc):
                self.VelEditorFrame.txtProfileMaxDcc.SetBackgroundColour((255,128,0))
            else:
                self.VelEditorFrame.txtProfileMaxDcc.SetBackgroundColour((204,0,0))

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
            self.VelInTime_tangents[self.hpoint].set(color='g')
        self.modifyP = 'none'
        self.Refresh()

    def OnKeyPress(self,evt):
        if evt.key == 'd':
            if (self.modifyP == 'TPoint' or self.modifyP == 'PPoint') and len(self.CP_P_Points[0]) >= 4:                
                self.CP_P_Points = np.delete(self.CP_P_Points,self.hpoint,axis=1)
                self.CP_T_Points = np.delete(self.CP_T_Points,self.hpoint,axis=1)
                self.CP_M_Points = np.delete(self.CP_M_Points,self.hpoint,axis=1)
                self.modifyP = 'none'
                self.RecalcMove(init = False)
                self.Plot(init = True)
                self.Refresh()                
        elif evt.key == 'i' and self.modifyP == 'TI':
            if self.clickpoint[0] > 0.1:
                y = self.eval_CP_M_Points(self.clickpoint[0],False)
                i = np.searchsorted(self.CP_M_Points[0],self.clickpoint[0])
                self.CP_M_Points = np.insert(self.CP_M_Points,i,[self.clickpoint[0],y,0],axis =1)
                self.CP_T_Points = np.insert(self.CP_T_Points,i,[self.clickpoint[0],y,0],axis =1)
                self.CP_P_Points = np.insert(self.T_2_P(self.CP_P_Points),i,[self.clickpoint[0],y,0],axis =1)
                self.RecalcMove(init = False)
                self.Plot(init = True)
                self.Refresh()                
        elif evt.key == 'i' and self.modifyP == 'PI':
            pass
            if self.clickpoint[0] > 0.1:
                y = self.eval_CP_P_Points((self.clickpoint[0]),False)
                i = np.searchsorted(self.CP_M_Points[0],self.P_2_T(self.clickpoint[0]))
                self.CP_M_Points = np.insert(self.CP_M_Points,i,[self.P_2_T(self.clickpoint[0]),y,0],axis =1)
                self.CP_T_Points = np.insert(self.CP_T_Points,i,[self.P_2_T(self.clickpoint[0]),y,0],axis =1)
                self.CP_P_Points = np.insert(self.CP_P_Points,i,[self.clickpoint[0],y,0],axis =1)
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
        self.KeyPointWindow.txtGenerateAcc        = xrc.XRCCTRL(self.KeyPointWindow,'txtGenerateAcc')
        self.KeyPointWindow.txtGenerateVel        = xrc.XRCCTRL(self.KeyPointWindow,'txtGenerateVel')
        self.KeyPointWindow.txtGenerateLength     = xrc.XRCCTRL(self.KeyPointWindow,'txtGenerateLength')
        self.KeyPointWindow.txtGenerateDuration   = xrc.XRCCTRL(self.KeyPointWindow,'txtGenerateDuration')
        self.KeyPointWindow.txtMouseXPos          = xrc.XRCCTRL(self.KeyPointWindow,'txtMouseXPos')
        self.KeyPointWindow.txtMouseYPos          = xrc.XRCCTRL(self.KeyPointWindow,'txtMouseYPos')
        self.KeyPointWindow.txtProfileMaxAcc      = xrc.XRCCTRL(self.KeyPointWindow,'txtProfileMaxAcc')
        self.KeyPointWindow.txtProfileMaxDcc      = xrc.XRCCTRL(self.KeyPointWindow,'txtProfileMaxDcc')
        self.KeyPointWindow.btnGenerate           = xrc.XRCCTRL(self.KeyPointWindow,'btnGenerate')
        self.KeyPointWindow.txtGenerateTimeFactor = xrc.XRCCTRL(self.KeyPointWindow,'txtGenerateTimeFactor')  
        self.KeyPointWindow.chkAccSmooth          = xrc.XRCCTRL(self.KeyPointWindow,'chkAccSmooth')
        self.KeyPointWindow.chkAutoLimit          = xrc.XRCCTRL(self.KeyPointWindow,'chkAutoLimit')
        self.KeyPointWindow.btnSign               = xrc.XRCCTRL(self.KeyPointWindow,'btnSign')

        #self.KeyPointWindow.txtMaxTime.Enable(False)
        self.KeyPointWindow.txtMouseXPos.Enable(False)
        self.KeyPointWindow.txtMouseYPos.Enable(False)
        self.KeyPointWindow.btnGenerate.Enable(False)
        
        self.Bind(wx.EVT_BUTTON        , self.OnButtonGenerate,      self.KeyPointWindow.btnGenerate)
        self.Bind(wx.EVT_BUTTON        , self.OnButtonSign,          self.KeyPointWindow.btnSign)
        self.Bind(wx.EVT_CHECKBOX      , self.OnAccSmooth,           self.KeyPointWindow.chkAccSmooth)


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
        
        # Probleme mit Debug Modus GUI von matplotlib ... daher mal auskomentiert
        #self.Bind(wx.EVT_KILL_FOCUS, self.EntertxtMaxTime,          self.KeyPointWindow.txtMaxTime)
        #self.Bind(wx.EVT_KILL_FOCUS, self.EntertxtSetupMaxAcc,      self.KeyPointWindow.txtSetupMaxAcc)
        #self.Bind(wx.EVT_KILL_FOCUS, self.EntertxtSetupMaxVel,      self.KeyPointWindow.txtSetupMaxVel)
        #self.Bind(wx.EVT_KILL_FOCUS, self.EntertxtSetupUsrAcc,      self.KeyPointWindow.txtSetupUsrAcc)
        #self.Bind(wx.EVT_KILL_FOCUS, self.EntertxtSetupUsrVel,      self.KeyPointWindow.txtSetupUsrVel)        

        self.KeyPointWindow.Show()

        return True
    def OnButtonSign(self,evt):
        print('Signing')
        pass

    def OnButtonGenerate(self,evt):
        self.KeyPointWindow.Diagramm.GenerateProfile(float(self.KeyPointWindow.txtGenerateLength.GetValue()),\
                                                     float(self.KeyPointWindow.txtGenerateAcc.GetValue()),\
                                                     float(self.KeyPointWindow.txtGenerateVel.GetValue()))
        pass

    def OnAccSmooth(self,evt):
        print('Smooth')
        self.KeyPointWindow.Diagramm.RecalcMove(False)
        self.KeyPointWindow.Diagramm.Plot(init = False)
        
    def OpenFile(self,evt):
        with wx.FileDialog(None, "Open Vel file", wildcard="Vel files (*.sfxact)|*.sfxact",
                       style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return     # the user changed their mind

            # Proceed loading the file chosen by the user
            pathname = fileDialog.GetPath()
            try:
                with open(pathname, 'r', encoding='utf-8') as file:
                    self.LoadFile(file)
            except IOError:
                wx.LogError("Cannot open file '%s'." % newfile)

    def SaveFile(self,evt):
        with wx.FileDialog(self, "Save Vel file", wildcard="Vel files (*.sfxact)|*.sfxact",
                       style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return     # the user changed their mind

            # save the current contents in the file
            pathname = fileDialog.GetPath()
            try:
                with open(pathname, 'w') as file:
                    self.doSaveData(file)
            except IOError:
                wx.LogError("Cannot save current data in file '%s'." % pathname)

    def Exit(self,evt):
        sys.exit()

    def LoadFile(self,file):
        data = file.read()
        file.close()
        Data = data.split(';')
        self.KeyPointWindow.Diagramm.Action_ID          = Data[0]
        self.KeyPointWindow.Diagramm.Action_Name        = Data[1]
        self.KeyPointWindow.Diagramm.Action_Saved       = Data[2]
        self.KeyPointWindow.Diagramm.Action_Path        = Data[3]
        self.KeyPointWindow.Diagramm.Action_MinPos      = Data[4]
        self.KeyPointWindow.Diagramm.Action_MaxPos      = Data[5]
        self.KeyPointWindow.Diagramm.Action_MaxAcc      = Data[6]
        self.KeyPointWindow.Diagramm.Action_MaxVel      = Data[7]
        self.KeyPointWindow.Diagramm.Action_Length      = Data[8]
        self.KeyPointWindow.Diagramm.Action_Jrk         = np.asarray(json.loads(Data[9]))
        self.KeyPointWindow.Diagramm.Action_Acc         = np.asarray(json.loads(Data[10]))
        self.KeyPointWindow.Diagramm.Action_Vel         = np.asarray(json.loads(Data[11]))
        self.KeyPointWindow.Diagramm.Action_Pos         = np.asarray(json.loads(Data[12]))
        self.KeyPointWindow.Diagramm.Action_VelInPos    = np.asarray(json.loads(Data[13]))
        self.KeyPointWindow.Diagramm.Action_Description = Data[14]
        self.KeyPointWindow.Diagramm.Action_Signed      = False

        self.KeyPointWindow.txtSetupLength.SetValue     ('%3.3f'% float(Data[8]))
        self.KeyPointWindow.txtSetupMaxAcc.SetValue('%3.3f'% float(Data[6]))
        self.KeyPointWindow.txtSetupMaxVel.SetValue('%3.3f'% float(Data[7]))

        self.KeyPointWindow.Diagramm.Entry()

if __name__ == "__main__":
    app = VelEditor4C()
    app.MainLoop()