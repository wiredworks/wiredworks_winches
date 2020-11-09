#!/usr/bin/python
# -*- coding: <<encoding>> -*-


import wx
from wx import xrc

import socket
import time
import json
import joystickapi
import sys

import select

from threading import Thread
from pubsub import pub
print('pubsub API version', pub.VERSION_API)


XRC_Joystick          = "Joystick.xrc"

UDP_IP = "127.0.0.1"
UDP_SENDPORT = 15017
UDP_RECPORT  = 15018

print("UDP target IP: %s" % UDP_IP)
print("UDP target port: %s" % UDP_RECPORT)
print("Round Trip Time through Blender")
print(" ")
class Shared:
    ww_Joy={ 'Ptime'            : 0,
             'Btime'            : 0,
             'X-Achse'          : 0,
             'Y-Achse'          : 0,
             'Z-Achse'          : 0,
             'X-Rot'            : 0,
             'Y-Rot'            : 0,
             'Z-Rot'            : 0,
             'Slider'           : 0,
             'Buttons'          : 0,
             'HAT-Switch'       : 0,
             'EndCommOPerator'  : False,
             'Destroy'          : False,
             'X-Soll'           : 0,
             'Y-Soll'           : 0,
             'Z-Soll'           : 0}

class SyncSend(Thread):
    def __init__(self):
        
        Thread.__init__(self)
        
        self.oldtime = time.time_ns()
        self.SendTime = time.time_ns()
        self.rt = self.SendTime
        self.dt = self.rt-self.SendTime
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
        self.ssock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP 
        
        num = joystickapi.joyGetNumDevs()
        ret, self.caps, self.startinfo = False, None, None
        for id in range(num):
            self.ret, self.caps = joystickapi.joyGetDevCaps(id)
            if self.ret:
                print("gamepad detected: " + self.caps.szPname)
                self.ret, self.startinfo = joystickapi.joyGetPosEx(id)
                break
        else:
            print("no gamepad detected")        
        print(" ")
        self.setDaemon(True)
        self.start()

    def send(self):
        self.SendTime =time.time_ns()
        Shared.ww_Joy["Ptime"]  = self.SendTime
        Message = json.dumps(Shared.ww_Joy)
        MESSAGE = Message.encode('utf-8')
        self.ssock.sendto(MESSAGE, (UDP_IP, UDP_SENDPORT))
        
    def rec(self):
        rsock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP 
        rsock.bind((UDP_IP,UDP_RECPORT))        
        data = "NO DATA"
        data,addr = rsock.recvfrom(512)
        if data != "NO DATA":
            Shared.ww_Joy = json.loads(data.decode('utf-8'))
            self.rt = time.time_ns()
        rsock.close()
            
    def run(self):
        while True:
            ret, info = joystickapi.joyGetPosEx(0)
            if ret:
                btns = [(1 << i) & info.dwButtons != 0 for i in range(self.caps.wNumButtons)]
                axisXYZ = [info.dwXpos-self.startinfo.dwXpos, info.dwYpos-self.startinfo.dwYpos, info.dwZpos-self.startinfo.dwZpos]
                axisRUV = [info.dwRpos-self.startinfo.dwRpos, info.dwUpos-self.startinfo.dwUpos, info.dwVpos-self.startinfo.dwVpos]
                Shared.ww_Joy['X-Achse']    = axisXYZ[0]
                Shared.ww_Joy['Y-Achse']    = axisXYZ[1]
                Shared.ww_Joy['Z-Achse']    = axisXYZ[2]
                Shared.ww_Joy['X-Rot']      = axisRUV[0]
                Shared.ww_Joy['Y-Rot']      = axisRUV[1]
                Shared.ww_Joy['Z-Rot']      = axisRUV[2]
                Shared.ww_Joy['Slider']     = 0
                Shared.ww_Joy['Buttons']    = btns
                Shared.ww_Joy['HAT-Switch'] = 0
                print(Shared.ww_Joy['Ptime'],Shared.ww_Joy['Btime'],Shared.ww_Joy['X-Achse'], end='\r')
            
            self.send()
            self.rec()

            diff_BlenderTime_SendTime=(Shared.ww_Joy["Btime"]-Shared.ww_Joy["Ptime"])/1000000.0
            self.lsB.pop(0)
            self.lsB.append(diff_BlenderTime_SendTime)
            self.sumB = 0.0
            for i in range(100):
                self.sumB = self.sumB + self.lsB[i]
            self.avgB = self.sumB/100.0
            
            diff_Now_BlenderTime = (time.time_ns()-Shared.ww_Joy["Ptime"])/1000000.0
            self.lsN.pop(0)
            self.lsN.append(diff_Now_BlenderTime)
            self.sumN = 0.0
            for i in range(100):
                self.sumN = self.sumN + self.lsN[i]
            self.avgN = self.sumN/100.0
            
            self.dt = (time.time_ns() -self.SendTime)/1000000.0
            self.lsT.pop(0)
            self.lsT.append(self.dt)
            self.sumT = 0.0
            for i in range(100):
                self.sumT = self.sumT + self.lsT[i]
            self.avgT = self.sumT/100.0
            #print("X-Soll %4.2f Y-Soll %4.2f Z-Soll %4.2f"%(Shared.ww_Joy["X-Soll"],Shared.ww_Joy["Y-Soll"],Shared.ww_Joy["Z-Soll"]))
            #print("BlendTime-SendTime %7.4f ms Round Trip %7.4f ms Diff Time: %2.2f ms" %(self.avgB,self.avgN,self.avgT))
            #print(' Diff 1: %7.4f Diff 2: %7.4f Diff 3: %7.4f'%((self.avgN-self.avgB),(self.avgT-self.avgN),(self.avgT-self.avgB)))
            wx.CallAfter(pub.sendMessage,'update',message=Shared.ww_Joy,ff=(self.avgT))

