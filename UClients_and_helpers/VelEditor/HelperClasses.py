from GrenzVel import GrenzVel
from scipy.interpolate import splprep, splev, interp1d, BPoly
import numpy as np
from math import sqrt, copysign
#from pandac.panda3dCoreModules import TransformState
#from pandac.panda3dCoreModules import LVector3f
#import mathutils
#from mathutils import Vector as LVector3f

class Pfad():
    def __init__(self,OrigPoints,RefPoints,ProfileLimits):
        self.OrigPoints    = OrigPoints
        self.RefPoints     = RefPoints
        self.ProfileLimits = ProfileLimits
        
        self.RParameter = 100000
        
        self.Description   = 'Description'
        self.Comment       = 'Comment'
        self.Visibility    = 'X'
        self.StartPoint    = LVector3f(0.0,0.0,0.0)
        self.MidPoint      = LVector3f(0.0,0.0,0.0)
        self.EndPoint      = LVector3f(0.0,0.0,0.0)
        self.Length        = 0.0
        self.tckp          = []
        self.u             = []
        self.Transposition = (0.0,0.0,0.0)
        self.Rotation      = (0.0,0.0,0.0)
        self.Bogen2Param   = []
        
        self.ProfileDics   = {}

        self.Initialize()
        
    def Initialize(self):
        # Get Spline through OrigPoints
        s=0.5;k=3; nest=-1     
        self.tckp,self.u = splprep(self.OrigPoints,s=s,k=k,nest=-1)
        A = splev(0,self.tckp)
        M = splev(0.5,self.tckp)
        E = splev(1,self.tckp)
        self.StartPoint    = LVector3f(A[0],A[1],A[2])
        self.MidPoint      = LVector3f(M[0],M[1],M[2])
        self.EndPoint      = LVector3f(E[0],E[1],E[2])
        # Calculate PathLength
        Parameter = np.linspace(0,1,self.RParameter)
        # Punkt entlang des Pfades als f von Parameter
        PvPX,PvPY,PvPZ = splev(Parameter,self.tckp)
        # Distanzen der Punkte ueber Pfad summiert
        SumLength = np.zeros(self.RParameter)
        for i in range(1,self.RParameter):
            SumLength[i]= SumLength[i-1]+ sqrt((PvPX[i]-PvPX[i-1])**2+
                                               (PvPY[i]-PvPY[i-1])**2+
                                               (PvPZ[i]-PvPZ[i-1])**2)
        self.Bogen2Param = SumLength
        self.Length      = SumLength[-1]
        
        Profile             = Profil(self.ProfileLimits,self.tckp,self.RefPoints)
        self.ProfileDics[0] = Profile

        
    def GetKeyPathDic(self,indexProfile):        
        TState = TransformState.makePosHpr(self.Transposition, self.Rotation)
        TState = 'TState'
        StartPoint = LVector3f(self.StartPoint[0],self.StartPoint[1],self.StartPoint[2])
        Endpoint   = LVector3f(self.Endpoint[0],self.Endpoint[1],self.Endpoint[2])
        return self.Description,\
               self.Visibility,\
               StartPoint,\
               Endpoint,\
               self.Length,\
               [self.tckp,self.u]\
               ,TState, \
               self.ProfileDics[indexProfile].Description,\
               self.ProfileDics[indexProfile].GrenzParaMinima,\
               self.ProfileDics[indexProfile].AccData, \
               self.ProfileDics[indexProfile].Duration,\
               self.ProfileDics[indexProfile].Prozent,\
               self.Bogen2Param

    def ____ReadKeyPointDic(self,KeyPathDic,MaxAcc,aAcc,MaxVel,AktuelleVel,
                             AccGrenzParaMinima,VelTimeAccPara,
                             YellowX,YellowY,YellowZ,
                             GreenX,GreenY,GreenZ,
                             CyanX,CyanY,CyanZ,
                             MagentaX,MagentaY,MagentaZ,
                             indexSelectedPath):
    
        self.Description =  KeyPathDic[indexSelectedPath][0]
        self.Visibility  =  KeyPathDic[indexSelectedPath][1]
        self.StartPoint  =  (KeyPathDic[indexSelectedPath][2][0],KeyPathDic[indexSelectedPath][2][1],KeyPathDic[indexSelectedPath][2][2])
        self.EndPoint    =  (KeyPathDic[indexSelectedPath][3][0],KeyPathDic[indexSelectedPath][3][1],KeyPathDic[indexSelectedPath][3][2])
        self.Length      =  KeyPathDic[indexSelectedPath][4]
        self.tck,self.u  =  KeyPathDic[indexSelectedPath][5]
        if KeyPathDic[indexSelectedPath][6].isIdentity() :
            TransX = 0.00; TransY = 0.00; TransZ = 0.00
            RotX = 0.00  ; RotY    = 0.00;RotZ   = 0.00
        if KeyPathDic[indexSelectedPath][6].hasPos():
            Pos = KeyPathDic[indexSelectedPath][6].getPos()
            TransX = Pos[0]; TransY = Pos[1]; TransZ = Pos[2]
            RotX = 0.00;     RotY   = 0.00;   RotZ    = 0.00                
        else:
            TransX = 0.00; TransY = 0.00;  TransZ = 0.00
            RotX = 0.00;   RotY    = 0.00; RotZ   = 0.00                
        if KeyPathDic[indexSelectedPath][6].hasHpr():
            Rot = KeyPathDic[indexSelectedPath][6].getHpr()
            RotX = Rot[1]; RotY   = Rot[2];  RotZ   = Rot[0]
            TransX = 0.00; TransY = 0.00;    TransZ = 0.00                
        else:
            RotX   = 0.00; RotY   = 0.00; RotZ   = 0.00
            TransX = 0.00; TransY = 0.00; TransZ = 0.00                
        self.Transposition = (TransX,TransY,TransZ)
        self.Rotation      = (RotX,RotY,RotZ)
        ReferencePoints = ((YellowX,YellowY,YellowZ),
                           (GreenX,GreenY,GreenZ),
                           (CyanX,CyanY,CyanZ),
                           (MagentaX,MagentaY,MagentaZ)) 
        self.PathComment = 'Path Comment for Key %3i \n Bla Bla'%(indexSelectedPath) 
        
        profile = Profil()
        profile.SetProfile(KeyPathDic[indexSelectedPath][7],MaxAcc,aAcc,MaxVel,
                   AktuelleVel,AccGrenzParaMinima,VelTimeAccPara)
        try:
            profileKey= max(self.ProfileDics.keys())+1
        except ValueError:
            profileKey = 0
        self.ProfileDics[profileKey]  = profile
            
