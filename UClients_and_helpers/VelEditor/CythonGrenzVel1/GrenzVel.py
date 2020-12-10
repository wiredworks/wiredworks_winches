import numpy as np
from scipy.interpolate import splev, splprep, splrep
from math import sqrt, copysign
import time


    # tckp                      + tckp from splprep
    # Points                    + Coordinates of Yellow, Green,Cyan,Magenta 
    # maxVel                    + max Vel
    # maxAcc                    + max Acc
    # RParameter                + Interpolation density for reparametrization
    # LA                        + Length of running Average Velocity
    # Schiebe                   + Width of Maximum Window
    # LA4                       + Decay of GaussFilter for AccGrenz Para Minima
    # SwitchSchiebe             + Incremental window building or one shot

def GrenzVel(tckp,Points,maxVel,ProzentMaxVel,maxAcc,ProzentMaxAcc,Schiebe,SwitchSchiebe,debug):

    def ChangeToTimeDomain(PathLength, usrVelLimit):
        ########################################################################################################
        ### Domain Wechsel #####################################################################################
        ########################################################################################################

        SumTime = 0.0
        VelTimeAvePara = np.zeros((2,(Teilung-2-1-1)),dtype = np.double)

        for i in range(1,(Teilung-2-1-1)-1):        
            Time = (usrVelLimit[0,i+1]-usrVelLimit[0,i])/((usrVelLimit[1,i+1]+usrVelLimit[1,i])/2)
            SumTime = SumTime+Time
            VelTimeAvePara[0,i]  = SumTime
            VelTimeAvePara[1,i]  = usrVelLimit[1,i]    
        VelTimeAvePara[0,-1] = VelTimeAvePara[0,i]- VelTimeAvePara[1,i]/((VelTimeAvePara[1,i]-VelTimeAvePara[1,i-1])/(VelTimeAvePara[0,i]-VelTimeAvePara[0,i-1]))
        VelTimeAvePara[1,-1] = 0.0
     
        
        #cdef double Parameter    = 0.0
        #cdef double SumParameter = 0.0
        #cdef np.ndarray[np.double_t, ndim=2] ParamTime =np.zeros((2,(Teilung-2-1-1-1)),dtype = np.double)
        
        #for i in range(0,(Teilung-2-1-1)-1):
            #Parameter     = (VelTimeAvePara[0,i+1]-VelTimeAvePara[0,i])*((VelTimeAvePara[1,i+1]+VelTimeAvePara[1,i])/2)
            #SumParameter = SumParameter + Parameter
            #ParamTime[0,i] = VelTimeAvePara[0,i]
            #ParamTime[1,i] = SumParameter

        
        
        #print 'VelTimeAvePara'
        #print VelTimeAvePara
        #print VelTimeAvePara.shape[1]
        
        #cdef double TVelGaussTime = time.time()
        
        ######### Differentiate CutVelTimeIntGrenzParaAverage
        
        AccData  =np.zeros((2,VelTimeAvePara.shape[1]-1),dtype = np.double)
        for i in range(0,VelTimeAvePara.shape[1]-1):
            if (VelTimeAvePara[0,i+1]-VelTimeAvePara[0,i]) == 0.0:
                aY = 100.0
            else:
                aY = ((VelTimeAvePara[1,i+1]-VelTimeAvePara[1,i])/(VelTimeAvePara[0,i+1]-VelTimeAvePara[0,i]))
            AccData[0,i]  = VelTimeAvePara[0,i]-VelTimeAvePara[0,0]
            AccData[1,i]  = aY
        AccData[1,0] = AccData[1,1]
        AccData[1,-1] = AccData[1,-2]
        
        #cdef np.ndarray[np.double_t, ndim=2] AccAccData
        #AccAccData  =np.zeros((2,AccData.shape[1]-1),dtype = np.double)
        #for i in range(0,AccData.shape[1]-1):   
            #aY = ((AccData[1,i+1]-AccData[1,i])/(AccData[0,i+1]-AccData[0,i]))
            #AccAccData[0,i]  = VelTimeAvePara[0,i]-VelTimeAvePara[0,0]
            #AccAccData[1,i]  = aY
        #AccAccData[1,0] = AccAccData[1,1]
        #AccAccData[1,-1] = AccAccData[1,-2]
        
        #print 'AccData'
        #print AccData
        #print AccData.shape[1]
        
        #cdef double TAccTime = time.time()
        SumAveTime = VelTimeAvePara[0,-1]-VelTimeAvePara[0,0]
        MeanVel       = PathLength/SumAveTime
        TotalPathAccTime = SumAveTime
        
        #print SumAveTime
                  
        return VelTimeAvePara, AccData, SumAveTime, MeanVel, TotalPathAccTime



    def Plot(SwitchSchiebe, Schiebe, maxVel, maxAcc, usrAccLimitLines,  TotalPathAccTime, VelTimeAvePara):
        import matplotlib.pyplot as plt
        #import mpl_toolkits.axisartist as AA 
        #import matplotlib.ticker as ticker
        
        ## Seil laengen
        #fig1 = plt.figure('Rope Length')
        #ax1  = plt.axes()
        #ax1.set_title('Rope Length')
        #ax1.plot(YellowPosData[0],  YellowPosData[1],                               'y-',label='GrenzVel',  ms = 10.0)
        #ax1.plot(GreenPosData[0],   GreenPosData[1],                                'g-',label='GrenzVel',  ms = 10.0)
        #ax1.plot(CyanPosData[0],    CyanPosData[1],                                 'c-',label='GrenzVel',  ms = 10.0)
        #ax1.plot(MagentaPosData[0], MagentaPosData[1],                              'm-',label='GrenzVel',  ms = 10.0)
        
        ## Seil Geschwindigkeiten
        #fig2 = plt.figure('Rope Velocities')
        #ax2  = plt.axes()
        #ax2.set_title('Rope Velocities')
        #ax2.plot(YellowVelData[0],  YellowVelData[1],                                'y-',label='GrenzVel',  ms = 10.0)
        #ax2.plot(GreenVelData[0],   GreenVelData[1],                                 'g-',label='GrenzVel',  ms = 10.0)
        #ax2.plot(CyanVelData[0],    CyanVelData[1],                                  'c-',label='GrenzVel',  ms = 10.0)
        #ax2.plot(MagentaVelData[0], MagentaVelData[1],                               'm-',label='GrenzVel',  ms = 1.0)
        #ax2.plot(YellowVelData[0],  1./YellowVelData[1],                             'y-.',label='GrenzVel',  ms = 1.0)
        #ax2.plot(GreenVelData[0],   1./GreenVelData[1],                              'g-.',label='GrenzVel',  ms = 1.0)
        #ax2.plot(CyanVelData[0],    1./CyanVelData[1],                               'c-.',label='GrenzVel',  ms = 1.0)
        #ax2.plot(MagentaVelData[0], 1./MagentaVelData[1],                            'm-.',label='GrenzVel',  ms = 1.0)
        #ax2.set_ylim(-5.,5.)
        
        ## Seil Beschleunigungen 
        #fig3 = plt.figure('Rope Accelerations')
        #ax3  = plt.axes()
        #ax3.set_title('Rope Accelerations') 
        #AccGrenzData[0,0]  = 0.0
        #AccGrenzData[1,0]  = AccGrenzData[1,1]
        #AccGrenzData[1,-1] = AccGrenzData[1,-2]   
        #ax3.plot(YellowAccData[0],  YellowAccData[1],                                'y-',label='GrenzVel',  ms = 10.0)
        #ax3.plot(GreenAccData[0],   GreenAccData[1],                                 'g-',label='GrenzVel',  ms = 10.0)
        #ax3.plot(CyanAccData[0],    CyanAccData[1],                                  'c-',label='GrenzVel',  ms = 10.0)
        #ax3.plot(MagentaAccData[0], MagentaAccData[1],                               'm-',label='GrenzVel',  ms = 10.0)
        #ax3.plot(YellowAccData[0],  np.sqrt(maxAcc/abs(YellowAccData[1])),           'y-.',label='GrenzVel',  ms = 1.)
        #ax3.plot(GreenAccData[0],   np.sqrt(maxAcc/abs(GreenAccData[1])),            'g-.',label='GrenzVel',  ms = 1.)
        #ax3.plot(CyanAccData[0],    np.sqrt(maxAcc/abs(CyanAccData[1])),             'c-.',label='GrenzVel',  ms = 1.)
        #ax3.plot(MagentaAccData[0], np.sqrt(maxAcc/abs(MagentaAccData[1])),          'm-.',label='GrenzVel',  ms = 1.) 
        #ax3.set_ylim(-20,20)
    
        # 
        #fig4 = plt.figure('Limits due to Velocities')
        #ax4  = plt.axes()
        #ax4.set_title('Limits due to Velocities') 
        #ax4.plot(YellowVelData[0],  AvvYg[1],                                        'y-',label='GrenzVel',  ms = 1.)
        #ax4.plot(GreenVelData[0],   AvvGg[1],                                        'g-',label='GrenzVel',  ms = 1.)
        #ax4.plot(CyanVelData[0],    AvvCg[1],                                        'c-',label='GrenzVel',  ms = 1.)
        #ax4.plot(MagentaVelData[0], AvvMg[1],                                        'm-',label='GrenzVel',  ms = 1.)
        #ax4.plot(VelGrenzData[0],   VelGrenzData[1],                                 'r-',label='GrenzVel',  ms = 10.0)
        #ax4.set_ylim(-20,20)
        
        fig=plt.figure('Composition of Vel Limits')
        ax=fig.add_subplot(111)
        #ax.set_ylim(-1,20)
        #ax.yaxis.set_major_locator(ticker.LinearLocator(5))
        #ax.yaxis.set_ticks_position('left')
        #ax.tick_params(which='major', width=1.00)
        #ax.tick_params(which='major', length=5)        

        ax.grid(True)

        #ax.plot(AccGrenzParaMinima[0],        AccGrenzParaMinima[1],                 'xkcd:ruby', '-',label='Acc VelLimit',  ms = 10.0,)
        ax.plot(AccGrenzData[0],              AccGrenzData[1],                       'xkcd:rosy pink'         , '-',label='Limit Acc',  ms = 10.0)        
        ax.plot(VelGrenzData[0],              VelGrenzData[1],                       'xkcd:stormy blue'  , '-',label='Limit Vel',  ms = 10.0)
        ax.plot(usrVelGrenzData[0],           usrVelGrenzData[1],                    'xkcd:off blue'   , '-',label='Limit Vel',  ms = 10.0) 
        ax.plot(usrVelLimit[0],           usrVelLimit[1],                    'xkcd:pale green', '-'   ,label='VelLimit',  ms = 10.0)
        ax.fill(usrVelLimit[0],           usrVelLimit[1],                    color="xkcd:pale green"  ,      alpha = 0.3) 
        #ax.plot(Out4[0],Out4[1],                                                     'xkcd:pale green', '-',label='Acc VelLimit',  ms = 10.0,  )
        #ax.plot(Out7[0],Out7[1],                                                     'xkcd:mint green','-',label='Acc VelLimit',  ms = 10.0   )  
        ax.scatter(CPoints[0],CPoints[1])
        
        #ax2 = ax.twiny()
        #ax2.plot(VelTimeAvePara[0],VelTimeAvePara[1],                                 'xkcd:olive','-',label='Acc VelLimit',  ms = 10.0 ) 
        #ax2.minorticks_on()
 #++++++       
        ##fig5 = plt.figure('Limits due to Accelerations')
        ##ax5  = plt.axes()
        ##ax5.set_title('Limits due to Accelerations')     
        ##ax5.plot(YellowAccData[0],  AvaYg[1],                                        'y-',label='GrenzVel',  ms = 1.)
        ##ax5.plot(GreenAccData[0],   AvaGg[1],                                        'g-',label='GrenzVel',  ms = 1.)
        ##ax5.plot(CyanAccData[0],    AvaCg[1],                                        'c-',label='GrenzVel',  ms = 1.)
        ##ax5.plot(MagentaAccData[0], AvaMg[1],                                        'm-',label='GrenzVel',  ms = 1.) 
        ##ax5.plot(AccGrenzData[0],   AccGrenzData[1],                                 'r-',label='GrenzVel',  ms = 10.0)
        ##ax5.set_ylim(-50,50)
        #fig6 = plt.figure('Composition of Vel Limits')
        ##fig6.subplots_adjust(right=1.)
        #ax6 = AA.Subplot(fig6, 1, 1, 1)
        #fig6.add_subplot(ax6)        
        ##ax6  = plt.axes()
        #ax6.grid(which="major", linewidth=1)
        #ax6.minorticks_on()
        #ax6.axis["left"].label.set_text("Velocity")
        ##ax6.axis["left"].toggle(all=True)
        #ax6.set_yticks([-10,-5,0,5,10,15,20,25,30])
        #ax6.axis["bottom"].label.set_text("Position")
        #ax6.set_title('MaxAcc: %2.2f MaxVel: %2.2f UsrAcc: %2.2f UsrVel: %2.2f\n Fenster: %i Switch: %i RParam: %i Density: %3.2f'%(maxAcc,maxVel,usrAcc,usrVel,Schiebe,SwitchSchiebe,RParameter,Density))          
        #ax6.plot(AccGrenzData[0],              AccGrenzData[1],                       'xkcd:rosy pink'         , '-',label='Limit Acc',  ms = 10.0)        
        #ax6.plot(VelGrenzData[0],              VelGrenzData[1],                       'xkcd:stormy blue'  , '-',label='Limit Vel',  ms = 10.0)
        #ax6.plot(usrVelGrenzData[0],           usrVelGrenzData[1],                    'xkcd:off blue'   , '-',label='Limit Vel',  ms = 10.0)
        ##ax6.plot(GrenzPara[0],                GrenzPara[1],                          'xkcd:pale green', '-'   ,label='GrenzVel',  ms = 10.0)
        #ax6.plot(GrenzParaMinima[0],           GrenzParaMinima[1],                    'xkcd:pale green', '-'   ,label='VelLimit',  ms = 10.0)
        #ax6.fill(GrenzParaMinima[0],           GrenzParaMinima[1],                    color="xkcd:pale green"  ,      alpha = 0.3)
        ##ax6.plot(GrenzPara[0],                GrenzParaSpline[1],                    'xkcd:pale green', '-',label='GrenzVel',  ms = 10.0)
        #ax6.plot(AccGrenzParaMinima[0],        AccGrenzParaMinima[1],                 'xkcd:ruby', '-',label='Acc VelLimit',  ms = 10.0,)
        #ax6.plot(usrAccLimitLines[0],          usrAccLimitLines[1],                        'xkcd:hot pink', '-',label='Acc VelLimit',  ms = 10.0,)
          
        ##ax6.plot(AccAccGrenzParaMinima[0],     AccAccGrenzParaMinima[1],             'xkcd:pale green', '-',label='Acc VelLimit',  ms = 10.0,)
      ## Beginn Offset Plots  
        ##ax6.plot( Out[0], Out[1],                                                    'xkcd:pale green', '-',label='Acc VelLimit',  ms = 10.0,  )
        ##ax6.plot(Out1[0],Out1[1],                                                    'xkcd:pale green', '-',label='Acc VelLimit',  ms = 10.0,  )
        ##ax6.plot(Out2[0],Out2[1],                                                    'xkcd:pale green', '-',label='Acc VelLimit',  ms = 10.0,  )
        ##ax6.plot(Out3[0],Out3[1],                                                    'xkcd:pale green', '-',label='Acc VelLimit',  ms = 10.0,  )
        #ax6.plot(Out4[0],Out4[1],                                                     'xkcd:pale green', '-',label='Acc VelLimit',  ms = 10.0,  )
        ##ax6.plot(Out5[0],Out5[1],                                                    'xkcd:pale green', '-',label='Acc VelLimit',  ms = 10.0,  )
        ##ax6.plot(Out6[0],Out6[1],                                                    'xkcd:pale green', '-',label='Acc VelLimit',  ms = 10.0,  )        
        #ax6.plot(Out7[0],Out7[1],                                                     'xkcd:olive','-',label='Acc VelLimit',  ms = 10.0   )
      ## End Offset Plots 
      ## Begin Time Domain
        #ax11 = ax6.twinx()
        #ax11.plot(VelTimeAvePara[0],          VelTimeAvePara[1],                        'xkcd:olive', '-',label='Acc VelLimit',  ms = 10.0,)
        #print VelTimeAvePara
      ## End Time DOmain
    
        ##ax6.set_ylim((np.amin(AccGrenzParaMinima[1])),max(np.amax(AccGrenzData[1]),np.amax(VelGrenzData[1])))
        #ax6.scatter(CPoints[0],CPoints[1])
        ##ax6.scatter(CPointsA[0],CPointsA[1])
        ##ax6.legend(loc=1)
 #+++++ 
        
        #fig7 = plt.figure('Vel Limits')
        #ax7  = plt.axes()
        #ax7.set_title('Vel Limits') 
        #ax7.plot(GrenzParaMinima[0],      GrenzParaMinima[1],                         'b-',label='GrenzVel',  ms = 10.0)     
        
        #from mpl_toolkits.mplot3d import Axes3D
        #fig8 = plt.figure('Path')
        #ax8 =  plt.axes(projection='3d',title='Path',label='1')
        #ax8.plot(PathPosX,PathPosY,PathPosZ)
        #plt.show()         
        #try:
            #plt = None
        #except:
            #pass
        #import matplotlib.pyplot as plt
        #plt.ioff()
        #fig9 = plt.figure('Time Domain')
        #ax9 = fig9.add_subplot(2,1,1)
    
        #ax9.set_title('Max Acc : %2.2f MaxVel : %2.2f \n Fenster : %i Switch : %i RParam : %i Density : %3.2f'%(maxAcc,maxVel,Schiebe,SwitchSchiebe,RParameter,Density))          
        #ax9.plot(GrenzParaMinima[0],  GrenzParaMinima[1],                          'm-',label='GrenzVel',  ms = 10.0)
        #ax9.fill(GrenzParaMinima[0], GrenzParaMinima[1],                               color="m",      alpha = 0.3)
        ##ax9.plot(AccGrenzPara[0], AccGrenzPara[1],                                'g-',label='Parabeln',  ms = 10.0)
        #ax9.plot(AccGrenzParaMinima[0], AccGrenzParaMinima[1],                     'b-',label='Filtered',  ms = 1.0)
        #ax9.grid(True)
        #ax9.axhline()
        ##pl.legend()
        #ax10 = fig9.add_subplot(2,1,2,sharex=ax9)
        
        #ax10.set_title('Time Domain MinTime : %3.2f PTime : %3.2f'%( TotalPathAccTime,SumAveTime))
        #ax10.plot(VelTimeAvePara[0]-VelTimeAvePara[0,0], VelTimeAvePara[1],        'c-',label='Acc gefeilt /Time', ms = 1.0)
        #ax10.plot(AccData[0] , AccData[1],                                         'g-',label='Acc gefeilt /Time', ms = 1.0) 
        #ax10.grid(True)
        #fig9.subplots_adjust(hspace=0.3)
        #plt.legend()
        plt.show()

        
    
    def InitVars(ProzentMaxVel, ProzentMaxAcc, maxAcc, maxVel, Points):
        # *** Beginn Init Vars
        ProzentMaxVel = max(min(ProzentMaxVel,1),0.1)
        ProzentMaxAcc = max(min(ProzentMaxAcc,1),0.1)
        usrAcc = ProzentMaxAcc*maxAcc
        usrVel = ProzentMaxVel*maxVel
        Off = 0.5
        
        RParameter = 100000
        
        Density = 100.0
        
        YPx = Points[0][0]
        YPy = Points[0][1]
        YPz = Points[0][2]
        GPx = Points[1][0]
        GPy = Points[1][1]
        GPz = Points[1][2]
        CPx = Points[2][0]
        CPy = Points[2][1]
        CPz = Points[2][2]
        MPx = Points[3][0]
        MPy = Points[3][1]
        MPz = Points[3][2]
    
        YellowPoint  = np.array([YPx,YPy,YPz])
        GreenPoint   = np.array([GPx,GPy,GPz])
        CyanPoint    = np.array([CPx,CPy,CPz])
        MagentaPoint = np.array([MPx,MPy,MPz])
        
        # *** End Init Vars    
        return usrVel, usrAcc, RParameter, Density, Off, YellowPoint, GreenPoint, CyanPoint, MagentaPoint    
    def PathLength(RParameter, tckp):
        # *** Beginn PathLength        
        ParamIn = np.linspace(0,1,RParameter)
        W = np.linspace(0,1,RParameter)

        SegmentPunkteX,SegmentPunkteY,SegmentPunkteZ = splev(W,tckp)
        
        SumLengthU = np.zeros(RParameter,dtype = np.double)
        for i in range(1, RParameter):
            SumLengthU[i]= SumLengthU[i-1]+ sqrt((SegmentPunkteX[i]-SegmentPunkteX[i-1])**2+
                                                 (SegmentPunkteY[i]-SegmentPunkteY[i-1])**2+
                                                 (SegmentPunkteZ[i]-SegmentPunkteZ[i-1])**2)
        
        PathLength = SumLengthU[RParameter-1]        
        #*** End Path Length
        return ParamIn, SumLengthU, PathLength

    def Reparametrize(SumLengthU, ParamIn, Density, PathLength):
        #*** Beginn Umparametrierung 
        tckP1 = splrep(SumLengthU, ParamIn, w=None, xb=None, xe=None, k=3, task=0, s=0, t=None,full_output=0, per=0, quiet =1) 
        
        Teilung = int(PathLength*Density)+1
        Density = Teilung/PathLength
        
        PosIntervalle = np.linspace(0,PathLength,Teilung)        
        Param = splev(PosIntervalle, tckP1) 
        #*** End Umparametrierung
        return tckP1,Teilung, Density, Param
    
    def RopeLength(Param, tckp, Teilung, Density, YellowPoint, GreenPoint, CyanPoint, MagentaPoint):
        #*** Beginn Pos Data --- Laengen der Seile        
        PathPosX,PathPosY,PathPosZ = splev(Param,tckp)
        
        YellowPosData   = np.zeros((2,Teilung),dtype = np.double)
        GreenPosData    = np.zeros((2,Teilung),dtype = np.double)
        CyanPosData     = np.zeros((2,Teilung),dtype = np.double)
        MagentaPosData  = np.zeros((2,Teilung),dtype = np.double)
        
        for i in range(0, Teilung):
                YellowPosData[0,i] = i/Density 
                YellowPosData[1,i] = sqrt((PathPosX[i]   - YellowPoint[0])**2+
                                         (PathPosY[i]   - YellowPoint[1])**2+
                                         (PathPosZ[i]   - YellowPoint[2])**2)
                
                GreenPosData[0,i] = i/Density
                GreenPosData[1,i] = sqrt((PathPosX[i]   - GreenPoint[0])**2+
                                        (PathPosY[i]   - GreenPoint[1])**2+
                                        (PathPosZ[i]   - GreenPoint[2])**2)
                
                CyanPosData[0,i] = i/Density
                CyanPosData[1,i] = sqrt((PathPosX[i]   - CyanPoint[0])**2+
                                       (PathPosY[i]   - CyanPoint[1])**2+
                                       (PathPosZ[i]   - CyanPoint[2])**2)
                MagentaPosData[0,i] = i/Density
                MagentaPosData[1,i] = sqrt((PathPosX[i]   - MagentaPoint[0])**2+
                                          (PathPosY[i]   - MagentaPoint[1])**2+
                                          (PathPosZ[i]   - MagentaPoint[2])**2)

        #print 'PosData'
        #print YellowPosData
        #print YellowPosData.shape[1] 
        
        #*** End Positionsdata
        return YellowPosData, GreenPosData, CyanPosData, MagentaPosData
    
    def DerivatePosFirst(Teilung, PathLength, YellowPosData, Density, GreenPosData, CyanPosData, MagentaPosData, maxVel, usrVel):
        #*** Beginn d Seillaengen/ d Parameter        
        VelIntervalle = np.linspace(0,PathLength,Teilung-1)
        
        YellowVelData      = np.zeros((2,Teilung-1),dtype = np.double)
        GreenVelData       = np.zeros((2,Teilung-1),dtype = np.double)
        CyanVelData        = np.zeros((2,Teilung-1),dtype = np.double)
        MagentaVelData     = np.zeros((2,Teilung-1),dtype = np.double)
        
        AvvYg              = np.zeros((2,Teilung-1),dtype = np.double)
        AvvGg              = np.zeros((2,Teilung-1),dtype = np.double)
        AvvCg              = np.zeros((2,Teilung-1),dtype = np.double)
        AvvMg              = np.zeros((2,Teilung-1),dtype = np.double)
        
        vG                 = np.zeros((2,Teilung-1),dtype = np.double)
        VelGrenzData       = np.zeros((2,Teilung-1),dtype = np.double)
        usrVelGrenzData    = np.zeros((2,Teilung-1),dtype = np.double)

        for i in range(0,Teilung-1):
            vY  = ((YellowPosData[1,i+1]-YellowPosData[1,i])/
                   (YellowPosData[0,i+1]-YellowPosData[0,i]))         
            YellowVelData[0,i] = i/Density
            YellowVelData[1,i] = vY
            vG = ((GreenPosData[1,i+1]-GreenPosData[1,i])/
                  (GreenPosData[0,i+1]-GreenPosData[0,i]))
            GreenVelData[0,i]  = i/Density
            GreenVelData[1,i]  = vG
            vC = ((CyanPosData[1,i+1]-CyanPosData[1,i])/
                  (CyanPosData[0,i+1]-CyanPosData[0,i]))
            CyanVelData[0,i]   = i/Density
            CyanVelData[1,i]   = vC
            vM = ((MagentaPosData[1,i+1]-MagentaPosData[1,i])/
                  (MagentaPosData[0,i+1]-MagentaPosData[0,i]))
            MagentaVelData[0,i] = i/Density
            MagentaVelData[1,i] = vM
            
            AvvYg[1,i] = maxVel* (1./abs(vY))
            AvvGg[1,i] = maxVel* (1./abs(vG))
            AvvCg[1,i] = maxVel* (1./abs(vC))
            AvvMg[1,i] = maxVel* (1./abs(vM)) 
            
            vvYg = maxVel* (1./abs(vY))
            vvGg = maxVel* (1./abs(vG))
            vvCg = maxVel* (1./abs(vC))
            vvMg = maxVel* (1./abs(vM))        
            
            vG = min(vvYg,vvGg,vvCg,vvMg)
            
            VelGrenzData[0,i]  = VelIntervalle[i]
            VelGrenzData[1,i]  = vG 
            
            usrVelGrenzData[0,i]  = VelIntervalle[i]
            usrVelGrenzData[1,i]  = usrVel         
                
        #print 'VelData'
        #print YellowVelData
        #print YellowVelData.shape[1]
  
        #*** End d Seillaengen/ d Parameter
        return YellowVelData, GreenVelData, CyanVelData, MagentaVelData, VelGrenzData, usrVelGrenzData
    
    def DerivatePosSecond(Teilung, PathLength, YellowVelData, GreenVelData, CyanVelData, MagentaVelData, maxAcc):
        #*** Beginn d**2 Seillaenge / d Parameter**2        
        AccIntervalle = np.linspace(0,PathLength,Teilung-2)
        
        YellowAccData         = np.zeros((2,Teilung-2),dtype = np.double)
        GreenAccData          = np.zeros((2,Teilung-2),dtype = np.double)
        CyanAccData           = np.zeros((2,Teilung-2),dtype = np.double)
        MagentaAccData        = np.zeros((2,Teilung-2),dtype = np.double)
        
        AvaYg        = np.zeros((2,Teilung-2),dtype = np.double)
        AvaGg        = np.zeros((2,Teilung-2),dtype = np.double)
        AvaCg        = np.zeros((2,Teilung-2),dtype = np.double)
        AvaMg        = np.zeros((2,Teilung-2),dtype = np.double)
        
        aG          = np.zeros((2,Teilung-2),dtype = np.double)     
        AccGrenzData          = np.zeros((2,Teilung-2),dtype = np.double)

        for i in range(0,Teilung-2):   
            aY = ((YellowVelData[1,i+1]-YellowVelData[1,i])/
                  (YellowVelData[0,i+1]-YellowVelData[0,i]))
            YellowAccData[0,i]  = AccIntervalle[i]
            YellowAccData[1,i]  = aY
            aG = ((GreenVelData[1,i+1]-GreenVelData[1,i])/
                  (GreenVelData[0,i+1]-GreenVelData[0,i]))
            GreenAccData[0,i]   = AccIntervalle[i]
            GreenAccData[1,i]   = aG
            aC = ((CyanVelData[1,i+1]-CyanVelData[1,i])/
                  (CyanVelData[0,i+1]-CyanVelData[0,i]))
            CyanAccData[0,i]    = AccIntervalle[i]
            CyanAccData[1,i]    = aC
            aM = ((MagentaVelData[1,i+1]-MagentaVelData[1,i])/
                  (MagentaVelData[0,i+1]-MagentaVelData[0,i]))
            MagentaAccData[0,i] = AccIntervalle[i]
            MagentaAccData[1,i] = aM 
            
            AvaYg[1,i] = np.sqrt(maxAcc/abs(aY))
            AvaGg[1,i] = np.sqrt(maxAcc/abs(aG))
            AvaCg[1,i] = np.sqrt(maxAcc/abs(aC))
            AvaMg[1,i] = np.sqrt(maxAcc/abs(aM))
            
            vaYg = np.sqrt(maxAcc/abs(aY))
            vaGg = np.sqrt(maxAcc/abs(aG))
            vaCg = np.sqrt(maxAcc/abs(aC))
            vaMg = np.sqrt(maxAcc/abs(aM))
            
            aG = min(vaYg,vaGg,vaCg,vaMg)
            
            AccGrenzData[0,i]  = AccIntervalle[i]
            AccGrenzData[1,i]  = aG
            
        AccGrenzData[0,0]  = 0.0
        AccGrenzData[1,0]  = 0.001
        AccGrenzData[1,-1] = 0.001     
        #print 'AccData'
        #print YellowAccData
        #print YellowAccData.shape[1]
        
        #*** End d**2 Seillaenge / d Parameter**2
        return AccGrenzData
    
    def FindRawMin(Teilung, AccGrenzData, VelGrenzData, usrVelGrenzData):
        #*** Beginn Find Minimum -- either VelGrenz or AccGrenz         
        GrenzData          = np.zeros((2,Teilung-2),dtype = np.double)        
        for i in range(0,Teilung-2):
            GrenzData[1,i]=min(VelGrenzData[1,i],AccGrenzData[1,i],usrVelGrenzData[1,i])
            GrenzData[0,i]=AccGrenzData[0,i]            
        #*** End Find Minimum -- either VelGrenz or AccGrenz
        return GrenzData
    
    def InsertRoots(Teilung, GrenzData, maxAcc):
        #*** Beginn rising Roots        
        GrenzDataFilter=np.zeros((2,Teilung-2-1),dtype = np.double) 
        Intervall = 1.0/(GrenzData[0,1]-GrenzData[0,0])         
        Flag0 = 1
        l = 0
        for i in range(0,Teilung-2-1):
            if ((GrenzData[1,i+1]-GrenzData[1,i])/
                (GrenzData[0,i+1]-GrenzData[0,i]) > maxAcc/GrenzData[1,i]) and Flag0 ==0:
                Flag0 = 1
                if l == 0 :
                    l = i
                GrenzDataFilter[0,i] = GrenzData[0,i]
                GrenzDataFilter[1,i] = ParaUp(GrenzData[0,l],GrenzData[1,l],maxAcc,i,Intervall)
            else:
                if Flag0 ==1:
                    GrenzDataFilter[0,i] = GrenzData[0,i]
                    GrenzDataFilter[1,i] = ParaUp(GrenzData[0,l],GrenzData[1,l],maxAcc,i,Intervall)
                    if GrenzDataFilter[1,i] > GrenzData[1,i]:
                        Flag0 = 0 ; l = 0
                else:
                    GrenzDataFilter[0,i] = GrenzData[0,i]
                    GrenzDataFilter[1,i] = GrenzData[1,i]
                    l = 0                    
        #*** End rising Roots
        #*** Beginn falling Roots
        GrenzDataFilter1=np.zeros((2,Teilung-2),dtype = np.double)         
        Flag0 = 1
        l = Teilung-2-1
        for i in range(Teilung-2-1,0,-1):

            if ((GrenzData[1,i-1]-GrenzData[1,i])/
                (GrenzData[0,i-1]-GrenzData[0,i]) <- maxAcc/GrenzData[1,i]) and Flag0 ==0:
                Flag0 = 1
                if l == 0 :
                    l = i
                    GrenzDataFilter1[0,i] = GrenzData[0,i]
                    GrenzDataFilter1[1,i] = ParaDown(GrenzData[0,l],GrenzData[1,l],maxAcc,i,Intervall)
            else:
                if Flag0 ==1:
                    GrenzDataFilter1[0,i] = GrenzData[0,i]
                    GrenzDataFilter1[1,i] = ParaDown(GrenzData[0,l],GrenzData[1,l],maxAcc,i,Intervall)
                    if GrenzDataFilter1[1,i] > GrenzData[1,i]:
                        Flag0 = 0; l = 0
                else: 
                    GrenzDataFilter1[0,i] = GrenzData[0,i]
                    GrenzDataFilter1[1,i] = GrenzData[1,i]
                    l = 0
        GrenzDataFilter1[1,-1]=0.01
        #*** End falling Roots
        #*** Beginn find minimum    
        GrenzPara  =np.zeros((2,Teilung-2),dtype = np.double)
        for i in range(0,Teilung-2-1):
            GrenzPara[0,i] = GrenzDataFilter1[0,i]
            GrenzPara[1,i] = min(GrenzDataFilter1[1,i],GrenzDataFilter[1,i])            
        GrenzPara[0,-1] = PathLength        
        #*** End find minimum        
        return GrenzPara

    def AccGrenzPara(Teilung, GrenzPara):
        # Differentiate GrenzPara
        AccGrenzPara  =np.zeros((2,Teilung-2-1),dtype = np.double)
        for i in range(0,Teilung-2-1):
            Acc = (GrenzPara[1,i+1]-GrenzPara[1,i])/(GrenzPara[0,i+1]-GrenzPara[0,i])
            AccGrenzPara[0,i]= GrenzPara[0,i]
            AccGrenzPara[1,i]= Acc #max(min(AccAcc,4),-4)
        AccGrenzPara[1,-1] = AccGrenzPara[1,-2]
        return AccGrenzPara

    def PeakKiller(Teilung, GrenzPara):
        #*** Beginn Find Small Peak Maxima and Replace by Zeroes
        Schiebe = 20        # >= 20 sonst passen Dimensionen nicht
        SwitchSchiebe = 1 
        
        GrenzParaRR = np.zeros((Teilung-2-1),dtype = np.double)   #AccGrenzPara.shape[1]
        GrenzParaRL = np.zeros((Teilung-2-1),dtype = np.double) #AccGrenzPara.shape[1]
        Zeros       = np.zeros(GrenzPara.shape[1],dtype = np.double)
        GrenzParaM  = np.copy(GrenzPara)
        if SwitchSchiebe == 1 :
            for i in range (1,int(Schiebe/10)):        
                GrenzParaRR   = np.roll(GrenzPara[1],i*10)        
                GrenzParaRL   = np.roll(GrenzPara[1],(Teilung-2-1)-i*10) 
                GrenzParaM    = np.vstack((GrenzPara[0],np.where(((GrenzPara[1] >= GrenzParaRR) & (GrenzPara[1] >= GrenzParaRL)),Zeros,GrenzParaM[1])))
        else:
            GrenzParaRR       = np.roll(GrenzPara[1],Schiebe)        
            GrenzParaRL       = np.roll(GrenzPara[1],-Schiebe) 
            GrenzParaM = np.vstack((GrenzPara[0],np.where(((GrenzPara[1] >= GrenzParaRR[1]) & (GrenzPara[1] >= GrenzParaRL[1])),Zeros,GrenzParaM[1])))
        GrenzParaZeros = np.copy(GrenzParaM)
        #*** End Find Small Peak Maxima and Replace by Zeroes
        #*** Beginn Substitute Zeroes by Cubic Spline 
        GrenzParaSpline  =np.zeros((2,Teilung-2),dtype = np.double)
        j = 0
        for i in range(2,(Teilung-2-1-1)):
            if GrenzParaM[1,i]== 0:
                APointX  = GrenzPara[0,i]
                APointY  = GrenzPara[1,i]
                A1PointX = GrenzPara[0,i-1]
                A1PointY = GrenzPara[1,i-1]
                while (GrenzParaM[1,i+j]== 0.0):
                    j=j+1
            BPointX  = GrenzPara[0,i+j-1]
            BPointY  = GrenzPara[1,i+j-1]
            B1PointX = GrenzPara[0,i+j]
            B1PointY = GrenzPara[1,i+j]
            if j > 0:
                for n in range(0,j+3):
                    if j-1 == 0:
                        p = 0
                    else:
                        m = j-1
                        p = (n-1)/float(m)
                    y =EvaluateSplineY(APointX,APointY,A1PointX,A1PointY,BPointX,BPointY,B1PointX,B1PointY, p)
                    GrenzParaM[1,i+n-2] = y
                    GrenzParaSpline[1,i+n-2] = y 
            j=0
        
        #*** End Substitute Zeroes by Cubic Spline
        #*** Beginn find minimum
        
        GrenzParaMinima  =np.zeros((2,Teilung-2),dtype = np.double)
        for i in range(0,Teilung-2):
            GrenzParaMinima[0,i] = GrenzParaM[0,i]
            GrenzParaMinima[1,i] = min(GrenzPara[1,i],GrenzParaM[1,i])
        
        #*** End find minimum        
        return GrenzParaM, GrenzParaMinima
    
    def usrAccLimitLines(Teilung, GrenzParaMinima, usrAcc):
        #*** Beginn usrAcc Limit Lines
        #usrAcc = 1.
        CPointsAX=[]
        CPointsAY=[]
        sf= 0
        usrVelLimit  =np.zeros((2,Teilung-2),dtype = np.double)    
        for i in range(0,Teilung-2-1):
            if usrAcc * GrenzParaMinima[0,i] <= GrenzParaMinima[1,i]:
                usrVelLimit[0,i] = GrenzParaMinima[0,i]
                usrVelLimit[1,i] = usrAcc * GrenzParaMinima[0,i]
                j=i
            elif usrAcc * (GrenzParaMinima[0,-1]-GrenzParaMinima[0,i]) <= GrenzParaMinima[1,i] :
                usrVelLimit[0,i] = GrenzParaMinima[0,i]
                usrVelLimit[1,i] = usrAcc * (GrenzParaMinima[0,-1]-GrenzParaMinima[0,i])
                if sf == 0:
                    k=i ; sf = 1
            else:
                usrVelLimit[0,i] = GrenzParaMinima[0,i]
                usrVelLimit[1,i] = GrenzParaMinima[1,i]
        usrVelLimit[0,-1] = GrenzParaMinima[0,-1]
        usrVelLimit[1,-1] = 0.
        
        CPointsAX.append(GrenzParaMinima[0,j])
        CPointsAY.append(GrenzParaMinima[1,j])
        CPointsAX.append(GrenzParaMinima[0,k])
        CPointsAY.append(GrenzParaMinima[1,k])        
        
        CPointsANX = np.array(CPointsAX)
        CPointsANY = np.array(CPointsAY)
        CPointsA   = np.stack((CPointsANX,CPointsANY))        
        #*** End usrAcc Limit Lines
        return usrVelLimit, CPointsA



    def FindCPoints(Teilung, GrenzParaMinima, CPointsA):
        #*** Beginn Find ControlPoints
        #### Differentiate GrenzParaMinima
   
        AccGrenzParaMinima  =np.zeros((2,Teilung-2-3),dtype = np.double)
        for i in range(0,Teilung-2-3):
            Acc = (GrenzParaMinima[1,i+1]-GrenzParaMinima[1,i])/(GrenzParaMinima[0,i+1]-GrenzParaMinima[0,i])
            AccGrenzParaMinima[0,i]= GrenzParaMinima[0,i]
            AccGrenzParaMinima[1,i]= Acc
        AccGrenzParaMinima[1,-1] = AccGrenzParaMinima[1,-2]
        AccGrenzParaMinima[1,0]  = AccGrenzParaMinima[1,1]


        AccAccGrenzParaMinima  =np.zeros((2,Teilung-2-4),dtype = np.double)
        for i in range(0,Teilung-2-4):
            Acc = (AccGrenzParaMinima[1,i+1]-AccGrenzParaMinima[1,i])/(AccGrenzParaMinima[0,i+1]-AccGrenzParaMinima[0,i])
            AccAccGrenzParaMinima[0,i]= GrenzParaMinima[0,i]
            AccAccGrenzParaMinima[1,i]= Acc
        AccAccGrenzParaMinima[1,-1] = AccGrenzParaMinima[1,-2]
        AccAccGrenzParaMinima[1,0] = AccGrenzParaMinima[1,1]
        
        CPointsX=[]
        CPointsY=[]
        c = 0 ; CFlag = 0 
        for i in range(Teilung-2-4):
            if ((copysign(1, AccGrenzParaMinima[1,i-1]) != copysign(1,AccGrenzParaMinima[1,i])) or
                AccGrenzParaMinima[1,i] == 0 and AccAccGrenzParaMinima[1,i-1] != 0):
               # and (abs(CPointsX[-1]-GrenzParaMinima[0,i]) > PathLength/50.):
                CPointsX.append(GrenzParaMinima[0,i])
                CPointsY.append(GrenzParaMinima[1,i])    
        CPointsX.append(GrenzParaMinima[0,-1])
        CPointsY.append(0.)

        for i in range(len(CPointsA[0])):
            CPointsX.append(CPointsA[0,i])
        for i in range(len(CPointsA[1])):    
            CPointsY.append(CPointsA[1,i])
        CPointsNX = np.array(CPointsX)
        CPointsNY = np.array(CPointsY)
        CPoints = np.stack((CPointsNX,CPointsNY))
        CPoints = np.transpose(CPoints)
        ind = np.argsort(CPoints[:,0])
        CPoints=CPoints[ind]
        CPoints = np.transpose(CPoints)
        #CPoints[0,0]= 0. ; CPoints[1,0]=0.
        #CPoints[0,-1]=GrenzParaMinima[0,-1] ; CPoints[1,-1]=0.

        #*** End FindControlpoints
        return CPoints, AccGrenzParaMinima

    def Offset(Teilung, GrenzParaMinima, Off, GrenzParaM):
        #*** Beginn Offset
        Out  =np.zeros((2,Teilung-2),dtype = np.double)
        Out1 =np.zeros((2,Teilung-2),dtype = np.double)
        Out2 =np.zeros((2,Teilung-2),dtype = np.double)
        Out3 =np.zeros((2,Teilung-2),dtype = np.double)
        Out4 =np.zeros((2,Teilung-2),dtype = np.double)
        Out5 =np.zeros((2,Teilung-2),dtype = np.double)
        Out6 =np.zeros((2,Teilung-2),dtype = np.double)
        Out7 =np.zeros((2,Teilung-2),dtype = np.double)
        Out7 =np.zeros((2,Teilung-2),dtype = np.double)
        for i in range(0,Teilung-2-1):
            Out[0,i]= GrenzParaMinima[0,i]+ ((GrenzParaMinima[1,i+1]-GrenzParaMinima[1,i]) /
                                             sqrt((GrenzParaMinima[0,i+1]-GrenzParaMinima[0,i])**2+(GrenzParaMinima[1,i+1]-GrenzParaMinima[1,i])**2)*Off)
            Out[1,i]= GrenzParaMinima[1,i]- ((GrenzParaMinima[0,i+1]-GrenzParaMinima[0,i]) /
                                             sqrt((GrenzParaMinima[0,i+1]-GrenzParaMinima[0,i])**2+(GrenzParaMinima[1,i+1]-GrenzParaMinima[1,i])**2)*Off)
            Out1[0,i]= GrenzParaMinima[0,i]- ((GrenzParaMinima[1,i+1]-GrenzParaMinima[1,i]) /
                                             sqrt((GrenzParaMinima[0,i+1]-GrenzParaMinima[0,i])**2+(GrenzParaMinima[1,i+1]-GrenzParaMinima[1,i])**2)*Off)
            Out1[1,i]= GrenzParaMinima[1,i]+ ((GrenzParaMinima[0,i+1]-GrenzParaMinima[0,i]) / 
                                             sqrt((GrenzParaMinima[0,i+1]-GrenzParaMinima[0,i])**2+(GrenzParaMinima[1,i+1]-GrenzParaMinima[1,i])**2)*Off)
        Out [0,-1] = GrenzParaMinima[0,-1]-Off ;    Out[1,-1] = 0.   
        Out1[0,-1] = GrenzParaMinima[0,-1]+Off ;    Out1[1,-1] = 0. 
        
        j=0
        for i in range(0,Teilung-2-1):
            while j < Teilung-2-3:
                if Out1[0,j] <= GrenzParaMinima[0,i]:
                    j = j+1
                    pass
                else:
                    Out2[1,i]= Out1[1,j-1] + (GrenzParaMinima[0,i]-Out1[0,j-1])*((Out1[1,j]-Out1[1,j-1])/(Out1[0,j]-Out1[0,j-1]))
                    Out2[0,i]= GrenzParaMinima[0,i]
                    break
        Out2[0,-1] = GrenzParaMinima[0,-1]
        Out2[1,-1] = 0.
        
        j=Teilung-2-4
        for i in range(Teilung-2-1,0,-1):
            while j > 0:
                if Out1[0,j] >= GrenzParaMinima[0,i]:
                    j = j-1
                    pass
                else:
                    Out3[1,i]= Out1[1,j] + (GrenzParaMinima[0,i]-Out1[0,j])*((Out1[1,j]-Out1[1,j+1])/(Out1[0,j]-Out1[0,j+1]))
                    Out3[0,i]= GrenzParaMinima[0,i]
                    break    
               
        j = 0
        for i in range(0,Teilung-2-1):
            if GrenzParaMinima[0,i] <= Out[0,j] or GrenzParaMinima[0,i] >= Out[0,-1] :
                Out5[0,i] = GrenzParaM[0,i]
                Out5[1,i] = 0.
            else:
                while j < len(Out[0])-1:
                    if GrenzParaMinima[0,i] <= Out[0,j+1] and Out[0,j] < Out[0,j+1] :
                        Out5[0,i] = GrenzParaM[0,i]
                        Out5[1,i] = Out[1,j]+ (GrenzParaMinima[0,i]-Out[0,j])*((Out[1,j+1]-Out[1,j])/(Out[0,j+1]-Out[0,j]))
                        break
                    else:
                        j=j+1    
                
        j = len(Out[0])-2
        for i in range(Teilung-2-1,0,-1):
            if GrenzParaMinima[0,i] >= Out[0,-1] or GrenzParaMinima[0,i] <= Out[0,0] :
                Out6[0,i] = GrenzParaM[0,i]
                Out6[1,i] = 0.
            else:
                while j > 0:
                    if GrenzParaMinima[0,i] >= Out[0,j-1] and Out[0,j-1] < Out[0,j] :
                        Out6[0,i] = GrenzParaM[0,i]
                        Out6[1,i] = Out[1,j]+ (GrenzParaMinima[0,i]-Out[0,j])*((Out[1,j-1]-Out[1,j])/(Out[0,j-1]-Out[0,j]))
                        break
                    else:
                        j=j-1
        for i in range(0,len(Out3[0])-1):
            Out4[0,i] = GrenzParaM[0,i]
            Out4[1,i] = max(Out3[1,i],Out2[1,i])
        Out4[0,-1] = GrenzParaMinima[0,-1]
        Out4[1,-1] = 0.      
        
        for i in range(0,Teilung-2-1):
            Out7[0,i] = GrenzParaM[0,i]
            Out7[1,i] = min(Out6[1,i],Out5[1,i])
        Out7[0,-1] = GrenzParaMinima[0,-1]
        Out7[1,-1] = 0.
        
   #*** End Offset
        return Out4, Out7

    def Percentage(ProzentMaxVel):
        ## Prozentsatz anwenden
        ProzentGrenzParaMinima  =np.zeros((2,Teilung-2-1-1),dtype = np.double)
        for i in range(0,Teilung-2-1-1):
            ProzentGrenzParaMinima[0,i] = GrenzParaMinima[0,i]
            ProzentGrenzParaMinima[1,i] =  GrenzParaMinima[1,i] # *ProzentMaxVel       
        return ProzentGrenzParaMinima

    
    
    usrVel, usrAcc, RParameter, Density, Off, YellowPoint, GreenPoint, CyanPoint, MagentaPoint =\
        InitVars(ProzentMaxVel, ProzentMaxAcc, maxAcc, maxVel, Points)
    
    ParamIn, SumLengthU, PathLength =\
        PathLength(RParameter, tckp)
    
    tckP1,Teilung, Density, Param =\
        Reparametrize(SumLengthU, ParamIn, Density, PathLength)
    
    YellowPosData, GreenPosData, CyanPosData, MagentaPosData = \
        RopeLength(Param, tckp, Teilung, Density, YellowPoint, GreenPoint, CyanPoint, MagentaPoint)
    
    YellowVelData, GreenVelData, CyanVelData, MagentaVelData, VelGrenzData, usrVelGrenzData = \
        DerivatePosFirst(Teilung, PathLength, YellowPosData, Density, GreenPosData, CyanPosData, MagentaPosData, maxVel, usrVel)
    
    AccGrenzData =\
        DerivatePosSecond(Teilung, PathLength, YellowVelData, GreenVelData, CyanVelData, MagentaVelData, maxAcc)
    
    GrenzData =\
        FindRawMin(Teilung, AccGrenzData, VelGrenzData, usrVelGrenzData)
    
    GrenzPara =\
        InsertRoots(Teilung, GrenzData, maxAcc)

    AccGrenzPara =\
        AccGrenzPara(Teilung, GrenzPara)
    
    GrenzParaM, GrenzParaMinima =\
        PeakKiller(Teilung, GrenzPara)    
    
    usrVelLimit, CPointsA =\
        usrAccLimitLines(Teilung, GrenzParaMinima, usrAcc)
    
    CPoints, AccGrenzParaMinima =\
        FindCPoints(Teilung, GrenzParaMinima, CPointsA)
    
    Out4, Out7 =\
        Offset(Teilung, GrenzParaMinima, Off, GrenzParaM)
    
    ProzentGrenzParaMinima =\
        Percentage(ProzentMaxVel)
    
    VelTimeAvePara, AccData, SumAveTime, MeanVel, TotalPathAccTime = \
        ChangeToTimeDomain(PathLength, usrVelLimit)

    if debug == 1:
        Plot(SwitchSchiebe, Schiebe, maxVel, maxAcc, usrVelLimit, TotalPathAccTime, VelTimeAvePara)
        #GrenzParaMinima = usrVelLimit
    return (tckP1,SumLengthU,ProzentGrenzParaMinima,GrenzParaMinima,
            PathLength, TotalPathAccTime, SumAveTime, MeanVel,
            AccGrenzData , AccGrenzPara, VelTimeAvePara, AccData,CPoints)

def ParaUp(Px,Py,a,i,Intervall):        
    x=Px;  y=Py
    if abs(y) < 0.01:
        c= 2*a; b = x
    else:
        c = 2*a ; b = x- y**2/(2*a)
    return (abs((i-(b*(Intervall)))*c/Intervall))**0.5
    
def ParaDown(Px,Py,a,i,Intervall):         
    x=Px ;  y=Py;
    if abs(y) < 0.01 :
        c = -2*a; b = x
    else:
        c = -2*a ; b = x-y**2/(2*-a)
    return (abs(((b*(Intervall)-i))*c/Intervall))**0.5

def EvaluateSplineY(x1,y1,x11,y11,x2,y2,x12,y12,p):                           
    k1 = (y11-y1)/(x11-x1)
    k2 = (y12-y2)/(x12-x2)
    t1 = -((-k2*x1 + k2*x2 + y1 - y2)/(k1 - k2))
    t2 = -(x1 - x2 - (-k2*x1 + k2*x2 + y1 - y2)/(k1 - k2))
    y = (2*p**3-3*p**2+1)*y1+(p**3-2*p**2+p)*(t1*k1)+(-2*p**3+3*p**2)*y2+(p**3-p**2)*(t2*k2)
    return y

    