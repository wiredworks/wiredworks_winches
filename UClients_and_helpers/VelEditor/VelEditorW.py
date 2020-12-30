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

from simplification.cutil import (
    simplify_coords,
    simplify_coords_idx,
    simplify_coords_vw,
    simplify_coords_vw_idx,
    simplify_coords_vwp,
)

import math
from math import copysign

import time
import os
import copy

import pickle
import json

ID_Menu_OpenVelFile = 5005
ID_Menu_SaveVelFile = 5006
ID_Menu_Exit        = 5008
ID_Menu             = 5011

class Simplify:
    def __init__(self):
        pass
    
    def main(self, Kurve, error):
        splineVerts = []
        for i in range(0, len(Kurve[0])):
            splineVerts.append(np.array([Kurve[0][i],Kurve[1][i]]))
        newVerts = self.Visvalingam(splineVerts, error)
        return newVerts

    def Visvalingam(self,splineVerts, error):
        return simplify_coords_idx(splineVerts, 0.01)

class Calc_Default_Profile:
    def __init__(self, length, maxAcc, maxVel):
        self.Length     = length
        self.accS        = maxAcc
        self.velS       = maxVel
        self.JH         = 10.0 
        self.JerkD      = [[],[]]
        self.AccD       = [[],[]]
        self.VelD       = [[],[]]
        self.PosD       = [[],[]]

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
        return self.JerkD, self.AccD, self.VelD, self.PosD 

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
        
        print( 'Delta JH: %3.4f Delta Acc: %3.4f Adjusted Vel: %3.4f'%(JerkHeightS-JerkHeight,accS-acc,velS-vel))                            
        print( '                  With Acc: %3.4f      and Vel: %3.4f ---> Time: %3.4f Length: %3.4f'%(acc , vel, Time, Length))
       
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
        f = interp1d(self.JerkD[0],self.JerkD[1], kind ='linear')
        return f(x)

    def CalcDrawFcurves(self):
        self.AccD[0].append(0)
        self.AccD[1].append(0) 
        for i in range(1, len(self.X)):
            self.AccD[0].append(self.X[i])
            self.JrkC[i] = self.interp_Jerk(self.X[i])
            self.AccD[1].append( self.AccD[1][-1] + self.JrkC[i] * (self.X[i]-self.X[i-1]))
 
        self.VelD[0].append(0)
        self.VelD[1].append(0) 
        for i in range(1, len(self.X)):
            self.VelD[0].append(self.X[i])
            self.VelD[1].append( self.VelD[1][-1] + self.AccD[1][i] * (self.X[i]-self.X[i-1]))
           
        self.PosD[0].append(0)
        self.PosD[1].append(0) 
        for i in range(1, len(self.X)):
            self.PosD[0].append(self.X[i])
            self.PosD[1].append( self.PosD[1][-1] + self.VelD[1][i] * (self.X[i]-self.X[i-1]))

        # VelPos.keyframe_points.insert( 0 , 0)
        # VelPos.keyframe_points[0].handle_left   = (VelPos.keyframe_points[0].co[0],-10)
        # VelPos.keyframe_points[0].handle_right  = (VelPos.keyframe_points[0].co[0],10)
        # for i in range(0,len(self.X)):
        #     v = Velcurve.evaluate(self.X[i])
        #     p = Poscurve.evaluate(self.X[i])
        #     if p > 0.015:
        #         VelPos.keyframe_points.insert( p , v)
        # VelPos.keyframe_points[-1].handle_left   = (VelPos.keyframe_points[-1].co[0],10)
        # VelPos.keyframe_points[-1].handle_right  = (VelPos.keyframe_points[-1].co[0],-10)
        
        # self.maxJrk = max(abs(self.JrkC))
        # self.maxAcc = max(abs(self.AccC))
        # self.maxVel = max((self.VelC))
        # self.maxPos = max(abs(self.PosC))
        # self.maxTime = self.X[-1]
            
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

        self.JerkD[0].append(Jert0)
        self.JerkD[1].append(Jer0)
        self.JerkD[0].append(Jert1)
        self.JerkD[1].append(Jer1)
        self.JerkD[0].append(Jert2)
        self.JerkD[1].append(Jer2)
        self.JerkD[0].append(Jert3)
        self.JerkD[1].append(Jer3)


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
        
        self.MDDX = 0.
        self.MDDY = 0.
        
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

        self.JrkD   = [[],[]]
        self.AccD   = [[],[]]
        self.VelD   = [[],[]]
        self.PosD   = [[],[]]
        self.VelDS  = [[],[]]

        self.TimeScaling =1.0
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
        if not(self.Action_Signed):
            self.VelEditorFrame.btnGenerate.Enable(True)

        self.ClearVars()
        self.Length               = self.Action_VelInPos[0][-1]
        self.X_Pos_Values         = np.linspace(0., self.Length , 1000, dtype= np.double)
        self.Time_Pos_Values      = np.zeros(1000)
        self.init_CP_P_Points()
        self.init_P_BPoly()
        # Integrate Vel in Pos; 1st Step to get PosToTime interpolation
        self.Time_Pos_Values = self.int_VelInPos_Line()
        self.X_Time_Values   = np.linspace(0., self.Time_Pos_Values[-1] , 1000, dtype= np.double)
        self.init_CP_T_Points()
        self.init_T_BPoly()
        self.RecalcMove(init = True)
        self.rezoom               = True
        self.Plot(init = True)

    def Calc_Default_Profile(self):   
        A = Calc_Default_Profile(float(self.VelEditorFrame.txtGenerateLength.GetValue()),float(self.VelEditorFrame.txtGenerateAcc.GetValue()),
                                 float(self.VelEditorFrame.txtGenerateVel.GetValue())*0.9)
        self.JrkD, self.AccD, self.VelD, self.PosD = A.GetData()
        B = Simplify()
        T =time.time_ns()
        c = B.main(self.VelD, .01)
        print((time.time_ns()-T)/1000000000)
        for i in range(0,len(c)-1):
            self.VelDS[0].append(self.VelD[0][c[i]])
            self.VelDS[1].append(self.VelD[1][c[i]])

        self.rezoom               = True
        self.Plot(init = True)        

    def init_CP_P_Points(self):
        '''Init the Controlpoints in P-Domain'''
        self.init_CP_P_Limit()
        self.init_CP_P()

    def init_CP_P_Limit(self):
        ''' Init Limits in P-Domain'''
        self.CP_P_Points_Limit[0] = copy.copy(self.Action_VelInPos[0])
        self.CP_P_Points_Limit[1] = copy.copy(self.Action_VelInPos[1])
        k = (self.CP_P_Points_Limit[1][1]-self.CP_P_Points_Limit[1][0])/(self.CP_P_Points_Limit[0][1]-self.CP_P_Points_Limit[0][0])
        self.CP_P_Points_Limit[2].append(k)    
        for i in range (1,len(self.CP_P_Points_Limit[0])):
            k= (self.CP_P_Points_Limit[1][i]-self.CP_P_Points_Limit[1][i-1])/(self.CP_P_Points_Limit[0][i]-self.CP_P_Points_Limit[0][i-1])
            self.CP_P_Points_Limit[2].append(k)

    def init_CP_P(self):
        ''' Init Controlpoints in P_Domain'''
        self.CP_P_Points[0]       = copy.copy(self.Action_VelInPos[0])
        self.CP_P_Points[1]       = copy.copy(self.Action_VelInPos[1]*0.9)
        k = (self.CP_P_Points[1][1]-self.CP_P_Points[1][0])/(self.CP_P_Points[0][1]-self.CP_P_Points[0][0])
        self.CP_P_Points[2].append(k)    
        for i in range (1,len(self.CP_P_Points[0])):
            k= (self.CP_P_Points[1][i]-self.CP_P_Points[1][i-1])/(self.CP_P_Points[0][i]-self.CP_P_Points[0][i-1])
            self.CP_P_Points[2].append(k)

    def init_P_BPoly(self):
        ''' Init BPolys in P-Domain'''
        x  = self.eval_Grenz_P_Points(0.1,True)
        y  = self.eval_CP_P_Points(0.1,True)

    def int_VelInPos_Line(self):
        ''' Integrate Vel over Pos to find out when a Pos is reached''' 
        T_P_Values =[]
        T_P_Values.append(0)
        ST = 0       
        for i in range(1,1000):
            T = abs(self.X_Pos_Values[i-1]-self.X_Pos_Values[i])/\
            ((self.eval_CP_P_Points(self.X_Pos_Values[i-1],False)+self.eval_CP_P_Points(self.X_Pos_Values[i],False))/2)
            ST = ST + T
            T_P_Values.append(ST) 
        return T_P_Values

    def init_CP_T_Points(self):
        '''Init Controlpoints in T-Domain'''
        self.init_CP_M()
        self.init_CP_T()
        self.init_CP_T_Limit()

    def init_CP_M(self):
        ''' Init Master Controlpoint in T-Domain'''
        self.CP_M_Points[0]       = self.eval_PosToTime_Line(copy.copy(self.Action_VelInPos[0]))
        self.CP_M_Points[1]       = copy.copy(self.Action_VelInPos[1]*0.9)
        k = (self.CP_M_Points[1][1]-self.CP_M_Points[1][0])/(self.CP_M_Points[0][1]-self.CP_M_Points[0][0])
        self.CP_M_Points[2].append(k)    
        for i in range (1,len(self.CP_M_Points[0])):
            k= (self.CP_M_Points[1][i]-self.CP_M_Points[1][i-1])/(self.CP_M_Points[0][i]-self.CP_M_Points[0][i-1])
            self.CP_M_Points[2].append(k) 
        self.CP_M_Points[2][0] =0.0
        self.CP_M_Points[2][-1]=0.0

    def init_CP_T(self):
        '''Init Vel in T-Domain'''
        self.CP_T_Points[0]       = self.eval_PosToTime_Line(self.CP_P_Points[0])
        self.CP_T_Points[1]       = self.CP_P_Points[1]
        k = (self.CP_T_Points[1][1]-self.CP_T_Points[1][0])/(self.CP_T_Points[0][1]-self.CP_T_Points[0][0])
        self.CP_T_Points[2].append(k)    
        for i in range (1,len(self.CP_T_Points[0])):
            k= (self.CP_T_Points[1][i]-self.CP_T_Points[1][i-1])/(self.CP_T_Points[0][i]-self.CP_T_Points[0][i-1])
            self.CP_T_Points[2].append(k) 
        self.CP_T_Points[2][0] =0.0
        self.CP_T_Points[2][-1]=0.0

    def init_CP_T_Limit(self):
        '''Init Vel Limits In T-Domain'''
        self.CP_T_Points_Limit[0]       = self.eval_PosToTime_Line(self.CP_P_Points_Limit[0]) * self.TimeScaling
        self.CP_T_Points_Limit[1]       = self.CP_P_Points_Limit[1]
        k = (self.CP_T_Points_Limit[1][1]-self.CP_T_Points_Limit[1][0])/(self.CP_T_Points_Limit[0][1]-self.CP_T_Points_Limit[0][0])
        self.CP_T_Points_Limit[2].append(k)    
        for i in range (1,len(self.CP_T_Points_Limit[0])):
            k= (self.CP_T_Points_Limit[1][i]-self.CP_T_Points_Limit[1][i-1])/(self.CP_T_Points_Limit[0][i]-self.CP_T_Points_Limit[0][i-1])
            self.CP_T_Points_Limit[2].append(k) 
        self.CP_T_Points_Limit[2][0] =0
        self.CP_T_Points_Limit[2][-1]=0.0

    def init_T_BPoly(self):
        '''Init BPolys in T-Domain'''
        u  = self.eval_Grenz_T_Points(0.1,True)
        v  = self.eval_CP_T_Points(0.1,True)
        w  = self.eval_CP_M_Points(0.1,True)

    def eval_Grenz_P_Points(self,x,refresh):
        '''BPoly for Grenz_P_Points'''
        if refresh == True:
            yi = [[self.CP_P_Points_Limit[1][0],self.CP_P_Points_Limit[2][0]]]
            for i in range(1,len(self.CP_P_Points_Limit[0])):
                yi.append([self.CP_P_Points_Limit[1][i],self.CP_P_Points_Limit[2][i]])
            order = 3
            self.Grenz_P_BPoly = BPoly.from_derivatives(self.CP_P_Points_Limit[0],yi,orders = order)
        return self.Grenz_P_BPoly(x)

    def eval_CP_P_Points(self,x,refresh):
        '''BPoly for Vel in P-Domain'''
        if refresh == True:
            yi = [[self.CP_P_Points[1][0],self.CP_P_Points[2][0]]]
            for i in range(1,len(self.CP_P_Points[0])):
                yi.append([self.CP_P_Points[1][i],self.CP_P_Points[2][i]])
            order = 3
            self.CP_P_BPoly = BPoly.from_derivatives(self.CP_P_Points[0],yi,orders = order)
            self.int_VelInPos_Line()
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

    def eval_Grenz_T_Points(self,x,refresh):
        ''' BPoly für Vel Limit in T-Domain'''
        if refresh:
            order = 3
            yi = [[self.CP_T_Points_Limit[1][0],self.CP_T_Points_Limit[2][0]]]
            for i in range (1,len(self.CP_T_Points_Limit[0])):
                k= (self.CP_T_Points_Limit[1][i]-self.CP_T_Points_Limit[1][i-1])/(self.CP_T_Points_Limit[0][i]-self.CP_T_Points_Limit[0][i-1])
                yi.append([self.CP_T_Points_Limit[1][i],k])
            self.Grenz_T_BPoly =BPoly.from_derivatives(self.CP_T_Points_Limit[0] * self.TimeScaling,yi,orders = order)
        return self.Grenz_T_BPoly(x)

    def int_VelInTime_Line(self):
        ST = 0       
        for i in range(1,1000):
            T = abs(self.X_Time_Values[i-1]-self.X_Time_Values[i])*\
            ((self.eval_CP_T_Points(self.X_Time_Values[i-1],False)+self.eval_CP_T_Points(self.X_Time_Values[i],False))/2)
            ST = ST + T
        self.Time_Pos_Values[i] = ST

    # Interpolation der TimeInPos_Line
    def eval_TimeToPos_Line(self,x):
        #print(self.Time_Pos_Values)
        f=interp1d(self.X_Time_Values,self.Time_Pos_Values, kind ='slinear',bounds_error=False, fill_value=np.nan)
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
        # self.lines += self.axes.plot(self._xInit,self.Null, color="darkred",            linewidth=1.0, linestyle="-"              , pickradius = 0)  # Vel  Beziers  [1]
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
        
        self.linesT += self.axesT.plot(self._xInit,self.Null,  color="darkgreen",       linewidth=1.5, linestyle="-."              , pickradius = 0) # Vel  Points [1]
        self.linesT += self.axesT.plot(self._xInit,self.Null,  color="darkred",         linewidth=1.5, linestyle="-.",pickradius = 0 ) # Vel  Beziers [1]
        self.linesT += self.axesT.plot(self._xInit,self.Null,  color="black",           linewidth=1.5, linestyle="-.",pickradius = 0)  # Acc  Beziers [2]
        self.linesT += self.axesT.plot(self._xInit,self.Null,  color="black",           linewidth=1.5, linestyle="-.",pickradius = 0)   # Vel          [4]
        # self.linesT += self.axesT.plot(self._xInit,self.Null,  color="darkgreen",       linewidth=1.4, linestyle="-",pickradius = 0)   # Acc          [5]
        self.linesT += self.axesT.plot(self._xInit,self.Null,  color="m",           linewidth=0.8, linestyle="-",pickradius = 0)   # Pos          [6] 

    def Plot(self, init = True):        
        #self.rezoom = True
        self.Refresh()
        self.lines[0].set( xdata = self.Vel_P_Limit[0], ydata=self.Vel_P_Limit[1])
        self.lines[1].set( xdata = self.Vel_P[0], ydata=self.Vel_P[1])
 
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

        #self.linesT[0].set( xdata = self.Vel_T_Limit[0], ydata=self.Vel_T_Limit[1])
        #self.linesT[1].set( xdata = self.Vel_T[0],        ydata=self.Vel_T[1])
        #self.linesT[2].set( xdata = self.Acc_T[0],        ydata=self.Acc_T[1])

        #self.linesT[3].set( xdata = self.JrkD[0],        ydata=self.JrkD[1])
        #self.linesT[4].set( xdata = self.AccD[0],        ydata=self.AccD[1])
        #self.linesT[5].set( xdata = self.VelD[0],        ydata=self.VelD[1])
        #self.linesT[6].set( xdata = self.PosD[0],        ydata=self.PosD[1]) 
        self.linesT[0].set( xdata = self.VelDS[0],       ydata=self.VelDS[1]) 
        self.axesT.plot(self.VelDS[0],self.VelDS[1],marker ='o',markersize = 7*self.scaleP , color = 'darkred')                

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
            m = np.amax(self.Action_VelInPos[1]) 
            self.axes.set_ylim(-0.5,m*1.1)
        if self.modifyP == 'TPoint' or self.rezoom == True:
            minlimTx = self.CP_T_Points_Limit[0][0]-0.05
            maxlimTx = self.CP_T_Points_Limit[0][-1]+0.05
            self.axesT.set_xlim(minlimTx,maxlimTx)
            m = np.amax(self.Action_Vel[1]) 
            self.axesT.set_ylim(-0.5,m*1.1)
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
                self.MDDX = MDX
            else:
                flag = 'exit' 
                if MDX < 0 :
                    x= x3-0.2
                else:
                    x= x1+0.2
            if (self.eval_Grenz_T_Points(x,False) > self.ThpointY-MDY):
                y= max((self.ThpointY-MDY),0)
                self.MDDY = MDY
            else:
                flag = 'exit'
                y = max((self.eval_Grenz_T_Points(x,False)),0) 
                self.MDDY = MDY                
            if flag == 'exit':
                self.modifyP == 'none'               
                self.VelInTime_markers[self.hpoint].set(color='r')
                
            self.CP_M_Points[0][self.hpoint] = x
            self.CP_M_Points[1][self.hpoint] = y
            
            self.RecalcMove(init = False)

            self.Refresh()
            self.rezoom = False
            self.Plot(init = False)
            
            
            #wx.PostEvent(self,wx.PaintEvent()) 
       
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
                        self.PhpointX = self.CP_P_Points[0][self.hpoint]
                        self.PhpointY = self.CP_P_Points[1][self.hpoint]
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
            self.MDDX = 0.
            self.MDDY = 0.
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
                    self.MDDX = MDX
                else:
                    flag = 'exit' 
                    if MDX < 0 :
                        x= x3-0.2
                    else:
                        x= x1+0.2
                if (self.eval_Grenz_P_Points(x,False) > self.PhpointY-MDY ):
                    y=max((self.PhpointY-MDY),0.1)
                    self.MDDY = MDY
                else:
                    flag = 'exit'
                    y = max(self.eval_Grenz_P_Points(x,False),0.1) 
                    self.MDDY = MDY                
                if flag == 'exit':
                    self.modifyP == 'none'               
                    self.VelInPos_markers[self.hpoint].set(color='r')
                if (self.eval_PosToTime_Line(x) > self.CP_M_Points[0][self.hpoint-1] and
                    self.eval_PosToTime_Line(x) < self.CP_M_Points[0][self.hpoint+1]):
                    self.CP_M_Points[0][self.hpoint] = self.eval_PosToTime_Line(x)
                    self.CP_M_Points[1][self.hpoint] = y
                
                self.RecalcMove(init = False)

                self.Plot(init = False)
                self.rezoom = True    
                self.Refresh()

    def RecalcMove(self, init):
        if init:
            self.Vel_P_Limit[0] = self.X_Pos_Values
            self.Vel_P_Limit[1] = self.eval_Grenz_P_Points(self.X_Pos_Values,False)

        u = self.eval_CP_M_Points(0.1,True)
        pint = self.CP_M_BPoly.antiderivative(1)
        
        PosI = pint(self.CP_T_Points[0][-1])
        self.TimeScaling    = self.CP_P_Points_Limit[0][-1]/PosI
        self.X_Time_Values         = self.X_Time_Values        * self.TimeScaling
        self.CP_M_Points[0]        = self.CP_M_Points[0]       * self.TimeScaling
        self.CP_T_Points_Limit[0]  = self.CP_T_Points_Limit[0] * self.TimeScaling
        u = self.eval_CP_M_Points(0.1,True)

        self.CP_T_Points[0] = self.CP_M_Points[0]
        self.CP_T_Points[1] = self.CP_M_Points[1]
        # for i in range(1,len(self.CP_T_Points[0])-1):
        #     self.CP_T_Points[2][i]=(self.CP_T_Points[1][i+1]-self.CP_T_Points[1][i-1])/(self.CP_T_Points[0][i+1]-self.CP_T_Points[0][i-1])
        self.CP_P_Points[0] = pint(self.CP_M_Points[0])
        self.CP_P_Points[1] = self.CP_M_Points[1]
        for i in range(1,len(self.CP_P_Points[0])-1):
            self.CP_P_Points[2][i]=(self.CP_P_Points[1][i+1]-self.CP_P_Points[1][i-1])/(self.CP_P_Points[0][i+1]-self.CP_P_Points[0][i-1])

        self.Vel_P[0] = self.X_Pos_Values
        self.Vel_P[1] = self.eval_CP_P_Points(self.X_Pos_Values,True)        
        self.Vel_T[0] = self.X_Time_Values
        self.Vel_T[1] = self.eval_CP_T_Points(self.X_Time_Values,True)
        self.Vel_T_Limit[0]= self.X_Time_Values
        self.Vel_T_Limit[1]= self.eval_Grenz_T_Points(self.X_Time_Values,True)
        pdt  = self.CP_T_BPoly.derivative(1)
        self.Acc_T[0] = self.X_Time_Values
        self.Acc_T[1] = pdt(self.X_Time_Values)

        maxAcc = max(self.Acc_T[1])
        maxDcc = min(self.Acc_T[1])
        if self.VelEditorFrame:
            self.VelEditorFrame.txtMaxTime.SetValue('%3.3f'% self.CP_M_Points[0][-1])
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
                # if self.VelEditorFrame:
                #     self.VelEditorFrame.btnProfileSave.Enable(True)    
                #     self.VelEditorFrame.btnProfileReplace.Enable(True) 
                #     self.VelEditorFrame.btnProfileReload.Enable(True)                  
                self.Plot(init = True)
                self.Refresh()                
        elif evt.key == 'i' and self.modifyP == 'TI':
            if self.clickpoint[0] > 0.1:
                y = self.eval_CP_M_Points(self.clickpoint[0],False)
                i = np.searchsorted(self.CP_M_Points[0],self.clickpoint[0])
                self.CP_M_Points = np.insert(self.CP_M_Points,i,[self.clickpoint[0],y,0],axis =1)
                self.RecalcMove(init = False)
                # if self.VelEditorFrame:
                #     self.VelEditorFrame.btnProfileSave.Enable(True)    
                #     self.VelEditorFrame.btnProfileReplace.Enable(True) 
                #     self.VelEditorFrame.btnProfileReload.Enable(True)                 
                self.Plot(init = True)
                self.Refresh()                
        elif evt.key == 'i' and self.modifyP == 'PI':
            pass
            if self.clickpoint[0] > 0.1:
                y = self.BPolyFunct(self.VelPosToVelTime(self.clickpoint[0]))
                i = np.searchsorted(self.CP_M_Points[0],self.VelPosToVelTime(self.clickpoint[0]))
                self.CP_M_Points = np.insert(self.SCTPCP_M_PointsointsT,i,[self.VelPosToVelTime(self.clickpoint[0]),y],axis =1)
                self.RecalcBPolySCT()
                # if self.VelEditorFrame:
                #     self.VelEditorFrame.btnProfileSave.Enable(True)    
                #     self.VelEditorFrame.btnProfileReplace.Enable(True) 
                #     self.VelEditorFrame.btnProfileReload.Enable(True) 
                    
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
        self.res = xrc.XmlResource('VelEditorW.xrc')
        self.KeyPointWindow                    = self.res.LoadFrame(None,'ID_WXFRAME')
        self.KeyPointWindow.panelMainPanel     = xrc.XRCCTRL(self.KeyPointWindow,'MainPanel')         
        self.KeyPointWindow.panelOne           = xrc.XRCCTRL(self.KeyPointWindow.panelMainPanel,'PanelOne')
        self.KeyPointWindow.panelVelPath       = xrc.XRCCTRL(self.KeyPointWindow.panelOne,'panelVelPath')        
        self.KeyPointWindow.Diagramm           = Diagramm(self.KeyPointWindow.panelVelPath)        
        self.KeyPointWindow.txtLength          = xrc.XRCCTRL(self.KeyPointWindow,'txtLength')
        self.KeyPointWindow.txtMaxTime         = xrc.XRCCTRL(self.KeyPointWindow,'txtMaxTime')       
        self.KeyPointWindow.txtSetupMaxAcc     = xrc.XRCCTRL(self.KeyPointWindow,'txtSetupMaxAcc')
        self.KeyPointWindow.txtSetupMaxVel     = xrc.XRCCTRL(self.KeyPointWindow,'txtSetupMaxVel')
        self.KeyPointWindow.txtGenerateAcc     = xrc.XRCCTRL(self.KeyPointWindow,'txtGenerateAcc')
        self.KeyPointWindow.txtGenerateVel     = xrc.XRCCTRL(self.KeyPointWindow,'txtGenerateVel')
        self.KeyPointWindow.txtGenerateLength  = xrc.XRCCTRL(self.KeyPointWindow,'txtGenerateLength')
        self.KeyPointWindow.txtGenerateDuration= xrc.XRCCTRL(self.KeyPointWindow,'txtGenerateDuration')
        self.KeyPointWindow.txtMouseXPos       = xrc.XRCCTRL(self.KeyPointWindow,'txtMouseXPos')
        self.KeyPointWindow.txtMouseYPos       = xrc.XRCCTRL(self.KeyPointWindow,'txtMouseYPos')
        self.KeyPointWindow.txtProfileMaxAcc   = xrc.XRCCTRL(self.KeyPointWindow,'txtProfileMaxAcc')
        self.KeyPointWindow.txtProfileMaxDcc   = xrc.XRCCTRL(self.KeyPointWindow,'txtProfileMaxDcc')
        self.KeyPointWindow.btnSmooth          = xrc.XRCCTRL(self.KeyPointWindow,'btnSmooth')
        self.KeyPointWindow.btnGenerate        = xrc.XRCCTRL(self.KeyPointWindow,'btnGenerate')     

        #self.KeyPointWindow.txtMaxTime.Enable(False)
        self.KeyPointWindow.txtMouseXPos.Enable(False)
        self.KeyPointWindow.txtMouseYPos.Enable(False)
        self.KeyPointWindow.btnGenerate.Enable(False)
        self.KeyPointWindow.btnSmooth.Enable(False)
        
        self.Bind(wx.EVT_BUTTON        , self.OnButtonSmooth,        self.KeyPointWindow.btnSmooth)
        self.Bind(wx.EVT_BUTTON        , self.OnButtonGenerate,      self.KeyPointWindow.btnGenerate)


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
    def OnButtonSmooth(self,evt):
        print('Smooth')
        pass

    def OnButtonGenerate(self,evt):
        print('Generate')
        self.KeyPointWindow.Diagramm.Calc_Default_Profile()
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

        self.KeyPointWindow.txtLength.SetValue     ('%3.3f'% float(Data[8]))
        self.KeyPointWindow.txtSetupMaxAcc.SetValue('%3.3f'% float(Data[6]))
        self.KeyPointWindow.txtSetupMaxVel.SetValue('%3.3f'% float(Data[7]))

        self.KeyPointWindow.Diagramm.Entry()

if __name__ == "__main__":
    app = VelEditor4C()
    app.MainLoop()