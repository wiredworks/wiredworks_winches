#!/usr/bin/python
# -*- coding: <<encoding>> -*-

import wx
from wx import xrc

import socket
import time
import select
import sys
import math

from threading import Thread
from pubsub import pub
print('pubsub API version', pub.VERSION_API)

import sys
print(sys.executable)

XRC_ENGINES             = "simple_AxisSimulation.xrc"

UDP_IP = "127.0.0.1"
UDP_SENDPORT = 15023
UDP_RECPORT  = 15024


class SyncSend(Thread):
    def __init__(self):
        
        Thread.__init__(self)
        
        self.initVars()
        
        self.ssock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP 

        self.setDaemon(True)
        self.start()

    def initVars(self):        
        self.oldtime = time.time_ns()
        self.st = time.time_ns()
        self.rt = self.st
        self.dt = self.rt-self.st
        self.i = 0
        self.data = b" "
        self.lsT = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,
                    0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,
                    0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,
                    0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,
                    0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,
                    0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,
                    0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,
                    0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,
                    0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,
                    0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
        self.lsB = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,
                    0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,
                    0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,
                    0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,
                    0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,
                    0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,
                    0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,
                    0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,
                    0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,
                    0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
        self.lsN = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,
                    0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,
                    0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,
                    0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,
                    0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,
                    0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,
                    0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,
                    0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,
                    0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,
                    0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]        
        self.sumT = 0.0
        self.avgT = 0.0
        
        self.TickTime  = 0.0
        self.MaxPos    = 10.0
        self.MinPos    = 0.0
        self.MaxVel    = 10.0
        self.MaxAcc    = 1.0
        self.IstVel    = 0.0
        self.IstPos    = 0.0
        self.IstForce  = 0.0
        self.SpeedIstUI = 0.0
        self.SollVel    = 0.0
        self.SollPos    = 0.0
        self.SollForce  = 0.0
        self.confirm   = 'False'
        self.confirmed = 'False'
        self.Online    = 'False'
        self.Selected  = 'False'
        self.Status    = 'False'
        self.Reset     = 'False'
        self.Status    = 'WasWeiWie'
        self.Enabled   = 'False'
        self.OldTime_ns = time.time_ns()
        self.IntervallR  = 0.0
        self.message = {'IP'        :  UDP_IP,
                   'SendPort'  :  UDP_SENDPORT,
                   'RecPort'   :  UDP_RECPORT,                   
                   'IstPos'    :  self.IstPos,
                   'IstVel'    :  self.IstVel,
                   'IstForce'  :  self.IstForce,
                   'SollVel'   :  self.SollVel,
                   'Status'    :  self.Status,
                   'TickTime'  :  self.TickTime,
                   'MaxPos'    :  self.MaxPos,
                   'MinPos'    :  self.MinPos,
                   'MaxVel'    :  self.MaxVel,
                   'MaxAcc'    :  self.MaxAcc,
                   'Confirmed' :  self.confirmed,
                   'Selected'  :  self.Selected,
                   'Online'    :  self.Online
                   }
        

    def send(self):
        self.st =time.time_ns()        
        Message = self.packSendStringToBlender().encode('utf-8')    
        self.ssock.sendto(Message, (UDP_IP, UDP_SENDPORT))
        
    def rec(self):
        rsock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP 
        rsock.bind((UDP_IP,UDP_RECPORT))
        rsock.settimeout(0.1)
        data = "NO DATA"
        self.Online = 'False'
        try:
            data,addr = rsock.recvfrom(512)
        except:
            self.message['Confirmed'] = 'False'
            self.confirmed = 'False'
            wx.CallAfter(pub.sendMessage,'update',message=self.message)
        if data != "NO DATA":
            self.unpackRecStringfromBlender(data.decode('utf-8'))
            self.Online = 'True'
            self.rt = time.time_ns()
        rsock.close()
        
    def unpackRecStringfromBlender(self,Data):
        #print('IN         *'+Data)
        Data = Data.split(';')
        fo ="%3.4f"
        self.TickTime   = Data[0]                #
        self.SetMaxPos  = fo%(float(Data[1]))    #
        self.SetMinPos  = fo%(float(Data[2]))    #
        self.SetMaxVel  = fo%(float(Data[3]))    #
        self.SetMaxAcc  = fo%(float(Data[4]))    #
        self.SollVel    = fo%(float(Data[5]))    #
        self.SollPos    = Data[6]
        self.SollForce  = Data[7]
        self.confirm    = Data[8]    
        self.confirmed  = Data[9]                #
        self.Enabled    = Data[10]               #
        self.Selected   = Data[11]               #
        self.Status     = Data[13]               #
        self.Reset      = Data[14]
        if self.confirm == 'True':
            self.MaxPos = self.SetMaxPos
            self.MinPos = self.SetMinPos
            self.MaxVel = self.SetMaxVel
            self.MaxAcc = self.SetMaxAcc
            self.confirmed = 'True'
        else:
            self.confirmed = 'False'
        
    def packSendStringToBlender(self):
        fo ="%3.4f"
        self.SendData = str(time.time_ns())
        self.SendData = (self.SendData+';'            # 0
                    +str(self.MaxPos)+';'      # 1  
                    +str(self.MinPos)+';'      # 2
                    +str(self.MaxVel)+';'      # 3
                    +str(self.MaxAcc)+';'      # 4
                    +fo%(float(self.SpeedIstUI))+';'  # 5
                    +fo%(float(self.IstPos))+';'      # 6
                    +fo%(float(self.IstForce))+';'    # 7
                    +str(self.confirm)+';'            # 8
                    +str(self.confirmed)+';'          # 9
                    +str(self.Online)+';'             # 10
                    +str(self.Selected)+';'           # 11
                    +str(self.Status)+';'             # 12
                    +str(self.Reset))                 # 13
        #print('Out   '+self.SendData)
        return self.SendData
    
    def run(self):
        while True:            
            self.rec()
            self.CalculateVelPosForce()
            self.send()            
            self.CalculateTimes()
            message = self.packMessage()
            wx.CallAfter(pub.sendMessage,'update',message=self.message)
            
    def packMessage(self):
        fo ="%3.4f" 
        self.message['IP']        =  UDP_IP
        self.message['SendPort']  =  UDP_SENDPORT
        self.message['RecPort']   =  UDP_RECPORT                   
        self.message['IstPos']    =  fo%(float(self.IstPos))
        self.message['IstVel']    =  fo%(float(self.SpeedIstUI))
        self.message['IstForce']  =  fo%(float(self.IstForce))
        self.message['SollVel']   =  self.SollVel        
        self.message['TickTime']  =  self.IntervallR
        self.message['MaxPos']    =  self.MaxPos
        self.message['MinPos']    =  self.MinPos
        self.message['MaxVel']    =  self.MaxVel
        self.message['MaxAcc']    =  self.MaxAcc        
        self.message['Confirmed'] =  self.confirmed
        self.message['Online']    =  self.Online
        self.message['Enabeled']  =  self.Enabled        
        self.message['Selected']  =  self.Selected
        self.message['Status']    =  self.Status
        return self.message
                      
            
    def CalculateVelPosForce(self):
        self.IntervallR = (time.time_ns()-self.OldTime_ns)*10e-10
        self.Status   = "SIMUL"
        #print(self.IntervallR)
               
        if self.Selected == 'True' and self.confirmed == 'True':
            #print('Calculate Speed')
            SpeedIstIntern = self.SpeedIstUI
            SpeedSollIntern = min(float(self.SollVel),float(self.MaxVel))
            SpeedSollIntern = max(float(self.SollVel),-float(self.MaxVel))

            PosDiffG = float(self.MaxPos) - float(self.IstPos)
            if PosDiffG > 0 :
                SpeedMaxG = math.sqrt(float(self.MaxAcc)*PosDiffG)
                SpeedSollIntern = min(SpeedSollIntern,SpeedMaxG)
                #print(" Ausserer Anschlag")
            else:
                if SpeedSollIntern > 0:
                    SpeedSollIntern = 0.0
                    #print("auserhalb Ausserer Anschlag")                    
            PosDiffG = float(self.IstPos) - float(self.MinPos)
            if PosDiffG > 0:
                SpeedMaxG = math.sqrt(float(self.MaxAcc)*PosDiffG);
                SpeedSollIntern = max(SpeedSollIntern,-SpeedMaxG)
                #print(" Innerer Anschlag")
            else:
                if SpeedSollIntern < 0:
                    SpeedSollIntern= 0.0
                    #print("auserhalb innerenr Anschlag")
                    
            #print(SpeedSollIntern)                   
            if (SpeedSollIntern > 0 and SpeedSollIntern >= SpeedIstIntern):
                SpeedIstIntern = (SpeedIstIntern+float(self.MaxAcc)*self.IntervallR)
                #print("werden Schneller in Plus Richtung")
                if SpeedIstIntern > SpeedSollIntern:
                    SpeedIstIntern = SpeedSollIntern
                    #print("Soll Gesch erreicht von Unten Richtung Plus")
            elif (SpeedSollIntern >= 0 and SpeedSollIntern < SpeedIstIntern):
                SpeedIstIntern = (SpeedIstIntern-float(self.MaxAcc)*self.IntervallR)
                #print("werden langsamer in Plus Richtung")
                if SpeedIstIntern < SpeedSollIntern:
                    SpeedIstIntern = SpeedSollIntern
                    #print("Soll Gesch erreicht von Oben Richtung Plus")
            elif (SpeedSollIntern <= 0 and SpeedSollIntern < SpeedIstIntern):
                SpeedIstIntern = (SpeedIstIntern-float(self.MaxAcc)*self.IntervallR)
                #print("werden Schneller in Minus Richtung")
                if SpeedIstIntern < SpeedSollIntern :
                    SpeedIstIntern = SpeedSollIntern
                    #print("Soll Gesch erreicht von Oben Richtung Minus")
            elif (SpeedSollIntern <= 0 and SpeedSollIntern >= SpeedIstIntern):
                SpeedIstIntern = (SpeedIstIntern+float(self.MaxAcc)*self.IntervallR)
                #print("werden Langsamer in Minus Richtung")
                if SpeedIstIntern > SpeedSollIntern:
                    SpeedIstIntern = SpeedSollIntern
                    #print("Soll Gesch erreicht von Unten Richtung Minus")

        #self.PosIst
            self.IstPos = str(float(self.IstPos)+SpeedIstIntern*self.IntervallR)
            self.SpeedIstUI = SpeedIstIntern
        else:
            self.IstVel = 0.0
            
        self.OldTime_ns = time.time_ns()
        
    def CalculateTimes(self):
        A = self.SendData.split(';')
        diff_BlenderTime_SendTime=(time.time_ns()-int(self.TickTime))/1000000.0
        self.lsB.pop(0)
        self.lsB.append(diff_BlenderTime_SendTime)
        self.sumB = 0.0
        for i in range(100):
            self.sumB = self.sumB + self.lsB[i]
        self.avgB = self.sumB/100.0
        
        self.dt = (self.st -self.rt)/1000000.0
        self.lsT.pop(0)
        self.lsT.append(self.dt)
        self.sumT = 0.0
        for i in range(100):
            self.sumT = self.sumT + self.lsT[i]
        self.avgT = self.sumT/100.0
        print("Round Trip Time %7.4f ms Diff Time: %2.2f ms" %(self.avgB,self.avgT),end='\r')