class Profil():
    def __init__(self,ProfileLimits,tckp,RefPoints):
        self.__tckp             = tckp
        self.__RefPoints        = RefPoints
        self.Description        = 'Description'
        self.Comment            = 'Comment'
        self.ProfileLimits      = ProfileLimits
        self.GrenzParaMinima    = []
        self.VelTimeAccPara     = []
        self.Duration           = 0.0
        self.Prozent            = 0.8
        self.Flag               = 'raw'
        self.SCTPoints          = []
        self.SBPolyVelPData     = []
        self.SBPolyVelTData     = []
        
        self.InitializePhaseI(self.__RefPoints,self.__tckp,self.ProfileLimits)

    def InitializePhaseI(self,RefPoints,tckp,ProfileLimits):
        
        MaxAcc        = ProfileLimits[0]
        UsrAcc        = ProfileLimits[1]
        MaxVel        = ProfileLimits[2]
        UsrVel        = ProfileLimits[3] 
        if UsrAcc <= 0 :
            UsrAcc = MaxAcc*0.1
        if UsrVel <= 0 :
            UsrVel = MaxVel*0.1
        ProzentMaxVel = MaxAcc/UsrAcc
        ProzentMaxAcc = MaxVel/UsrVel 
        ProzentMaxVel = max(min(ProzentMaxVel,1.0),0.1)
        ProzentMaxAcc = max(min(ProzentMaxAcc,1.0),0.1) 
        ProzentMaxVel = 0.8
        Debug         = 0
        SmoothingF    = 200
        SmoothingOn   = 1


        (A, Bogen2Param, ProzentGrenzParaMinima, self.GrenzParaMinima,
                        PathLengthGrenzVel,self.Duration,SumAveTime,
                        meanVel, AccGrenzData, AccGrenzPara,VelTimeAvePara,
                        self.AccData, self.CPoints) = GrenzVel(tckp,RefPoints,MaxVel,ProzentMaxVel,MaxAcc,
                                                          ProzentMaxAcc,SmoothingOn,SmoothingF,Debug)
        
        self.PrepToTimeDomain()
        self.Flag  = 'primed'
    
    def PrepToTimeDomain(self):
        # ------Beginn Get Position over Time Line
        self.PTData = np.zeros((2,len(self.GrenzParaMinima[0])),dtype = np.double)
        ST = 0.0
        for i in range(1,len(self.GrenzParaMinima[0])):
            T = abs(self.GrenzParaMinima[0,i-1]-self.GrenzParaMinima[0,i])/((self.GrenzParaMinima[1,i-1]+(self.GrenzParaMinima[1,i]))/2)
            ST = ST+T
            self.PTData[0,i]= self.GrenzParaMinima[0,i]
            self.PTData[1,i]= ST
        # ------End Get Position over Time Line
        # ------Beginn Get Vel over Time Line Interpolation
        self.VelTData = np.zeros((2,len(self.GrenzParaMinima[0])),dtype = np.double)
        self.VelPosToVelTime = interp1d(self.PTData[0], self.PTData[1], fill_value=np.nan, assume_sorted=True)
        self.VelTData[0] = self.VelPosToVelTime(self.GrenzParaMinima[0])
        self.VelTData[1] = self.GrenzParaMinima[1]
        # ------End Get Vel over Time Line Interpolation
        # ------Beginn Get Acc over Time Line
        self.AccTData = np.zeros((2,len(self.GrenzParaMinima[0])),dtype = np.double)
        for i in range(1,len(self.GrenzParaMinima[0])):
            Acc = (self.VelTData[1,i]-self.VelTData[1,i-1])/(self.VelTData[0,i]-self.VelTData[0,i-1])
            self.AccTData[0,i]= self.VelTData[0,i]
            self.AccTData[1,i]= Acc
        self.AccTData[0,-1]= self.VelTData[0,-1]
        self.AccTData[1,-1]= 0.0
        # ------End Get Acc over Time Line
        # ------Beginn AccData als differenzen
        self.DeltaAccTData = np.zeros((2,len(self.AccTData[0])),dtype = np.double)
        for i in range(0,len(self.AccTData[0])-1):
            self.DeltaAccTData[0,i]= self.AccTData[0,i+1]-self.AccTData[0,i]
            self.DeltaAccTData[1,i]= self.AccTData[1,i+1]-self.AccTData[1,i]
        #------End AccData als differenzen
        # ------Beginn ramp Difference
        maxJerk = 20.
        for i in range(0,len(self.AccTData[0])-1):
            if (abs(self.AccTData[1,i+1]-self.AccTData[1,i])/(self.AccTData[0,i+1]-self.AccTData[0,i]) > maxJerk):
                self.DeltaAccTData[0,i]= abs(self.AccTData[1,i+1]-self.AccTData[1,i])/maxJerk
        # ------Beginn Summation
        self.SumAccTData = np.zeros((2,len(self.DeltaAccTData[0])),dtype = np.double)
        for i in range(0,len(self.DeltaAccTData[0])):
            self.SumAccTData[0,i]= self.SumAccTData[0,i-1]+self.DeltaAccTData[0][i]
            self.SumAccTData[1,i]= self.SumAccTData[1,i-1]+self.DeltaAccTData[1][i]
        self.SumAccTData[0,0] = 0.
        self.SumAccTData[1,0] = 0.
        self.SumAccTData[1,-1] = 0.
        # ------End Summation
        # ------Beginn Rebase Time        
        GV = interp1d(self.SumAccTData[0], self.SumAccTData[1], kind='linear', axis=-1, copy=True, bounds_error=None, fill_value=np.nan, assume_sorted=True)
        NT = np.linspace(0,self.SumAccTData[0,-1], num=10000, endpoint=True, retstep=False, dtype=np.double)        
        AccScale = self.AccTData[0,-1]/self.SumAccTData[0,-1]
        NGV = GV(NT)
        self.RampedAccTData = np.stack((NT,NGV))
        self.RampedAccTData[0] = self.RampedAccTData[0]*AccScale        
        # ------End Rebase Time
        # ------Beginn Scaling to get Vend = 0
        # ------Beginn  Integrate Positive RBRampedAccTData over Time to get Vel over Time
        SP = 0.0
        self.PosRampedVelTData = np.zeros((1,len(self.RampedAccTData[0])),dtype = np.double)
        for i in range(1,len(self.RampedAccTData[0])-1):
            if self.RampedAccTData[1,i] > 0:
                P = ((-0.5*(self.RampedAccTData[1,i-1]+self.RampedAccTData[1,i+1]))*(self.RampedAccTData[0,i-1]-self.RampedAccTData[0,i]))
                SP = SP + P
                self.PosRampedVelTData[0,i]=SP
            self.PosRampedVelTData[0,-1]=SP
        # ------End  Integrate Positive RBRampedAccTData over Time to get Vel over Time
        # ------Beginn  Integrate Negative RBRampedAccTData over Time to get Vel over Time
        SP = 0.0
        self.NegRampedVelTData = np.zeros((1,len(self.RampedAccTData[0])),dtype = np.double)
        for i in range(1,len(self.RampedAccTData[0])-1):
            if self.RampedAccTData[1,i] < 0:
                P = ((-0.5*(self.RampedAccTData[1,i-1]+self.RampedAccTData[1,i+1]))*(self.RampedAccTData[0,i-1]-self.RampedAccTData[0,i]))
                SP = SP + P
                self.NegRampedVelTData[0,i]=SP
            self.NegRampedVelTData[0,-1]=SP
        # ------End  Integrate Positive RBRampedAccTData over Time to get Vel over Time
        AccScale1 = abs(self.NegRampedVelTData[0,-1]/self.PosRampedVelTData[0,-1])
        self.BalancedAccTData = np.zeros((2,len(self.RampedAccTData[0])),dtype = np.double)
        for i in range(0,len(self.RampedAccTData[0])):
            if self.RampedAccTData[1,i] > 0:
                self.BalancedAccTData[1,i] = self.RampedAccTData[1,i]*AccScale1
            else:
                self.BalancedAccTData[1,i] = self.RampedAccTData[1,i]*1.0
            self.BalancedAccTData[0,i] = self.RampedAccTData[0,i]
        # ------End Scaling to get Vend = 0 
        # ------Beginn  Integrate BalancedAccTData over Time to get Vel over Time
        SP = 0.0
        self.BalancedVelTData = np.zeros((2,len(self.BalancedAccTData[0])),dtype = np.double)
        for i in range(1,len(self.BalancedAccTData[0])-1):
            P = ((-0.5*(self.BalancedAccTData[1,i-1]+self.BalancedAccTData[1,i+1]))*(self.BalancedAccTData[0,i-1]-self.BalancedAccTData[0,i]))
            SP = SP + P
            self.BalancedVelTData[0,i]=self.BalancedAccTData[0,i]
            self.BalancedVelTData[1,i]=SP
        self.BalancedVelTData[0,-1]=self.BalancedAccTData[0,-1]
        self.BalancedVelTData[1,-1]=SP
        # ------End  BalancedAccTData over Time to get Vel over Time
        # ------Beginn Scale BalancedAccTData over Time to meet maxVel Kriterium
        mv = np.amax(self.BalancedVelTData[1])
        AccScale2 = self.ProfileLimits[3]/mv
        self.BalancedAccTData[1]=self.BalancedAccTData[1]*AccScale2
        for i in range(1,len(self.BalancedAccTData[0])-1):
            P = ((-0.5*(self.BalancedAccTData[1,i-1]+self.BalancedAccTData[1,i+1]))*(self.BalancedAccTData[0,i-1]-self.BalancedAccTData[0,i]))
            SP = SP + P
            self.BalancedVelTData[0,i]=self.BalancedAccTData[0,i]
            self.BalancedVelTData[1,i]=SP
        self.BalancedVelTData[0,-1]=self.BalancedAccTData[0,-1]
        self.BalancedVelTData[1,-1]=SP
        # ------End  BalancedAccTData over Time to get Vel over Time 
        # ------End Scale BalancedAccTData over Time to meet maxVel Kriterium
        # ------Beginn  Integrate BalancedVelTData over Time to get Pos over Time
        SP = 0.0
        self.BalancedPosTData = np.zeros((2,len(self.BalancedVelTData[0])),dtype = np.double)
        for i in range(1,len(self.BalancedVelTData[0])-1):
            P = ((-0.5*(self.BalancedVelTData[1,i-1]+self.BalancedVelTData[1,i+1]))*(self.BalancedVelTData[0,i-1]-self.BalancedVelTData[0,i]))
            SP = SP + P
            self.BalancedPosTData[0,i]=self.BalancedVelTData[0,i]
            self.BalancedPosTData[1,i]=SP
        self.BalancedPosTData[0,-1]=self.BalancedVelTData[0,-1]
        self.BalancedPosTData[1,-1]=SP
        #print 'Laenge des Pfades nach Ramp and Balance %3.4f'%(self.BalancedPosTData[1,-1])
        # ------End  Integrate BalancedVelTData over Time to get Pos over Time
        # ------Beginn  Scaled Integration of BalancedVelTData over Time to get Pos over Time while traveling the whole Path
        self.PosSkalierung = self.GrenzParaMinima[0,-1]/self.BalancedPosTData[1,-1]
        SP = 0.0
        self.SBalancedPosTData = np.zeros((2,len(self.BalancedVelTData[0])),dtype = np.double)
        for i in range(1,len(self.BalancedVelTData[0])-1):
            P = ((-0.5*(self.BalancedVelTData[1,i-1]+self.BalancedVelTData[1,i+1]))*(self.BalancedVelTData[0,i-1]-self.BalancedVelTData[0,i])*self.PosSkalierung)
            SP = SP + P
            self.SBalancedPosTData[0,i]=self.BalancedVelTData[0,i]*self.PosSkalierung
            self.SBalancedPosTData[1,i]=SP
        self.SBalancedPosTData[0,-1]=self.BalancedVelTData[0,-1]*self.PosSkalierung
        self.SBalancedPosTData[1,-1]=self.GrenzParaMinima[0,-1]
        #print 'Skalierte Laenge des Pfades nach Ramp and Balance %3.4f'%(self.SBalancedPosTData[1,-1])
        # ------End  Scaled Integration of BalancedVelTData over Time to get Pos over Time while traveling the whole Path
        # ------Beginn Scaled Vel and Acc
        self.SBalancedVelTData = np.zeros((2,len(self.BalancedVelTData[0])),dtype = np.double)
        self.SBalancedVelTData[0] = self.SBalancedPosTData[0]
        self.SBalancedVelTData[1] = self.BalancedVelTData[1]
        
        self.SBalancedAccTData = np.zeros((2,len(self.BalancedVelTData[0])),dtype = np.double)
        self.SBalancedAccTData[0] = self.SBalancedPosTData[0]
        self.SBalancedAccTData[1] = self.BalancedAccTData[1]
        # ------End Scaled Vel and Acc
        # ------Begin find Extrema of SBalancedVelTData
        CTPointsSBalancedVelX=[0.0]
        CTPointsSBalancedVelY=[0.0]
        for i in range(1,len(self.SBalancedAccTData[0])):
            if ((copysign(1, self.SBalancedAccTData[1,i-1]) != copysign(1,self.SBalancedAccTData[1,i])) or
                self.SBalancedAccTData[1,i] == 0 and self.SBalancedAccTData[1,i-1] != 0):
                CTPointsSBalancedVelX.append(self.SBalancedAccTData[0,i])
                CTPointsSBalancedVelY.append(self.SBalancedVelTData[1,i])
        CTPointsNX     = np.array(CTPointsSBalancedVelX)
        CTPointsNY     = np.array(CTPointsSBalancedVelY)
        self.CTPointsSBalancedVelT = np.stack((CTPointsNX,CTPointsNY))
        self.CTPointsSBalancedVelT[1,-1]= 0.0
        # ------End find Extrema of SVelTCVData
        # ------Begin find BPoly through SVelTCVData extrema
        #construct yi : array_like or list of array_likes yi[i][j] is the j-th derivative known at xi[i]        
        order = 3
        yi = [[0,0]]
        for i in range (1,len(self.CTPointsSBalancedVelT[1])):
            yi.append([self.CTPointsSBalancedVelT[1,i],0])
        yi[-1]=[0,0]         
        self.BPolyFunct =BPoly.from_derivatives(self.CTPointsSBalancedVelT[0],yi,orders = order)
        self.BPolyVelTData    = np.zeros((2,len(self.BalancedVelTData[0])),dtype = np.double)
        self.BPolyVelTData[0] = self.SBalancedVelTData[0]
        self.BPolyVelTData[1] = self.BPolyFunct(self.SBalancedVelTData[0])
        # ------End find BPoly through SVelTCVData extrema
        # ------Beginn Get SAccTCV over Time Line noch nicht skaliert
        self.BPolyAccTData = np.zeros((2,len(self.BPolyVelTData[0])),dtype = np.double)
        for i in range(1,len(self.BPolyVelTData[0])):
            Acc = (self.BPolyVelTData[1,i]-self.BPolyVelTData[1,i-1])/(self.BPolyVelTData[0,i]-self.BPolyVelTData[0,i-1])
            self.BPolyAccTData[0,i]= self.BPolyVelTData[0,i]
            self.BPolyAccTData[1,i]= Acc
        self.BPolyAccTData[0,-1]= self.BPolyVelTData[0,-1]
        self.BPolyAccTData[1,-1]= 0.0
        # ------End Get SAccTCV over Time Line  noch nicht skaliert
        # ------Beginn  Integrate SVelTCVData over Time to get Pos over Time
        SP = 0.0
        self.BPolyPosTData = np.zeros((2,len(self.BPolyVelTData[0])),dtype = np.double)
        for i in range(1,len(self.BPolyVelTData[0])-1):
            P = ((-0.5*(self.BPolyVelTData[1,i-1]+self.BPolyVelTData[1,i+1]))*(self.BPolyVelTData[0,i-1]-self.BPolyVelTData[0,i]))
            SP = SP + P
            self.BPolyPosTData[0,i]=self.BPolyVelTData[0,i]
            self.BPolyPosTData[1,i]=SP
        self.BPolyPosTData[0,-1]=self.BPolyVelTData[0,-1]
        self.BPolyPosTData[1,-1]=SP
        #print 'Laenge des Pfades nach BPoly %3.4f'%(self.BPolyPosTData[1,-1])
        # ------End  Integrate VelTRamped over Time to get Pos over Time
        # ------Beginn  Scaled Integration of SBPVelTData over Time to get Pos over Time while traveling the whole Path
        self.PosSkalierung1 = self.GrenzParaMinima[0,-1]/self.BPolyPosTData[1,-1]
        SP = 0.0
        self.SBPolyPosTData = np.zeros((2,len(self.BPolyVelTData[0])),dtype = np.double)
        for i in range(1,len(self.BPolyVelTData[0])-1):
            P = ((-0.5*(self.BPolyVelTData[1,i-1]+self.BPolyVelTData[1,i+1]))*(self.BPolyVelTData[0,i-1]-self.BPolyVelTData[0,i])*self.PosSkalierung1)
            SP = SP + P
            self.SBPolyPosTData[0,i]=self.BPolyVelTData[0,i]*self.PosSkalierung1
            self.SBPolyPosTData[1,i]=SP
        self.SBPolyPosTData[0,-1]=self.BPolyVelTData[0,-1]*self.PosSkalierung1
        self.SBPolyPosTData[1,-1]=self.GrenzParaMinima[0,-1]
        #print 'Skalierte Laenge des Pfades nach Editing %3.4f'%(self.SBPolyPosTData[1,-1])
        # ------End  Scaled Integration of SBPVelTData over Time to get Pos over Time while traveling the whole Path
        # ------Beginn 2nd Scaled Vel and Acc
        self.SBPolyVelTData = np.zeros((2,len(self.BalancedVelTData[0])),dtype = np.double)
        self.SBPolyVelTData[0] = self.SBPolyPosTData[0]
        self.SBPolyVelTData[1] = self.BPolyVelTData[1]
        
        self.SBPolyAccTData = np.zeros((2,len(self.BalancedVelTData[0])),dtype = np.double)
        self.SBPolyAccTData[0] = self.SBPolyPosTData[0]
        self.SBPolyAccTData[1] = self.BPolyAccTData[1] 
        
        self.SCTPointsT = np.zeros((2,len(self.CTPointsSBalancedVelT[0])),dtype = np.double)
        for i in range(len(self.CTPointsSBalancedVelT[0])):
            self.SCTPointsT[0,i] = self.CTPointsSBalancedVelT[0,i]*self.PosSkalierung1
            self.SCTPointsT[1,i] = self.CTPointsSBalancedVelT[1,i]        
        # ------End 2nd Scaled Vel and Acc
        
        # ------Beginn Get SBPolyVelTData in Pos Domain
        self.SBPolyVelPData = np.zeros((2,len(self.BPolyVelTData[0])),dtype = np.double)
        self.VelVelToVelPos = interp1d(self.SBPolyPosTData[0], self.SBPolyPosTData[1], fill_value=np.nan, assume_sorted=True)
        self.SBPolyVelPData[0] = self.VelVelToVelPos(self.SBPolyVelTData[0])
        self.SBPolyVelPData[1] = self.BPolyVelTData[1]
        # ------End Get SBPolyVelTData in Pos Domain
        self.VelPosToVelTime = interp1d(self.SBPolyPosTData[1], self.SBPolyPosTData[0], fill_value=np.nan, assume_sorted=True)
        self.RecalcBPolySCT()
        
    def RecalcBPolySCT(self):
        order = 3
        yi = [[0,0]]
        for i in range (1,len(self.SCTPointsT[0])):
            yi.append([self.SCTPointsT[1,i],0])
        yi[-1]=[0,0]        
        self.BPolyFunct =BPoly.from_derivatives(self.SCTPointsT[0],yi,orders = order)
        pdt  =self.BPolyFunct.derivative(1)
        pint =self.BPolyFunct.antiderivative(1)
        self.SBPolyVelTData[1] = self.BPolyFunct(self.SBPolyVelTData[0])
        self.SBPolyAccTData[0] = self.SBPolyVelTData[0]
        self.SBPolyAccTData[1] = pdt(self.SBPolyVelTData[0])
        
        # ------Beginn   Integration of SBPolyVelTData over Time to get Time Scaling to travel the whole Path
        PosI= pint(self.SBPolyVelTData[0,-1])
        # ------End   Integration of SBPolyVelTData over Time to get Time Scaling to travel the whole Path  
        # ------Beginn Rescale Vel Acc CTPoints anr representation Points - TTPoints TPPoints
        self.PosSkalierung2 = self.GrenzParaMinima[0,-1]/(PosI) 
        self.SBPolyVelTData[0] = self.SBPolyVelTData[0] *self.PosSkalierung2
        self.SBPolyAccTData[0] = self.SBPolyAccTData[0] *self.PosSkalierung2
        self.SCTPointsT[0]= self.SCTPointsT[0] *self.PosSkalierung2
         # ------End Rescale Vel Acc CTPoints anr representation Points - TTPoints TPPoints
        # ------Beginn   Integration of SBPolyVelTData over Time to get Pos over Time while traveling the whole Path
        SP = 0.0
        self.SBPolyPosTData = np.zeros((2,len(self.SBPolyVelTData[0])),dtype = np.double)
        for i in range(1,len(self.SBPolyVelTData[0])-1):
            P = ((-0.5*(self.SBPolyVelTData[1,i-1]+self.SBPolyVelTData[1,i+1]))*(self.SBPolyVelTData[0,i-1]-self.SBPolyVelTData[0,i]))
            SP = SP + P
            self.SBPolyPosTData[0,i]=self.SBPolyVelTData[0,i]
            self.SBPolyPosTData[1,i]=SP
        self.SBPolyPosTData[0,-1]=self.SBPolyVelTData[0,-1]
        self.SBPolyPosTData[1,-1]=self.GrenzParaMinima[0,-1]
        # ------End   Integration of SBPVelTData over Time to get Pos over Time while traveling the whole Path        
        # ------Beginn get new Domain changing Functions
        self.VelVelToVelPos  = interp1d(self.SBPolyPosTData[0], self.SBPolyPosTData[1], fill_value=np.nan, assume_sorted=True)
        self.VelPosToVelTime = interp1d(self.SBPolyPosTData[1], self.SBPolyPosTData[0], fill_value=np.nan, assume_sorted=True)
        self.GrenzDataX = self.VelPosToVelTime(self.GrenzParaMinima[0])
        self.GrenzDataY = self.GrenzParaMinima[1]

        self.GrenzVelT       = interp1d(self.GrenzDataX,self.GrenzDataY, bounds_error=False,fill_value=[0])
        
        # ------End get new Domain changing Functions        
        self.SBPolyVelPData[0] = self.VelVelToVelPos(self.SBPolyVelTData[0])
        self.SBPolyVelPData[1] = self.SBPolyVelTData[1]        
        