class JoystickUI(wx.Panel):
    def __init__(self, parent, id, title):
        self.locale = wx.Locale(wx.LANGUAGE_ENGLISH)

        wx.Frame.__init__(self, parent, size=(200,400))
        
        #self.res = xrc.XmlResource(XRC_Joystick)
        #self.RootPanel = self.res.LoadPanel(self,'RootPanel')
        self.init_Mainframe()
        
        pub.subscribe(self.PPPP,'update')
        
    def PPPP(self,message,ff):
        A="%2.2f"%(ff)
        self.txtRoundTrip.SetValue(A)
        self.txtX_Achse.SetValue(str(Shared.ww_Joy['X-Achse']))
        self.txtY_Achse.SetValue(str(Shared.ww_Joy['Y-Achse']))
        self.txtZ_Achse.SetValue(str(Shared.ww_Joy['Z-Achse']))
        self.txtX_Rot.SetValue(str(Shared.ww_Joy['X-Rot']))
        self.txtY_Rot.SetValue(str(Shared.ww_Joy['Y-Rot']))
        self.txtZ_Rot.SetValue(str(Shared.ww_Joy['Z-Rot']))
        #self.txtButtons        =Shared.ww_Joy['Buttons']

    def init_Mainframe(self):
        self.RootPanel = wx.Panel(self,-1,size = (150,150))
        
        self.txtRoundTrip = wx.TextCtrl(self, wx.ID_ANY, "")
        self.txtX_Achse = wx.TextCtrl(self, wx.ID_ANY, "44")
        self.txtY_Achse = wx.TextCtrl(self, wx.ID_ANY, "")
        self.txtZ_Achse = wx.TextCtrl(self, wx.ID_ANY, "")
        self.txtX_Rot = wx.TextCtrl(self, wx.ID_ANY, "")
        self.txtY_Rot = wx.TextCtrl(self, wx.ID_ANY, "")
        self.txtZ_Rot = wx.TextCtrl(self, wx.ID_ANY, "")
        self.txtButtons = wx.TextCtrl(self, wx.ID_ANY, "")      
        
        #self.SetSizer(box)
        object_1 = wx.BoxSizer(wx.VERTICAL)
        label_14 = wx.StaticText(self, wx.ID_ANY, "Round Trip Time")
        object_1.Add(label_14, 0, 0, 0)
        object_1.Add(self.txtRoundTrip, 0, 0, 0)
        label_7 = wx.StaticText(self, wx.ID_ANY, "X-Achse")
        label_7.SetMinSize((-1, 20))
        label_7.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_GRADIENTACTIVECAPTION))
        object_1.Add(label_7, 0, 0, 0)
        object_1.Add(self.txtX_Achse, 0, 0, 0)
        label_8 = wx.StaticText(self, wx.ID_ANY, "Y-Achse")
        object_1.Add(label_8, 0, 0, 0)
        object_1.Add(self.txtY_Achse, 0, 0, 0)
        label_9 = wx.StaticText(self, wx.ID_ANY, "Z-Achse")
        object_1.Add(label_9, 0, 0, 0)
        object_1.Add(self.txtZ_Achse, 0, 0, 0)
        label_10 = wx.StaticText(self, wx.ID_ANY, "X-Rot")
        object_1.Add(label_10, 0, 0, 0)
        object_1.Add(self.txtX_Rot, 0, 0, 0)
        label_11 = wx.StaticText(self, wx.ID_ANY, "Y-Rot")
        object_1.Add(label_11, 0, 0, 0)
        object_1.Add(self.txtY_Rot, 0, 0, 0)
        label_12 = wx.StaticText(self, wx.ID_ANY, "Z-Rot")
        object_1.Add(label_12, 0, 0, 0)
        object_1.Add(self.txtZ_Rot, 0, 0, 0)
        label_13 = wx.StaticText(self, wx.ID_ANY, "Buttons")
        object_1.Add(label_13, 0, 0, 0)
        object_1.Add(self.txtButtons, 0, 0, 0)
        self.SetSizer(object_1)      

class Frame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, parent=None, title='Frame', size=(130, 350))
        panel = JoystickUI(self, id, title='Title')
        
        self.ipc = SyncSend()
        
        self.Show()
if __name__ == "__main__":
    print(sys.executable)
    app = wx.App(False)
    frame = Frame()
    app.MainLoop()