class UI(wx.Panel):
    def __init__(self, parent, id, title):
        self.locale = wx.Locale(wx.LANGUAGE_ENGLISH)

        wx.Frame.__init__(self, parent, size=(645,170))
        self.res = xrc.XmlResource(XRC_ENGINES )
        self.RootPanel = self.res.LoadPanel(self,'RootPanel')
        self.init_Mainframe()
        
        pub.subscribe(self.UpdateUI,'update')
        
        
    def UpdateUI(self,message):
        fe="%1.3f"
        self.txtIP.SetValue(str(message['IP']))
        self.txtSPort.SetValue(str(message['SendPort']))
        self.txtRPort.SetValue(str(message['RecPort']))      
        self.txtAxisPos .SetValue(str(message['IstPos']))
        self.txtAxisVel.SetValue(str(message['IstVel']))
        self.txtAxisAmp.SetValue(str(message['IstForce']))
        self.txtSetVel.SetValue(str(message['SollVel']))
        self.txtAxisError.SetValue(str(message['Status']))
        #self.btnAxisReset
        self.txtTimeTick.SetValue(str(fe%float(message['TickTime'])))
        # Kinder vom ValuePanel
        self.txtMaxPos.SetValue(str(message['MaxPos']))
        self.txtMinPos.SetValue(str(message['MinPos']))
        self.txtMaxVel.SetValue(str(message['MaxVel']))
        self.txtMaxAcc.SetValue(str(message['MaxAcc']))
        #if message['Confirmed'] == 'True':
            #self.txtConfirmed.SetValue('Confirmed')
            #self.txtConfirmed.SetBackgroundColour((0,188,0))
        #else:
            #self.txtConfirmed.SetValue('UnConfirmed')
            #self.txtConfirmed.SetBackgroundColour((188,188,188))
        if message['Confirmed'] == 'True':
            self.chkConfirmed.SetValue(True)
            self.chkConfirmed.SetBackgroundColour((0,188,0))
        else:
            self.chkConfirmed.SetValue(False)
            self.chkConfirmed.SetBackgroundColour((188,188,188))        
            
            #self.rbConfirmed.SetValue(str(message['Confirmed'])
        # Kinder vom BitPanel
        if message['Online'] == 'True':
            self.txtOnline.SetValue('On-line')
            self.txtOnline.SetBackgroundColour((0,188,0))
        else:
            self.txtOnline.SetValue('Off-line')
            self.txtOnline.SetBackgroundColour((188,188,188))

        if message['Enabeled'] == 'True':
            self.txtEnabled.SetValue('En-abeled')
            self.txtEnabled.SetBackgroundColour((0,188,0))
        else:
            self.txtEnabled.SetValue('Dis-abeled')
            self.txtEnabled.SetBackgroundColour((188,188,188))
           
        if message['Selected'] == 'True':
            self.txtSelected.SetValue('Selected')
            self.txtSelected.SetBackgroundColour((0,188,0))
        else:
            self.txtSelected.SetValue('Dis-Selected')
            self.txtSelected.SetBackgroundColour((188,188,188))        


    def init_Mainframe(self):
        self.ControlsEnabeled = False
        self.StatusPanelColour = "RedBrown"        
        '''Initialisiert die Objekte des Mainframes'''      
        self.StatusPanel        = xrc.XRCCTRL(self.RootPanel,'StatusPanel')
        self.ValuePanel         = xrc.XRCCTRL(self.RootPanel,'ValuePanel')
        self.BitPanel           = xrc.XRCCTRL(self.RootPanel,'BitPanel')

        # Kinder vom StatusPanel
        self.txtIP             = xrc.XRCCTRL(self.StatusPanel,'txtIP')
        self.txtIP.SetEditable( False )
        self.txtSPort          = xrc.XRCCTRL(self.StatusPanel,'txtRPort')
        self.txtSPort.SetEditable( False )
        self.txtRPort          = xrc.XRCCTRL(self.StatusPanel,'txtSPort')
        self.txtRPort.SetEditable( False )        
        self.txtAxisPos        = xrc.XRCCTRL(self.StatusPanel,'txtAxisPos')
        self.txtAxisPos.SetEditable( False )
        self.txtAxisVel        = xrc.XRCCTRL(self.StatusPanel,'txtAxisVel')
        self.txtAxisVel.SetEditable( False )
        self.txtAxisAmp        = xrc.XRCCTRL(self.StatusPanel,'txtAxisAmp')
        self.txtAxisAmp.SetEditable( False )
        self.txtSetVel         = xrc.XRCCTRL(self.StatusPanel,'txtSetVel')
        self.txtSetVel.SetEditable( False )
        self.txtAxisError      = xrc.XRCCTRL(self.StatusPanel,'txtAxisError')
        self.txtAxisError.SetEditable( False )
        self.btnAxisReset      = xrc.XRCCTRL(self.StatusPanel,'btnAxisReset')    
        self.btnAxisReset.Disable()
        self.txtTimeTick       = xrc.XRCCTRL(self.StatusPanel,'txtTimeTick')
        self.txtTimeTick.SetEditable( False )
        # Kinder vom ValuePanel
        self.txtMaxPos          = xrc.XRCCTRL(self.ValuePanel,'txtMaxPos')
        self.txtMaxPos.SetEditable( False )
        self.txtMinPos          = xrc.XRCCTRL(self.ValuePanel,'txtMinPos')
        self.txtMinPos.SetEditable( False )
        self.txtMaxVel          = xrc.XRCCTRL(self.ValuePanel,'txtMaxVel')
        self.txtMaxVel.SetEditable( False )
        self.txtMaxAcc          = xrc.XRCCTRL(self.ValuePanel,'txtMaxAcc')
        self.txtMaxAcc.SetEditable( False )
        #self.txtConfirmed        = xrc.XRCCTRL(self.ValuePanel,'txtConfirmed')
        #self.txtConfirmed.SetEditable( False )
        self.chkConfirmed        = xrc.XRCCTRL(self.ValuePanel,'chkConfirmed')
        self.chkConfirmed.Disable()
        # Kinder vom BitPanel
        self.txtOnline          = xrc.XRCCTRL(self.BitPanel,'txtOnline')
        self.txtOnline.SetEditable( False )
        self.txtEnabled         = xrc.XRCCTRL(self.BitPanel,'txtEnabled')
        self.txtEnabled.SetEditable( False )
        self.txtSelected        = xrc.XRCCTRL(self.BitPanel,'txtSelected')
        self.txtSelected.SetEditable( False )
        
class Frame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, parent=None, title='Frame', size=(645, 175))
        panel = UI(self, id, title='Title')        
        self.ipc = SyncSend()        
        self.Show()
if __name__ == "__main__":

    app = wx.App(False)
    frame = Frame()
    app.MainLoop()