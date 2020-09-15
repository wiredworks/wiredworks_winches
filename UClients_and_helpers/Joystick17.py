import socket
import time
import json
import joystickapi

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
             'EndCommOPerator' : False,
             'Destroy'         : False}

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
        Shared.ww_Joy["Ptime"]  = self.st
        #print(Shared.ww_Joy)
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

            self.send()
            self.rec()

            diff_BlenderTime_SendTime=(Shared.ww_Joy["Btime"]-Shared.ww_Joy["Ptime"])/1000000.0
            self.lsB.pop(0)
            self.lsB.append(diff_BlenderTime_SendTime)
            self.sumB = 0.0
            for i in range(100):
                self.sumB = self.sumB + self.lsB[i]
            self.avgB = self.sumB/100.0

            diff_Now_BlenderTime = (time.time_ns()-Shared.ww_Joy["Btime"])/1000000.0
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
            print("X-Soll %4.2f Y-Soll %4.2f Z-Soll %4.2f"%(Shared.ww_Joy["X-Achse"],Shared.ww_Joy["Y-Achse"],Shared.ww_Joy["Z-Achse"]))
            print("BlendTime-SendTime %7.4f ms Now-BlendTime %7.4f ms Diff Time: %2.2f ms" %(self.avgB,self.avgN,self.avgT))         


if __name__ == "__main__":
    SyncSend()