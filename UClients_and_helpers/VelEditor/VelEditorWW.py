import wx
from wx import xrc

import numpy as np
import matplotlib

import matplotlib.pyplot as plt
import mpl_toolkits.axisartist as AA

from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
#from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg, wxc
from scipy.interpolate import splev, splrep, splint, interp1d, BPoly
import math
from math import copysign

import time
import os
import copy

import pickle

from GrenzVel import GrenzVel
#from GrenzVelReconstruct1 import GrenzVelReconstruct1 as GrenzVel


#self.rendertckpN=[([0.,0.,0.,0.,0.13861451,0.22641582,0.34179822,0.49557579,0.62585615,0.75110965,1.,1.,1.,1.]),
                 #[([ 0.12028099, -0.7305094,   2.25717151, 12.86629845, 22.15622902, 18.70388373,  8.65406875, -6.38714818,-13.77478783,-19.92023301]),
                  #([ 0.13272206, -4.35268003,-11.92641631,-13.21277906, -5.1798756 ,  8.08084009, 16.64408539, 13.38342587,  3.67003860,  0.42041895]),
                  #([50.01163513, 49.96801420, 49.94638256, 50.12640822, 49.87537868, 47.11572431, 43.36188280, 42.48085144, 40.85493989, 39.68681341])],3]

#self.rendertckpN=[([0., 0., 0., 0., 1., 1., 1., 1.]), 
                 #[([ 3.12999903e-16, -2.91683807e+01, -4.26490903e-02,  4.47113037e+00]),
                  #([-1.36086907e-16, -1.51991701e+01,  1.71124530e+00,  2.18266416e+00]),
                  #([50.        , 46.6073494 , 47.27580643, 51.80615997])], 3]
                   

