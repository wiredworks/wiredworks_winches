import socket
import time
import json
import joystickapi

UDP_IP = "127.0.0.1"
UDP_SENDPORT = 15021
UDP_RECPORT  = 15022

print("UDP target IP: %s" % UDP_IP)
print("UDP target port: %s" % UDP_RECPORT)
print("Round Trip Time through Blender")
print(" ")
class Shared:
    ww_data = { "Ptime" : 0, "Btime" : 0, "X-Soll" : -1.0 , "Y-Soll" : -1.0, "Z-Soll": -1,
                "X-Ist" : 0.0, "Y-Ist" : 0.0, "Z-Ist" : 0.0}

class SyncSend(object):
    def __init__(self):
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
        self.ssock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP 
        #self.rsock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP 
        #self.rsock.bind((UDP_IP,UDP_RECPORT))
        #self.rsock.setblocking(0)
        
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
        self.run()

    def send(self):
        self.st =time.time_ns()
        Shared.ww_data["Ptime"]  = self.st
        Shared.ww_data["X-Soll"] = -2*self.X
        Shared.ww_data["Y-Soll"] = -2*self.Y
        Shared.ww_data["Z-Soll"] = -2*self.Z
        Message = json.dumps(Shared.ww_data)
        MESSAGE = Message.encode('utf-8')
        self.ssock.sendto(MESSAGE, (UDP_IP, UDP_SENDPORT))
        
    def rec(self):
        rsock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP 
        rsock.bind((UDP_IP,UDP_RECPORT))        
        data = "NO DATA"
        data,addr = rsock.recvfrom(512)
        if data != "NO DATA":
            Shared.ww_data = json.loads(data.decode('utf-8'))
            self.rt = time.time_ns()
        rsock.close()
            
    def run(self):
        while True:
            ret, info = joystickapi.joyGetPosEx(0)
            if ret:
                btns = [(1 << i) & info.dwButtons != 0 for i in range(self.caps.wNumButtons)]
                axisXYZ = [info.dwXpos-self.startinfo.dwXpos, info.dwYpos-self.startinfo.dwYpos, info.dwZpos-self.startinfo.dwZpos]
                axisRUV = [info.dwRpos-self.startinfo.dwRpos, info.dwUpos-self.startinfo.dwUpos, info.dwVpos-self.startinfo.dwVpos]
                self.X = axisXYZ[0]
                self.Y = axisXYZ[1]
                self.Z = axisXYZ[2]
            
            self.send()
            self.rec()
            
            diff_BlenderTime_SendTime=(Shared.ww_data["Btime"]-Shared.ww_data["Ptime"])/1000000.0
            self.lsB.pop(0)
            self.lsB.append(diff_BlenderTime_SendTime)
            self.sumB = 0.0
            for i in range(100):
                self.sumB = self.sumB + self.lsB[i]
            self.avgB = self.sumB/100.0
            
            diff_Now_BlenderTime = (time.time_ns()-Shared.ww_data["Btime"])/1000000.0
            self.lsN.pop(0)
            self.lsN.append(diff_Now_BlenderTime)
            self.sumN = 0.0
            for i in range(100):
                self.sumN = self.sumN + self.lsN[i]
            self.avgN = self.sumN/100.0
            
            self.dt = (self.rt -self.st)/1000000.0
            self.lsT.pop(0)
            self.lsT.append(self.dt)
            self.sumT = 0.0
            for i in range(100):
                self.sumT = self.sumT + self.lsT[i]
            self.avgT = self.sumT/100.0
            print("X-Soll %4.2f Y-Soll %4.2f Z-Soll %4.2f"%(Shared.ww_data["X-Soll"],Shared.ww_data["Y-Soll"],Shared.ww_data["Z-Soll"]))
            print("X-Ist %4.2f Y-Ist %4.2f Z-Ist %4.2f"%(Shared.ww_data["X-Ist"],Shared.ww_data["Y-Ist"],Shared.ww_data["Z-Ist"]))
            print("BlendTime-SendTime %7.4f ms Now-BlendTime %7.4f ms Diff Time: %2.2f ms" %(self.avgB,self.avgN,self.avgT))         

        
if __name__ == "__main__":
    SyncSend()