rendertckpN = [([0.,0.,0.,0.,0.12812584,0.24459942,0.50114625,0.76612645,1.,1.,1.,1.]),
            [([ 0.08731752,  1.11506322,  3.99416078, 11.33227897, 18.20872362, 25.30739366,  33.36570704,  36.2906925]),
             ([ 0.06257548, -1.47087011, -3.30561348, -5.09293159, -7.14529766, -8.76211713, -10.39719564, -10.1796305]),
             ([50.09783148, 49.83594656, 49.98026792, 50.50023384, 45.04604929, 36.48810102,  38.05977388,  37.80970101])],3]

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
        self.rezoom = True
        
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



        self.GrenzParaMinima =[[],[]]
        self.VelTData        =[[],[]]
        self.SBPolyVelPData  =[[],[]]
        self.SBPolyVelTData  =[[],[]]
      

        self.GenerateTestData()

        self.PrepareGraphs()

        self.Plot()

    def GenerateTestData(self):
        n = np.linspace(0,1000,4)
        o = -(((n-500)*300.0)*((n-500)*300.0))/4000000000.0+6
        tckp1 = splrep(n,o) 

        x = np.linspace(0,1000,1001)        
        y = splev(x,tckp1)

        self.GrenzParaMinima[0] =x 
        self.GrenzParaMinima[1] =y

        self.VelTData[0] = x
        self.VelTData[1] = y*0.9

        self.SBPolyVelPData[0] = x
        self.SBPolyVelPData[1] = y*0.8

        self.SBPolyVelTData[0] = x
        self.SBPolyVelTData[1] = y*0.7



    def PrepareGraphs(self): 
        self.axes.clear()
        self.axesT.clear()
        self.PrepareAxes()
        self._xInit           = np.linspace(0., 1000. , 1001)
        self.Null             = np.zeros(len(self._xInit))
        # self.TCPointsBeziersData = np.zeros((2,len(self._xInit)),dtype = np.double)
        self.lines = []
        self.lines += self.axes.plot(self._xInit,self.Null, color="black",              linewidth=1., linestyle="-",pickradius = 0)   # VelLimit over Pos [0]

        self.lines += self.axes.plot(self._xInit,self.Null, color="darkred",            linewidth=1.0, linestyle="-",pickradius = 0)   # Vel  Beziers  [1]
        # self.lines += self.axes.plot(self._xInit,self.Null, color="darkgreen",          linewidth=1.0, linestyle="-.",pickradius = 0)   # Acc  Beziers  [2]
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
        self.linesT += self.axesT.plot(self._xInit,self.Null,  color="black",           linewidth=1., linestyle="-",pickradius = 0)   # VelLimit over Time [0]

        #self.linesT += self.axesT.plot(self._xInit,self.Null,  color="black",           linewidth=0.4, linestyle=":",pickradius = 0)   # VelLimit over Time [0]
        # self.linesT += self.axesT.plot(self._xInit,self.Null,  color="darkred",         linewidth=1.4, linestyle="-",pickradius = 0 ) # Vel  Beziers [1]
        # self.linesT += self.axesT.plot(self._xInit,self.Null,  color="black",           linewidth=0.4, linestyle="-.",pickradius = 0)  # Acc  Beziers [2]
        # self.linesT += self.axesT.plot(self._xInit,self.Null,  color="darkblue",        linewidth=1.0, linestyle="-.",pickradius = 0)  # Pos  Beziers [3]
        # self.linesT += self.axesT.plot(self._xInit,self.Null,  color="black",           linewidth=0.8, linestyle="-",pickradius = 0)   # Vel          [4]
        # self.linesT += self.axesT.plot(self._xInit,self.Null,  color="darkgreen",       linewidth=1.4, linestyle="-",pickradius = 0)   # Acc          [5]
        # self.linesT += self.axesT.plot(self._xInit,self.Null,  color="m",           linewidth=0.8, linestyle="-",pickradius = 0)   # Pos          [6]  
        
        #self.fillT = []
        #self.fillT +=  self.axesT.fill(self._xInit,self.Null, color="xkcd:pale lime", alpha = 0.3,)
        
    # def InitializePhaseI(self,RefYellow,RefGreen,RefCyan,RefMagenta,tckp,maxVel,maxAcc,ProzentMaxVel,ProzentMaxAcc,Debug,SmoothingF,SmootingOn):
    #     self.maxVelD = maxVel
    #     self.usrVelD = maxVel*ProzentMaxVel
    #     self.maxAccD = maxAcc
    #     self.usrAccD = maxAcc*ProzentMaxAcc
    #     self.PrepareGraphs()        
    #     (A, Bogen2Param, self.ProzentGrenzParaMinima, self.GrenzParaMinima,
    #                     self.PathLengthGrenzVel, self.TotalPathTime, self.SumAveTime,
    #                     meanVel, AccGrenzData, AccGrenzPara, self.VelTimeAvePara,
    #                     AccData, self.CPoints, self._x) = self.CalculateGrenzProfile(RefYellow,RefGreen,RefCyan,RefMagenta,tckp,
    #                                                                                  maxVel,maxAcc,ProzentMaxVel,ProzentMaxAcc,Debug,
    #                                                                                  SmoothingF,SmootingOn)
        
    #     self.PrepToTimeDomain()
        
    #     self.TTPoints   = []
    #     self.TPPoints   = []
    #     self.fillP      = []
    #     self.fillT      = [] 
    #     self.PosSkalierung2 = 1.
        
    #     return (A, Bogen2Param, self.ProzentGrenzParaMinima, self.GrenzParaMinima,
    #             self.PathLengthGrenzVel, self.TotalPathTime, self.SumAveTime,
    #             meanVel, AccGrenzData, AccGrenzPara, self.VelTimeAvePara,
    #             AccData, self.CPoints, self._x)
        
    # def CalculateGrenzProfile(self,RefYellow,RefGreen,RefCyan,RefMagenta,tckp,maxVel,maxAcc,ProzentMaxVel,ProzentMaxAcc,Debug,SmoothingF,SmoothingOn):

    #     self.rendertckpN = tckp
        
    #     YellowPoint  = RefYellow
    #     GreenPoint   = RefGreen
    #     CyanPoint    = RefCyan
    #     MagentaPoint = RefMagenta      
    #     Points = (YellowPoint,GreenPoint,CyanPoint,MagentaPoint)
                
    #     (A,
    #      Bogen2Param,
    #      self.ProzentGrenzParaMinima,
    #      self.GrenzParaMinima,
    #      self.PathLengthGrenzVel,
    #      self.TotalPathTime,
    #      self.SumAveTime,
    #      meanVel,
    #      AccGrenzData,
    #      AccGrenzPara,
    #      self.VelTimeAvePara,AccData,self.CPoints)= GrenzVel(self.rendertckpN,
    #                                                  Points,
    #                                                  maxVel,
    #                                                  ProzentMaxVel,
    #                                                  maxAcc,
    #                                                  ProzentMaxAcc,
    #                                                  SmoothingF,
    #                                                  SmoothingOn,
    #                                                  Debug)
        
    #     self._x = self.GrenzParaMinima[0]
    #     self.GrenzVelP= interp1d(self.GrenzParaMinima[0],self.GrenzParaMinima[1], bounds_error=False,fill_value=[0])
        
    #     return (A, Bogen2Param, self.ProzentGrenzParaMinima, self.GrenzParaMinima,
    #             self.PathLengthGrenzVel, self.TotalPathTime, self.SumAveTime,
    #             meanVel, AccGrenzData, AccGrenzPara, self.VelTimeAvePara,
    #             AccData, self.CPoints, self._x)
        
        
    def Plot(self):        
        self.rezoom = True
        self.lines[0].set( xdata = self.GrenzParaMinima[0],ydata=self.GrenzParaMinima[1])
        if self.fillP ==[]:
            self.fillP =self.axes.fill(self.GrenzParaMinima[0],self.GrenzParaMinima[1], color="lightgreen", alpha = 0.3,)
        self.lines[1].set( xdata=self.SBPolyVelPData[0],         ydata=self.SBPolyVelPData[1])
        
        self.linesT[0].set( xdata=self.VelTData[0],         ydata=self.VelTData[1])
        for i in range (len(self.fillT)):
            self.axesT.patches.remove(self.fillT[i])
        self.fillT =[]
        if self.fillT ==[]:
            self.fillT += self.axesT.fill(self.VelTData[0],self.VelTData[1] , color="lightgreen", alpha = 0.1,)        
            #self.fillT += self.axesT.fill(self.GrenzDataX,self.GrenzDataY, color="lightgreen", alpha = 0.2,)

        # for i in range(len(self.TPPoints)):
        #     self.axes.lines.remove(self.TPPoints[i])
        # self.TPPoints   = []
        # for i in range(0,len(self.SCTPointsT[0])):
        #     self.TPPoints += self.axes.plot(self.VelVelToVelPos(self.SCTPointsT[0,i]),self.SCTPointsT[1,i],'rx')    

        # for i in range(len(self.TTPoints)):
        #     self.axesT.lines.remove(self.TTPoints[i])
        # self.TTPoints   = []
        # for i in range(0,len(self.SCTPointsT[0])):
        #     self.TTPoints += self.axesT.plot(self.SCTPointsT[0,i],self.SCTPointsT[1,i],'rx')

        pass                     

    def OnPaint(self,evt):
        #self.axes.plot( self.GrenzParaMinima[0],self.GrenzParaMinima[1], color="red",              linewidth=1., linestyle="-",pickradius = 0) 
        #self.axesT.plot( self.GrenzParaMinima[0],self.GrenzParaMinima[1], color="red",              linewidth=1., linestyle="-",pickradius = 0)  # VelLimit over Pos [0]
        # print(self.lines)
        # for i in range ( 0 ,len(self.lines)):
        #     self.lines[i].plot()
        
        # try:
        #     self.linesT[1].set(xdata=self.SBPolyVelTData[0], ydata= self.SBPolyVelTData[1])
        #     #self.linesT[2].set(xdata=self.VelTData[0]*sc, ydata= self.VelTData[1])
        #     self.linesT[3].set(xdata=self.SBPolyAccTData[0], ydata= self.SBPolyAccTData[1])
        #     self.linesT[2].set(xdata=self.GrenzDataX, ydata= self.GrenzDataY)
        #     self.linesT[6].set(xdata=self.SBPolyPosTData[0], ydata= self.SBPolyPosTData[1])
        # except:
        #     pass
        # self.linesT[6].set( xdata=self.SBPolyVelPData[0],         ydata=self.SBPolyVelPData[1])
        
        # self.linesT[3].set(xdata=TCPointsData[0], ydata= TCPointsData[1])
        # self.linesT[4].set(xdata=AccTCPoints[0], ydata= AccTCPoints[1])
        # self.linesT[5].set(xdata=PosTCPoints[0], ydata= PosTCPoints[1])
        
        if self.modifyP == 'Point' or self.rezoom == True:
            #minlimTx = min(-self.SBPolyVelTData[0][-1]*0.05, -self.SBPolyVelTData[0][-1]*0.05 )
            #maxlimTx = max(self.SBPolyVelTData[0][-1]*1.05,self.SBPolyVelTData[0][-1]*1.05)
            minlimTx = min(-self.GrenzParaMinima[0][0]*0.05,-self.GrenzParaMinima[0][0])
            maxlimTx = max( self.GrenzParaMinima[0][-1]*1.05, self.GrenzParaMinima[0][-1]*1.05)
            self.axesT.set_xlim(minlimTx,maxlimTx)
            #minlimTy = min(np.amin(self.SBPolyVelTData[1]),np.amin(self.VelTData[1]),np.amin(self.SBPolyAccTData[1]))
            #maxlimTy = max(np.amax(self.SBPolyVelTData[1]),np.amax(self.VelTData[1]),np.amax(self.SBPolyAccTData[1]))
            m = np.amax(self.VelTData[1]) 
            self.axesT.set_ylim(-0.5,m*1.1)
            #self.axesT.set_ylim(minlimTy*1.05,maxlimTy*1.05)
            self.rezoom = False
        if  self.rezoom == True:  
            # minlimx = 0 #min(-self.SBPolyVelTData[0,-1]*0.05,-self.SBPolyVelTData[0,-1])
            # maxlimx = 10 #max( self.SBPolyVelTData[0,-1]*1.05, self.SBPolyVelTData[0,-1]*1.05)
            minlimx = min(-self.GrenzParaMinima[0][0]*0.05,-self.GrenzParaMinima[0][0])
            maxlimx = max( self.GrenzParaMinima[0][-1]*1.05, self.GrenzParaMinima[0][-1]*1.05)
            self.axes.set_xlim(minlimx,maxlimx)
            m = np.amax(self.VelTData[1]) 
            self.axes.set_ylim(-0.5,m*1.1)
            pass

        size =  self.parent.GetClientSize()
        self.figure.set_size_inches(size[0]/self.dpi,size[1]/self.dpi)
        self.canvas.SetSize(size)
        self.canvas.draw()
        evt.Skip()

    # def PrepToTimeDomain(self):
    #     # ------Beginn Get Position over Time Line
    #     self.PTData = np.zeros((2,len(self.GrenzParaMinima[0])),dtype = np.double)
    #     ST = 0.0
    #     for i in range(1,len(self.GrenzParaMinima[0])):
    #         T = abs(self.GrenzParaMinima[0,i-1]-self.GrenzParaMinima[0,i])/((self.GrenzParaMinima[1,i-1]+(self.GrenzParaMinima[1,i]))/2)
    #         ST = ST+T
    #         self.PTData[0,i]= self.GrenzParaMinima[0,i]
    #         self.PTData[1,i]= ST
    #     # ------End Get Position over Time Line
    #     # ------Beginn Get Vel over Time Line Interpolation
    #     self.VelTData = np.zeros((2,len(self.GrenzParaMinima[0])),dtype = np.double)
    #     self.VelPosToVelTime = interp1d(self.PTData[0], self.PTData[1], fill_value=np.nan, assume_sorted=True)
    #     self.VelTData[0] = self.VelPosToVelTime(self.GrenzParaMinima[0])
    #     self.VelTData[1] = self.GrenzParaMinima[1]
    #     # ------End Get Vel over Time Line Interpolation
    #     # ------Beginn Get Acc over Time Line
    #     self.AccTData = np.zeros((2,len(self.GrenzParaMinima[0])),dtype = np.double)
    #     for i in range(1,len(self.GrenzParaMinima[0])):
    #         Acc = (self.VelTData[1,i]-self.VelTData[1,i-1])/(self.VelTData[0,i]-self.VelTData[0,i-1])
    #         self.AccTData[0,i]= self.VelTData[0,i]
    #         self.AccTData[1,i]= Acc
    #     self.AccTData[0,-1]= self.VelTData[0,-1]
    #     self.AccTData[1,-1]= 0.0
    #     # ------End Get Acc over Time Line
    #     # ------Beginn AccData als differenzen
    #     self.DeltaAccTData = np.zeros((2,len(self.AccTData[0])),dtype = np.double)
    #     for i in range(0,len(self.AccTData[0])-1):
    #         self.DeltaAccTData[0,i]= self.AccTData[0,i+1]-self.AccTData[0,i]
    #         self.DeltaAccTData[1,i]= self.AccTData[1,i+1]-self.AccTData[1,i]
    #     #------End AccData als differenzen
    #     # ------Beginn ramp Difference
    #     maxJerk = 20.
    #     for i in range(0,len(self.AccTData[0])-1):
    #         if (abs(self.AccTData[1,i+1]-self.AccTData[1,i])/(self.AccTData[0,i+1]-self.AccTData[0,i]) > maxJerk):
    #             self.DeltaAccTData[0,i]= abs(self.AccTData[1,i+1]-self.AccTData[1,i])/maxJerk
    #     # ------Beginn Summation
    #     self.SumAccTData = np.zeros((2,len(self.DeltaAccTData[0])),dtype = np.double)
    #     for i in range(0,len(self.DeltaAccTData[0])):
    #         self.SumAccTData[0,i]= self.SumAccTData[0,i-1]+self.DeltaAccTData[0][i]
    #         self.SumAccTData[1,i]= self.SumAccTData[1,i-1]+self.DeltaAccTData[1][i]
    #     self.SumAccTData[0,0] = 0.
    #     self.SumAccTData[1,0] = 0.
    #     self.SumAccTData[1,-1] = 0.
    #     # ------End Summation
    #     # ------Beginn Rebase Time        
    #     GV = interp1d(self.SumAccTData[0], self.SumAccTData[1], kind='linear', axis=-1, copy=True, bounds_error=None, fill_value=np.nan, assume_sorted=True)
    #     NT = np.linspace(0,self.SumAccTData[0,-1], num=10000, endpoint=True, retstep=False, dtype=np.double)        
    #     AccScale = self.AccTData[0,-1]/self.SumAccTData[0,-1]
    #     NGV = GV(NT)
    #     self.RampedAccTData = np.stack((NT,NGV))
    #     self.RampedAccTData[0] = self.RampedAccTData[0]*AccScale        
    #     # ------End Rebase Time
    #     # ------Beginn Scaling to get Vend = 0
    #     # ------Beginn  Integrate Positive RBRampedAccTData over Time to get Vel over Time
    #     SP = 0.0
    #     self.PosRampedVelTData = np.zeros((1,len(self.RampedAccTData[0])),dtype = np.double)
    #     for i in range(1,len(self.RampedAccTData[0])-1):
    #         if self.RampedAccTData[1,i] > 0:
    #             P = ((-0.5*(self.RampedAccTData[1,i-1]+self.RampedAccTData[1,i+1]))*(self.RampedAccTData[0,i-1]-self.RampedAccTData[0,i]))
    #             SP = SP + P
    #             self.PosRampedVelTData[0,i]=SP
    #         self.PosRampedVelTData[0,-1]=SP
    #     # ------End  Integrate Positive RBRampedAccTData over Time to get Vel over Time
    #     # ------Beginn  Integrate Negative RBRampedAccTData over Time to get Vel over Time
    #     SP = 0.0
    #     self.NegRampedVelTData = np.zeros((1,len(self.RampedAccTData[0])),dtype = np.double)
    #     for i in range(1,len(self.RampedAccTData[0])-1):
    #         if self.RampedAccTData[1,i] < 0:
    #             P = ((-0.5*(self.RampedAccTData[1,i-1]+self.RampedAccTData[1,i+1]))*(self.RampedAccTData[0,i-1]-self.RampedAccTData[0,i]))
    #             SP = SP + P
    #             self.NegRampedVelTData[0,i]=SP
    #         self.NegRampedVelTData[0,-1]=SP
    #     # ------End  Integrate Positive RBRampedAccTData over Time to get Vel over Time
    #     AccScale1 = abs(self.NegRampedVelTData[0,-1]/self.PosRampedVelTData[0,-1])
    #     self.BalancedAccTData = np.zeros((2,len(self.RampedAccTData[0])),dtype = np.double)
    #     for i in range(0,len(self.RampedAccTData[0])):
    #         if self.RampedAccTData[1,i] > 0:
    #             self.BalancedAccTData[1,i] = self.RampedAccTData[1,i]*AccScale1
    #         else:
    #             self.BalancedAccTData[1,i] = self.RampedAccTData[1,i]*1.0
    #         self.BalancedAccTData[0,i] = self.RampedAccTData[0,i]
    #     # ------End Scaling to get Vend = 0 
    #     # ------Beginn  Integrate BalancedAccTData over Time to get Vel over Time
    #     SP = 0.0
    #     self.BalancedVelTData = np.zeros((2,len(self.BalancedAccTData[0])),dtype = np.double)
    #     for i in range(1,len(self.BalancedAccTData[0])-1):
    #         P = ((-0.5*(self.BalancedAccTData[1,i-1]+self.BalancedAccTData[1,i+1]))*(self.BalancedAccTData[0,i-1]-self.BalancedAccTData[0,i]))
    #         SP = SP + P
    #         self.BalancedVelTData[0,i]=self.BalancedAccTData[0,i]
    #         self.BalancedVelTData[1,i]=SP
    #     self.BalancedVelTData[0,-1]=self.BalancedAccTData[0,-1]
    #     self.BalancedVelTData[1,-1]=SP
    #     # ------End  BalancedAccTData over Time to get Vel over Time
    #     # ------Beginn Scale BalancedAccTData over Time to meet maxVel Kriterium
    #     mv = np.amax(self.BalancedVelTData[1])
    #     AccScale2 = self.usrVelD/mv
    #     self.BalancedAccTData[1]=self.BalancedAccTData[1]*AccScale2
    #     for i in range(1,len(self.BalancedAccTData[0])-1):
    #         P = ((-0.5*(self.BalancedAccTData[1,i-1]+self.BalancedAccTData[1,i+1]))*(self.BalancedAccTData[0,i-1]-self.BalancedAccTData[0,i]))
    #         SP = SP + P
    #         self.BalancedVelTData[0,i]=self.BalancedAccTData[0,i]
    #         self.BalancedVelTData[1,i]=SP
    #     self.BalancedVelTData[0,-1]=self.BalancedAccTData[0,-1]
    #     self.BalancedVelTData[1,-1]=SP
    #     # ------End  BalancedAccTData over Time to get Vel over Time 
    #     # ------End Scale BalancedAccTData over Time to meet maxVel Kriterium
    #     # ------Beginn  Integrate BalancedVelTData over Time to get Pos over Time
    #     SP = 0.0
    #     self.BalancedPosTData = np.zeros((2,len(self.BalancedVelTData[0])),dtype = np.double)
    #     for i in range(1,len(self.BalancedVelTData[0])-1):
    #         P = ((-0.5*(self.BalancedVelTData[1,i-1]+self.BalancedVelTData[1,i+1]))*(self.BalancedVelTData[0,i-1]-self.BalancedVelTData[0,i]))
    #         SP = SP + P
    #         self.BalancedPosTData[0,i]=self.BalancedVelTData[0,i]
    #         self.BalancedPosTData[1,i]=SP
    #     self.BalancedPosTData[0,-1]=self.BalancedVelTData[0,-1]
    #     self.BalancedPosTData[1,-1]=SP
    #     #print 'Laenge des Pfades nach Ramp and Balance %3.4f'%(self.BalancedPosTData[1,-1])
    #     # ------End  Integrate BalancedVelTData over Time to get Pos over Time
    #     # ------Beginn  Scaled Integration of BalancedVelTData over Time to get Pos over Time while traveling the whole Path
    #     self.PosSkalierung = self.GrenzParaMinima[0,-1]/self.BalancedPosTData[1,-1]
    #     SP = 0.0
    #     self.SBalancedPosTData = np.zeros((2,len(self.BalancedVelTData[0])),dtype = np.double)
    #     for i in range(1,len(self.BalancedVelTData[0])-1):
    #         P = ((-0.5*(self.BalancedVelTData[1,i-1]+self.BalancedVelTData[1,i+1]))*(self.BalancedVelTData[0,i-1]-self.BalancedVelTData[0,i])*self.PosSkalierung)
    #         SP = SP + P
    #         self.SBalancedPosTData[0,i]=self.BalancedVelTData[0,i]*self.PosSkalierung
    #         self.SBalancedPosTData[1,i]=SP
    #     self.SBalancedPosTData[0,-1]=self.BalancedVelTData[0,-1]*self.PosSkalierung
    #     self.SBalancedPosTData[1,-1]=self.GrenzParaMinima[0,-1]
    #     #print 'Skalierte Laenge des Pfades nach Ramp and Balance %3.4f'%(self.SBalancedPosTData[1,-1])
    #     # ------End  Scaled Integration of BalancedVelTData over Time to get Pos over Time while traveling the whole Path
    #     # ------Beginn Scaled Vel and Acc
    #     self.SBalancedVelTData = np.zeros((2,len(self.BalancedVelTData[0])),dtype = np.double)
    #     self.SBalancedVelTData[0] = self.SBalancedPosTData[0]
    #     self.SBalancedVelTData[1] = self.BalancedVelTData[1]
        
    #     self.SBalancedAccTData = np.zeros((2,len(self.BalancedVelTData[0])),dtype = np.double)
    #     self.SBalancedAccTData[0] = self.SBalancedPosTData[0]
    #     self.SBalancedAccTData[1] = self.BalancedAccTData[1]
    #     # ------End Scaled Vel and Acc
    #     # ------Begin find Extrema of SBalancedVelTData
    #     CTPointsSBalancedVelX=[0.0]
    #     CTPointsSBalancedVelY=[0.0]
    #     for i in range(1,len(self.SBalancedAccTData[0])):
    #         if ((copysign(1, self.SBalancedAccTData[1,i-1]) != copysign(1,self.SBalancedAccTData[1,i])) or
    #             self.SBalancedAccTData[1,i] == 0 and self.SBalancedAccTData[1,i-1] != 0):
    #             CTPointsSBalancedVelX.append(self.SBalancedAccTData[0,i])
    #             CTPointsSBalancedVelY.append(self.SBalancedVelTData[1,i])
    #     CTPointsNX     = np.array(CTPointsSBalancedVelX)
    #     CTPointsNY     = np.array(CTPointsSBalancedVelY)
    #     self.CTPointsSBalancedVelT = np.stack((CTPointsNX,CTPointsNY))
    #     self.CTPointsSBalancedVelT[1,-1]= 0.0
    #     # ------End find Extrema of SVelTCVData
    #     # ------Begin find BPoly through SVelTCVData extrema
    #     #construct yi : array_like or list of array_likes yi[i][j] is the j-th derivative known at xi[i]        
    #     order = 3
    #     yi = [[0,0]]
    #     for i in range (1,len(self.CTPointsSBalancedVelT[1])):
    #         yi.append([self.CTPointsSBalancedVelT[1,i],0])
    #     yi[-1]=[0,0]         
    #     self.BPolyFunct =BPoly.from_derivatives(self.CTPointsSBalancedVelT[0],yi,orders = order)
    #     self.BPolyVelTData    = np.zeros((2,len(self.BalancedVelTData[0])),dtype = np.double)
    #     self.BPolyVelTData[0] = self.SBalancedVelTData[0]
    #     self.BPolyVelTData[1] = self.BPolyFunct(self.SBalancedVelTData[0])
    #     # ------End find BPoly through SVelTCVData extrema
    #     # ------Beginn Get SAccTCV over Time Line noch nicht skaliert
    #     self.BPolyAccTData = np.zeros((2,len(self.BPolyVelTData[0])),dtype = np.double)
    #     for i in range(1,len(self.BPolyVelTData[0])):
    #         Acc = (self.BPolyVelTData[1,i]-self.BPolyVelTData[1,i-1])/(self.BPolyVelTData[0,i]-self.BPolyVelTData[0,i-1])
    #         self.BPolyAccTData[0,i]= self.BPolyVelTData[0,i]
    #         self.BPolyAccTData[1,i]= Acc
    #     self.BPolyAccTData[0,-1]= self.BPolyVelTData[0,-1]
    #     self.BPolyAccTData[1,-1]= 0.0
    #     # ------End Get SAccTCV over Time Line  noch nicht skaliert
    #     # ------Beginn  Integrate SVelTCVData over Time to get Pos over Time
    #     SP = 0.0
    #     self.BPolyPosTData = np.zeros((2,len(self.BPolyVelTData[0])),dtype = np.double)
    #     for i in range(1,len(self.BPolyVelTData[0])-1):
    #         P = ((-0.5*(self.BPolyVelTData[1,i-1]+self.BPolyVelTData[1,i+1]))*(self.BPolyVelTData[0,i-1]-self.BPolyVelTData[0,i]))
    #         SP = SP + P
    #         self.BPolyPosTData[0,i]=self.BPolyVelTData[0,i]
    #         self.BPolyPosTData[1,i]=SP
    #     self.BPolyPosTData[0,-1]=self.BPolyVelTData[0,-1]
    #     self.BPolyPosTData[1,-1]=SP
    #     #print 'Laenge des Pfades nach BPoly %3.4f'%(self.BPolyPosTData[1,-1])
    #     # ------End  Integrate VelTRamped over Time to get Pos over Time
    #     # ------Beginn  Scaled Integration of SBPVelTData over Time to get Pos over Time while traveling the whole Path
    #     self.PosSkalierung1 = self.GrenzParaMinima[0,-1]/self.BPolyPosTData[1,-1]
    #     SP = 0.0
    #     self.SBPolyPosTData = np.zeros((2,len(self.BPolyVelTData[0])),dtype = np.double)
    #     for i in range(1,len(self.BPolyVelTData[0])-1):
    #         P = ((-0.5*(self.BPolyVelTData[1,i-1]+self.BPolyVelTData[1,i+1]))*(self.BPolyVelTData[0,i-1]-self.BPolyVelTData[0,i])*self.PosSkalierung1)
    #         SP = SP + P
    #         self.SBPolyPosTData[0,i]=self.BPolyVelTData[0,i]*self.PosSkalierung1
    #         self.SBPolyPosTData[1,i]=SP
    #     self.SBPolyPosTData[0,-1]=self.BPolyVelTData[0,-1]*self.PosSkalierung1
    #     self.SBPolyPosTData[1,-1]=self.GrenzParaMinima[0,-1]
    #     #print 'Skalierte Laenge des Pfades nach Editing %3.4f'%(self.SBPolyPosTData[1,-1])
    #     # ------End  Scaled Integration of SBPVelTData over Time to get Pos over Time while traveling the whole Path
    #     # ------Beginn 2nd Scaled Vel and Acc
    #     self.SBPolyVelTData = np.zeros((2,len(self.BalancedVelTData[0])),dtype = np.double)
    #     self.SBPolyVelTData[0] = self.SBPolyPosTData[0]
    #     self.SBPolyVelTData[1] = self.BPolyVelTData[1]
        
    #     self.SBPolyAccTData = np.zeros((2,len(self.BalancedVelTData[0])),dtype = np.double)
    #     self.SBPolyAccTData[0] = self.SBPolyPosTData[0]
    #     self.SBPolyAccTData[1] = self.BPolyAccTData[1] 
        
    #     self.SCTPointsT = np.zeros((2,len(self.CTPointsSBalancedVelT[0])),dtype = np.double)
    #     for i in range(len(self.CTPointsSBalancedVelT[0])):
    #         self.SCTPointsT[0,i] = self.CTPointsSBalancedVelT[0,i]*self.PosSkalierung1
    #         self.SCTPointsT[1,i] = self.CTPointsSBalancedVelT[1,i]        
    #     # ------End 2nd Scaled Vel and Acc
        
    #     # ------Beginn Get SBPolyVelTData in Pos Domain
    #     self.SBPolyVelPData = np.zeros((2,len(self.BPolyVelTData[0])),dtype = np.double)
    #     self.VelVelToVelPos = interp1d(self.SBPolyPosTData[0], self.SBPolyPosTData[1], fill_value=np.nan, assume_sorted=True)
    #     self.SBPolyVelPData[0] = self.VelVelToVelPos(self.SBPolyVelTData[0])
    #     self.SBPolyVelPData[1] = self.BPolyVelTData[1]
    #     # ------End Get SBPolyVelTData in Pos Domain
    #     self.VelPosToVelTime = interp1d(self.SBPolyPosTData[1], self.SBPolyPosTData[0], fill_value=np.nan, assume_sorted=True)
    #     self.RecalcBPolySCT()
        
    # def MovePointPosDomain(self):
    #     if self.modifyP == 'PPoint':
    #         flag = ''
    #         x1 = self.TPPoints[self.hpoint-1].get_xdata()
    #         y2 = self.TPPoints[self.hpoint].get_ydata()
    #         x3 = self.TPPoints[self.hpoint+1].get_xdata()
    #         MDX = self.MouseDeltaXPoint
    #         MDY = self.MouseDeltaYPoint
            
    #         if (x1+0.1 < self.PhpointX-MDX and
    #             self.PhpointX-MDX < x3-0.1):
    #             x = self.PhpointX-MDX
    #             self.MDDX = MDX
    #         else:
    #             flag = 'exit' 
    #             if MDX < 0 :
    #                 x= x3-0.2
    #             else:
    #                 x= x1+0.2
    #         if (self.GrenzVelT(self.VelPosToVelTime(x)) > self.PhpointY-MDY ):
    #             y=max((self.PhpointY-MDY),0.1)
    #             self.MDDY = MDY
    #         else:
    #             flag = 'exit'
    #             y = max(self.GrenzVelT(self.VelPosToVelTime(x)),0.1) 
    #             self.MDDY = MDY                
    #         if flag == 'exit':
    #             self.modifyP == 'none'               
    #             self.TPPoints[self.hpoint].set(color='r')
            
    #         self.SCTPointsT[0,self.hpoint] = self.VelPosToVelTime(x)
    #         self.SCTPointsT[1,self.hpoint] = y
            
    #         self.RecalcBPolySCT()
            
    #         if self.VelEditorFrame:
    #             self.VelEditorFrame.btnProfileSave.Enable(True)    
    #             self.VelEditorFrame.btnProfileReplace.Enable(True) 
    #             self.VelEditorFrame.btnProfileReload.Enable(True)                
            
    #         self.Plot()
    #         self.rezoom = True    
    #         wx.PostEvent(self,wx.PaintEvent())
                           
    # def MovePointTimeDomain(self):
    #     if self.modifyP == 'TPoint':
    #         flag = ''
    #         x1 = self.TTPoints[self.hpoint-1].get_xdata()
    #         y2 = self.TTPoints[self.hpoint].get_ydata()
    #         x3 = self.TTPoints[self.hpoint+1].get_xdata()
    #         MDX = self.MouseDeltaXPoint
    #         MDY = self.MouseDeltaYPoint

    #         if (x1+0.1 < self.ThpointX-MDX and
    #             self.ThpointX-MDX < x3-0.1):        
    #             x = self.ThpointX-MDX
    #             self.MDDX = MDX
    #         else:
    #             flag = 'exit' 
    #             if MDX < 0 :
    #                 x= x3-0.2
    #             else:
    #                 x= x1+0.2
    #         if (self.GrenzVelT(x) > self.ThpointY-MDY):
    #             y= max((self.ThpointY-MDY),0)
    #             self.MDDY = MDY
    #         else:
    #             flag = 'exit'
    #             y = max((self.GrenzVelT(x)),0) 
    #             self.MDDY = MDY                
    #         if flag == 'exit':
    #             self.modifyP == 'none'               
    #             self.TPPoints[self.hpoint].set(color='r')
                
    #         self.SCTPointsT[0,self.hpoint] = x
    #         self.SCTPointsT[1,self.hpoint] = y
            
    #         self.RecalcBPolySCT()
            
    #         if self.VelEditorFrame:
    #             self.VelEditorFrame.btnProfileSave.Enable(True)    
    #             self.VelEditorFrame.btnProfileReplace.Enable(True) 
    #             self.VelEditorFrame.btnProfileReload.Enable(True)               
            
    #         self.Plot()
    #         self.rezoom = False
    #         wx.PostEvent(self,wx.PaintEvent()) 
       
    # def RecalcBPolySCT(self):
    #     order = 3
    #     yi = [[0,0]]
    #     for i in range (1,len(self.SCTPointsT[0])):
    #         yi.append([self.SCTPointsT[1,i],0])
    #     yi[-1]=[0,0]        
    #     self.BPolyFunct =BPoly.from_derivatives(self.SCTPointsT[0],yi,orders = order)
    #     pdt  =self.BPolyFunct.derivative(1)
    #     pint =self.BPolyFunct.antiderivative(1)
    #     self.SBPolyVelTData[1] = self.BPolyFunct(self.SBPolyVelTData[0])
    #     self.SBPolyAccTData[0] = self.SBPolyVelTData[0]
    #     self.SBPolyAccTData[1] = pdt(self.SBPolyVelTData[0])
        
    #     # ------Beginn   Integration of SBPolyVelTData over Time to get Time Scaling to travel the whole Path
    #     PosI= pint(self.SBPolyVelTData[0,-1])
    #     # ------End   Integration of SBPolyVelTData over Time to get Time Scaling to travel the whole Path  
    #     # ------Beginn Rescale Vel Acc CTPoints anr representation Points - TTPoints TPPoints
    #     self.PosSkalierung2 = self.GrenzParaMinima[0,-1]/(PosI) 
    #     self.SBPolyVelTData[0] = self.SBPolyVelTData[0] *self.PosSkalierung2
    #     self.SBPolyAccTData[0] = self.SBPolyAccTData[0] *self.PosSkalierung2
    #     self.SCTPointsT[0]= self.SCTPointsT[0] *self.PosSkalierung2
    #     for i in range(len(self.TTPoints)):
    #         x =self.TTPoints[i].get_xdata()
    #         self.TTPoints[i].set(xdata=x *self.PosSkalierung2)
    #     for i in range(len(self.TPPoints)):
    #         x =self.TPPoints[i].get_xdata()
    #         self.TPPoints[i].set(xdata=x *self.PosSkalierung2)        
    #     # ------End Rescale Vel Acc CTPoints anr representation Points - TTPoints TPPoints
    #     # ------Beginn   Integration of SBPolyVelTData over Time to get Pos over Time while traveling the whole Path
    #     SP = 0.0
    #     self.SBPolyPosTData = np.zeros((2,len(self.SBPolyVelTData[0])),dtype = np.double)
    #     for i in range(1,len(self.SBPolyVelTData[0])-1):
    #         P = ((-0.5*(self.SBPolyVelTData[1,i-1]+self.SBPolyVelTData[1,i+1]))*(self.SBPolyVelTData[0,i-1]-self.SBPolyVelTData[0,i]))
    #         SP = SP + P
    #         self.SBPolyPosTData[0,i]=self.SBPolyVelTData[0,i]
    #         self.SBPolyPosTData[1,i]=SP
    #     self.SBPolyPosTData[0,-1]=self.SBPolyVelTData[0,-1]
    #     self.SBPolyPosTData[1,-1]=self.GrenzParaMinima[0,-1]
    #     # ------End   Integration of SBPVelTData over Time to get Pos over Time while traveling the whole Path        
    #     # ------Beginn get new Domain changing Functions
    #     self.VelVelToVelPos  = interp1d(self.SBPolyPosTData[0], self.SBPolyPosTData[1], fill_value=np.nan, assume_sorted=True)
    #     self.VelPosToVelTime = interp1d(self.SBPolyPosTData[1], self.SBPolyPosTData[0], fill_value=np.nan, assume_sorted=True)
    #     self.GrenzDataX = self.VelPosToVelTime(self.GrenzParaMinima[0])
    #     self.GrenzDataY = self.GrenzParaMinima[1]
    #     if self.VelEditorFrame:
    #         self.VelEditorFrame.txtMaxTime.SetValue('%3.3f'%(self.SBPolyVelTData[0,-1]-self.SBPolyVelTData[0,0]))
    #         if np.amax(self.GrenzParaMinima[1]) < self.usrVelD:
    #             self.usrVelD = np.amax(self.GrenzParaMinima[1])
    #             self.VelEditorFrame.txtSetupUsrVel.SetValue('%3.3f'%(np.amax(self.GrenzParaMinima[1])))
    #             self.VelEditorFrame.txtSetupUsrVel.SetBackgroundColour('red')
    #         else:
    #             self.VelEditorFrame.txtSetupUsrVel.SetBackgroundColour('white')
    #         self.VelEditorFrame.txtProfileMaxAcc.SetValue('%3.3f'%(np.amax((self.SBPolyAccTData[1]))))
    #         self.VelEditorFrame.txtProfileMaxDcc.SetValue('%3.3f'%(np.amin((self.SBPolyAccTData[1]))))
    #         if np.amax((self.SBPolyAccTData[1])) > float(self.VelEditorFrame.txtSetupMaxAcc.GetValue()):
    #             self.VelEditorFrame.txtProfileMaxAcc.SetBackgroundColour((220,50,50))
    #         elif np.amax((self.SBPolyAccTData[1])) > float(self.VelEditorFrame.txtSetupUsrAcc.GetValue()):
    #             self.VelEditorFrame.txtProfileMaxAcc.SetBackgroundColour((255,190,0))
    #         else:
    #             self.VelEditorFrame.txtProfileMaxAcc.SetBackgroundColour((0,190,0))
    #         if np.amin((self.SBPolyAccTData[1])) < -float(self.VelEditorFrame.txtSetupMaxAcc.GetValue()):
    #             self.VelEditorFrame.txtProfileMaxDcc.SetBackgroundColour((220,50,50))
    #         elif np.amin((self.SBPolyAccTData[1])) < -float(self.VelEditorFrame.txtSetupUsrAcc.GetValue()):
    #             self.VelEditorFrame.txtProfileMaxDcc.SetBackgroundColour((255,190,0))
    #         else:
    #             self.VelEditorFrame.txtProfileMaxDcc.SetBackgroundColour((0,190,0))

    #         self.VelEditorFrame.txtProfileMaxAcc.Update()
    #         self.VelEditorFrame.txtProfileMaxDcc.Update()    
    #         self.VelEditorFrame.txtMaxTime.Update()

    #     self.GrenzVelT       = interp1d(self.GrenzDataX,self.GrenzDataY, bounds_error=False,fill_value=[0])
        
    #     # ------End get new Domain changing Functions        
    #     self.SBPolyVelPData[0] = self.VelVelToVelPos(self.SBPolyVelTData[0])
    #     self.SBPolyVelPData[1] = self.SBPolyVelTData[1]        
     
    def OnSize(self,evt):
        #print 'OnSize'
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
                for i in range(1,len(self.TPPoints)-1):
                    if self.TPPoints[i].contains(evt)[0]:
                        self.hpoint=i
                        self.PhpointX = self.TPPoints[self.hpoint].get_xdata()
                        self.PhpointY = self.TPPoints[self.hpoint].get_ydata()
                        self.TPPoints[self.hpoint].set( color='b')
                        self.modifyP = 'PPoint'
                        self.TTPoints[self.hpoint].set( color= 'b')
                        break
                    else:
                        self.modifyP = 'PI'
            elif evt.inaxes == self.axesT :
                self.rezoom = False
                for i in range(1,len(self.TTPoints)-1):
                    if self.TTPoints[i].contains(evt)[0]:
                        self.hpoint=i
                        self.ThpointX = self.TTPoints[self.hpoint].get_xdata()
                        self.ThpointY = self.TTPoints[self.hpoint].get_ydata()
                        self.TTPoints[self.hpoint].set( color='b')
                        self.modifyP = 'TPoint'
                        self.TPPoints[self.hpoint].set( color= 'b')
                        break
                    else:
                        self.modifyP = 'TI'
            self.MouseDeltaXPoint = 0.0
            self.MouseDeltaYPoint = 0.0
            self.MDDX = 0.
            self.MDDY = 0.
            self.clickpoint = [evt.xdata, evt.ydata]
            self.Refresh()
            #wx.PostEvent(self,wxEVT_PAINT)
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
        elif evt.button == 3:
            self.Pan(evt)
        pass

            
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
            # deal with something that should never happen
            scale_factor = 1
                
        if evt.inaxes == self.axes :
            new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor
            new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor 
            relx = (cur_xlim[1] - xdata)/(cur_xlim[1] - cur_xlim[0])
            rely = (cur_ylim[1] - ydata)/(cur_ylim[1] - cur_ylim[0])
            if(self.xzoom):
                self.axes.set_xlim([xdata - new_width * (1-relx), xdata + new_width * (relx)])
            if(self.yzoom):
                self.axes.set_ylim([ydata - new_height * (1-rely), ydata + new_height * (rely)]) 
        else:
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
        for i in range(len(self.TPPoints)):
            self.TPPoints[self.hpoint].set(color='r')
        for i in range(len(self.TTPoints)):
            self.TTPoints[self.hpoint].set(color='r')
        self.modifyP = 'none'
        self.Refresh()
        #wx.PostEvent(self,wxEVT_PAINT)
        pass
    
    def OnKeyPress(self,evt):
        if evt.key == 'd':
            if (self.modifyP == 'TPoint' or self.modifyP == 'PPoint') and len(self.SCTPointsT[0]) >= 4:                
                self.SCTPointsT = np.delete(self.SCTPointsT,self.hpoint,axis=1)
                self.modifyP = 'none'
                self.RecalcBPolySCT()
                if self.VelEditorFrame:
                    self.VelEditorFrame.btnProfileSave.Enable(True)    
                    self.VelEditorFrame.btnProfileReplace.Enable(True) 
                    self.VelEditorFrame.btnProfileReload.Enable(True)                  
                self.Plot()
                self.Refresh()                
                #wx.PostEvent(self,wx.PaintEvent())
        elif evt.key == 'i' and self.modifyP == 'TI':
            if self.clickpoint[0] > 0.1:
                y = self.BPolyFunct(self.clickpoint[0])
                i = np.searchsorted(self.SCTPointsT[0],self.clickpoint[0])
                self.SCTPointsT = np.insert(self.SCTPointsT,i,[self.clickpoint[0],y],axis =1)
                self.RecalcBPolySCT()
                if self.VelEditorFrame:
                    self.VelEditorFrame.btnProfileSave.Enable(True)    
                    self.VelEditorFrame.btnProfileReplace.Enable(True) 
                    self.VelEditorFrame.btnProfileReload.Enable(True)                 
                self.Plot()
                self.Refresh()                
                #wx.PostEvent(self,wx.PaintEvent())
        elif evt.key == 'i' and self.modifyP == 'PI':
            pass
            if self.clickpoint[0] > 0.1:
                y = self.BPolyFunct(self.VelPosToVelTime(self.clickpoint[0]))
                i = np.searchsorted(self.SCTPointsT[0],self.VelPosToVelTime(self.clickpoint[0]))
                self.SCTPointsT = np.insert(self.SCTPointsT,i,[self.VelPosToVelTime(self.clickpoint[0]),y],axis =1)
                self.RecalcBPolySCT()
                if self.VelEditorFrame:
                    self.VelEditorFrame.btnProfileSave.Enable(True)    
                    self.VelEditorFrame.btnProfileReplace.Enable(True) 
                    self.VelEditorFrame.btnProfileReload.Enable(True) 
                    
                self.Plot()
                self.Refresh()                
                #wx.PostEvent(self,wx.PaintEvent())                
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
            
    def RefreshFunction(self):
        self.Refresh()
        # wx.PostEvent(self,wx.PaintEvent())
        pass
        

class VelEditor4C(wx.App):
    #def __init__(self):
        #self.OnInit()
    def OnInit(self):        
        self.res = xrc.XmlResource('TestWW.xrc')
        self.KeyPointWindow                    = self.res.LoadFrame(None,'ID_WXFRAME')
        self.KeyPointWindow.panelMainPanel     = xrc.XRCCTRL(self.KeyPointWindow,'MainPanel')         
        self.KeyPointWindow.panelOne           = xrc.XRCCTRL(self.KeyPointWindow.panelMainPanel,'PanelOne')
        self.KeyPointWindow.panelVelPath       = xrc.XRCCTRL(self.KeyPointWindow.panelOne,'panelVelPath')        
        self.KeyPointWindow.Diagramm           = Diagramm(self.KeyPointWindow.panelVelPath)        
        self.KeyPointWindow.txtPathLength      = xrc.XRCCTRL(self.KeyPointWindow,'txtPathLength')
        self.KeyPointWindow.txtPathMinTime     = xrc.XRCCTRL(self.KeyPointWindow,'txtPathMinTime')       
        self.KeyPointWindow.txtSetupMaxAcc     = xrc.XRCCTRL(self.KeyPointWindow,'txtSetupMaxAcc')
        self.KeyPointWindow.txtSetupMaxVel     = xrc.XRCCTRL(self.KeyPointWindow,'txtSetupMaxVel')
        self.KeyPointWindow.txtSetupUsrAcc     = xrc.XRCCTRL(self.KeyPointWindow,'txtSetupUsrAcc')
        self.KeyPointWindow.txtSetupUsrVel     = xrc.XRCCTRL(self.KeyPointWindow,'txtSetupUsrVel')
        self.KeyPointWindow.txtMaxTime         = xrc.XRCCTRL(self.KeyPointWindow,'txtMaxTime')
        self.KeyPointWindow.txtMaxDistance     = xrc.XRCCTRL(self.KeyPointWindow,'txtMaxDistance')
        self.KeyPointWindow.txtMouseXPos       = xrc.XRCCTRL(self.KeyPointWindow,'txtMouseXPos')
        self.KeyPointWindow.txtMouseYPos       = xrc.XRCCTRL(self.KeyPointWindow,'txtMouseYPos')
        self.KeyPointWindow.txtProfileMaxAcc   = xrc.XRCCTRL(self.KeyPointWindow,'txtProfileMaxAcc')
        self.KeyPointWindow.txtProfileMaxDcc   = xrc.XRCCTRL(self.KeyPointWindow,'txtProfileMaxDcc')

        self.KeyPointWindow.txtMaxTime.Enable(False)
        self.KeyPointWindow.txtMouseXPos.Enable(False)
        self.KeyPointWindow.txtMouseYPos.Enable(False)
        
        self.Bind(wx.EVT_TEXT_ENTER        , self.EntertxtSetupMaxAcc,      self.KeyPointWindow.txtSetupMaxAcc)
        self.Bind(wx.EVT_TEXT_ENTER        , self.EntertxtSetupMaxVel,      self.KeyPointWindow.txtSetupMaxVel)
        self.Bind(wx.EVT_TEXT_ENTER        , self.EntertxtSetupUsrAcc,      self.KeyPointWindow.txtSetupUsrAcc)
        self.Bind(wx.EVT_TEXT_ENTER        , self.EntertxtSetupUsrVel,      self.KeyPointWindow.txtSetupUsrVel) 
        self.Bind(wx.EVT_TEXT_ENTER        , self.EntertxtMaxTime,          self.KeyPointWindow.txtMaxTime)
        
        # Probleme mit Debug Modus GUI von matplotlib ... daher mal auskomentiert
        #self.Bind(wx.EVT_KILL_FOCUS, self.EntertxtMaxTime,          self.KeyPointWindow.txtMaxTime)
        #self.Bind(wx.EVT_KILL_FOCUS, self.EntertxtSetupMaxAcc,      self.KeyPointWindow.txtSetupMaxAcc)
        #self.Bind(wx.EVT_KILL_FOCUS, self.EntertxtSetupMaxVel,      self.KeyPointWindow.txtSetupMaxVel)
        #self.Bind(wx.EVT_KILL_FOCUS, self.EntertxtSetupUsrAcc,      self.KeyPointWindow.txtSetupUsrAcc)
        #self.Bind(wx.EVT_KILL_FOCUS, self.EntertxtSetupUsrVel,      self.KeyPointWindow.txtSetupUsrVel)        

        self.KeyPointWindow.Show()
        return True

    def EntertxtMaxTime(self,evt):
        evt.Skip()
    def EntertxtSetupMaxAcc(self,evt):
        evt.Skip()        
    def EntertxtSetupMaxVel(self,evt):
         evt.Skip()        
    def EntertxtSetupUsrAcc(self,evt):
        evt.Skip()        
    def EntertxtSetupUsrVel(self,evt):
         evt.Skip()

if __name__ == "__main__":
    app = VelEditor4C()
    app.MainLoop()