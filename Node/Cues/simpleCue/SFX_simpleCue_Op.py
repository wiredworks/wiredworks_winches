import bpy
import time
import math
import hashlib
from scipy.integrate import quad
from scipy.integrate import simps
import numpy as np

from .... exchange_data.sfx import sfx
from . SFX_simpleCue_Data import cue_simple

class SFX_simpleCue_Op(bpy.types.Operator):
    """ simple Cue op"""
    bl_idname = "sfx.simplecue_op"
    bl_label = "Simple Cue Operator"

    def modal(self, context, event):
        if event.type == 'TIMER':
            try:
                sfx.cues[self.MotherNode.name].TickTime_prop = (time.time_ns() - self.old_time)/100000.0
            except KeyError:
                return {'CANCELLED'}
            self.MotherNode.sfx_update()
            if not(sfx.cues[self.MotherNode.name].operator_started):
                sfx.cues[self.MotherNode.name].operator_running_modal = False
                return {'CANCELLED'}
            else:
                sfx.cues[self.MotherNode.name].operator_running_modal = True

                self.cue_act_pos = sfx.cues[self.MotherNode.name].cue_act_pos
                self.cue_act_speed = sfx.cues[self.MotherNode.name].cue_act_speed
       
                if (sfx.cues[self.MotherNode.name].ActConfirmed or sfx.cues[self.MotherNode.name].ActConfirm):
                    self.CanCueBeConfirmed()
                    if sfx.cues[self.MotherNode.name].confirmed:
                        self.CalcTargetSpeed()                   
                        self.ReactToInputs()
                else:
                    #print('modal',self.FcurvesInitialized)
                    sfx.cues[self.MotherNode.name].toTime_executed = False
                    sfx.cues[self.MotherNode.name].confirm = False
                    sfx.cues[self.MotherNode.name].confirmed = False
                    self.ResetFcurves()

                self.CalcKeypointsHash()
                self.old_time = time.time_ns()
                #return {'CANCELLED'}
                return {'PASS_THROUGH'}
        return {'PASS_THROUGH'}


    def execute(self, context):
        self.sfx_entry_exists = True
        self.MotherNode = context.active_node
        self.old_time = time.time_ns()
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        self.sfx_entry_exists = True
        self.MotherNode       = context.active_node
        if not(sfx.cues[self.MotherNode.name].operator_running_modal):
            self.InitVars() 
            self.InitDataobject()
            self.InitGraph()
            return self.execute(context)
        else:
            return {'CANCELLED'}

    def draw(self,context):
        pass

    def InitVars(self): 
            self.length = sfx.cues[self.MotherNode.name].length
            self.MD5Old = ''
            self.MD5   = ''
            self.target_speed = 0.0
            self.target_speed_percent = 0.0
            self.cue_act_speed = 0.0
            self.cue_act_pos = 0.0
            self.max_Vel = 0.0
            self.max_Acc = 0.0
            self.FcurvesInitialized = False
            self.VelInPosInitialized = False
            self.CalcGrenzVelCalculated = False
            sfx.cues[self.MotherNode.name].toTime_executed = False

    def InitDataobject(self):
            try:
                self.Dataobject =  bpy.data.objects[self.MotherNode.name+'_Data']
            except KeyError:
                print(self.MotherNode.name+'_Data' +' not found in ww SFX_Nodes')
                return {'CANCELLED'}
            if self.Dataobject.animation_data:
                self.Dataobject.animation_data_clear()
                bpy.data.actions.remove(bpy.data.actions.get(self.MotherNode.name+'_Cue'))
            if not self.Dataobject.animation_data:
                self.Dataobject.animation_data_create()
            if not self.Dataobject.animation_data.action:
                self.Dataobject.animation_data.action = \
            bpy.data.actions.new(self.MotherNode.name+"_Cue")# or bpy.data.actions.get(self.MotherNode.name+"_Cue")
            self.action = self.Dataobject.animation_data.action

    def InitGraph(self):
        self.InitFcurves()
        self.CalcGrenzVel()
        self.InitVelInPos() 

    def InitFcurves(self):
        err = False
        try:
            self.VelInPos = self.action.fcurves.new('Vel In Pos Domain')
        except RuntimeError:
            err = True
        if not(err):
            self.VelInPos.keyframe_points.insert( 0, 1 )
            self.VelInPos.keyframe_points.insert( 1, 1 )
            self.VelInPos.keyframe_points.insert( 2, 1 )
            self.VelInPos.keyframe_points.insert( 3, 1 )
            self.VelInPos.select = True
        err = False
        try:
            self.GrenzVel = self.action.fcurves.new('Vel Limit')
        except RuntimeError:
            err = True
        if not(err):
            self.GrenzVel.keyframe_points.insert( 0, 0 )
            self.GrenzVel.keyframe_points.insert( 1, 0 )
            self.GrenzVel.keyframe_points.insert( 2, 0 )
            self.GrenzVel.keyframe_points.insert( 3, 0 )
            self.GrenzVel.select = True
            self.GrenzVel.lock = True
            self.GrenzVel.mute = True
        err = False
        try:
            self.VelInTime1 = self.action.fcurves.new('Vel In Time Domain Kp')
        except RuntimeError:
            err = True
        if not(err):
            self.VelInTime1.lock = True
        err = False
        try:
            self.AccInTime = self.action.fcurves.new('Acc In Time Domain')
        except RuntimeError:
            err = True
        if not(err):
            self.AccInTime.lock = True

        self.FcurvesInitialized = True

    def CalcGrenzVel(self):
        Frames_2_Seconds = bpy.data.scenes["Scene"].render.fps / bpy.data.scenes["Scene"].render.fps_base
        self.GrenzVel.lock = True
        self.GrenzVel.mute = True        
        max_Pos = sfx.cues[self.MotherNode.name].Actuator_props.simple_actuator_HardMax_prop
        min_Pos = sfx.cues[self.MotherNode.name].Actuator_props.simple_actuator_HardMin_prop
        max_Vel = sfx.cues[self.MotherNode.name].Actuator_props.simple_actuator_VelMax_prop
        max_Acc = sfx.cues[self.MotherNode.name].Actuator_props.simple_actuator_AccMax_prop

        Point0 = (min_Pos*100,0)
        Point1 = ((min_Pos+(max_Vel*max_Vel)/(2.0*max_Acc))*100,max_Vel*100)
        Point2 = ((max_Pos-(max_Vel*max_Vel)/(2.0*max_Acc))*100,max_Vel*100)
        Point3 = (max_Pos*100,0)
        mid_KPos = (max_Pos-min_Pos)/2.0

        if Point1[0]>Point2[0]:
            Point1=(mid_KPos*100,math.sqrt(((max_Pos-min_Pos)/2.0)*max_Acc)*100)
            Point2 = Point1
        
        self.GrenzVel.keyframe_points[0].co = Point0
        self.GrenzVel.keyframe_points[0].interpolation ='LINEAR'             
        self.GrenzVel.keyframe_points[1].co = Point1
        self.GrenzVel.keyframe_points[1].interpolation ='LINEAR'
        if len(self.GrenzVel.keyframe_points)>2:
            self.GrenzVel.keyframe_points[2].co = Point2
        else:
            self.GrenzVel.keyframe_points.insert( Point2[0] * Frames_2_Seconds,Point2[1] )
        self.GrenzVel.keyframe_points[2].interpolation ='LINEAR'
        if len(self.GrenzVel.keyframe_points)>3:
            self.GrenzVel.keyframe_points[3].co = Point3
        else:
            self.GrenzVel.keyframe_points.insert( Point3[0] * Frames_2_Seconds,Point3[1] )

        self.CalcGrenzVelCalculated = True

    def InitVelInPos(self):
        Frames_2_Seconds = bpy.data.scenes["Scene"].render.fps / bpy.data.scenes["Scene"].render.fps_base
        max_Pos = sfx.cues[self.MotherNode.name].Actuator_props.simple_actuator_HardMax_prop
        min_Pos = sfx.cues[self.MotherNode.name].Actuator_props.simple_actuator_HardMin_prop
        max_Vel = sfx.cues[self.MotherNode.name].Actuator_props.simple_actuator_VelMax_prop
        max_Acc = sfx.cues[self.MotherNode.name].Actuator_props.simple_actuator_AccMax_prop

        Point0 = (min_Pos*100 * Frames_2_Seconds,0)
        Point1 = ((min_Pos+((max_Vel*max_Vel)/(2.0*max_Acc))*1.5)*100 * Frames_2_Seconds,max_Vel*90)
        Point2 = ((max_Pos-((max_Vel*max_Vel)/(2.0*max_Acc))*1.5)*100 * Frames_2_Seconds,max_Vel*90)
        Point3 = (max_Pos*100,0 * Frames_2_Seconds)
        mid_KPos = (max_Pos-min_Pos)/2.0

        if Point1[0]>Point2[0]:
            Point1=(mid_KPos*100,math.sqrt(((max_Pos-min_Pos)/2.0)*max_Acc)*90)
            Point2 = Point1
        
        self.VelInPos.keyframe_points[0].co = Point0
        self.VelInPos.keyframe_points[0].handle_left_type = 'FREE'
        self.VelInPos.keyframe_points[0].handle_right_type = 'FREE'
        self.VelInPos.keyframe_points[0].handle_left = (Point0[0]-500,0)
        self.VelInPos.keyframe_points[0].handle_right = (Point0[0]+500,0)
        self.VelInPos.keyframe_points[0].interpolation ='BEZIER'             
        self.VelInPos.keyframe_points[1].co = Point1
        self.VelInPos.keyframe_points[1].handle_left_type = 'AUTO_CLAMPED'
        self.VelInPos.keyframe_points[1].handle_right_type = 'AUTO_CLAMPED'
        self.VelInPos.keyframe_points[1].handle_left = (Point1[0]-500,Point1[1])
        self.VelInPos.keyframe_points[1].handle_right = (Point1[0] +500,Point1[1])
        self.VelInPos.keyframe_points[1].interpolation ='BEZIER'
        if len(self.VelInPos.keyframe_points)>2:
            self.VelInPos.keyframe_points[2].co = Point2
        else:
            self.VelInPos.keyframe_points.insert(Point2)
        self.VelInPos.keyframe_points[2].handle_left_type = 'AUTO_CLAMPED'
        self.VelInPos.keyframe_points[2].handle_right_type = 'AUTO_CLAMPED'
        self.VelInPos.keyframe_points[2].handle_left = (Point2[0] -500,Point2[1])
        self.VelInPos.keyframe_points[2].handle_right = ((Point2[0] +500),Point2[1])
        self.VelInPos.keyframe_points[2].interpolation ='BEZIER'
        if len(self.VelInPos.keyframe_points)>3:
            self.VelInPos.keyframe_points[3].co = Point3
        else:
            self.VelInPos.keyframe_points.insert(Point3)        
        self.VelInPos.keyframe_points[3].handle_left_type = 'FREE'
        self.VelInPos.keyframe_points[3].handle_right_type = 'FREE'
        self.VelInPos.keyframe_points[3].handle_left = (Point3[0]-500,Point3[1])
        self.VelInPos.keyframe_points[3].handle_right = (Point3[0]+500,Point3[1])

        self.VelInPosInitialized = True

    def FixEndsOfVelInPos(self):
        max_Pos = sfx.cues[self.MotherNode.name].Actuator_props.simple_actuator_HardMax_prop
        min_Pos = sfx.cues[self.MotherNode.name].Actuator_props.simple_actuator_HardMin_prop
        Point0 = (min_Pos*100,0)
        Point3 = (max_Pos*100,0)        
        self.VelInPos.keyframe_points[0].co = Point0
        self.VelInPos.keyframe_points[0].handle_left = (Point0[0]-500,0)
        self.VelInPos.keyframe_points[0].handle_right = (Point0[0]+500,0)
        self.VelInPos.keyframe_points[-1].co = Point3
        self.VelInPos.keyframe_points[-1].handle_left = (Point3[0]-500,0)
        self.VelInPos.keyframe_points[-1].handle_right = (Point3[0]+500,0)

    def VelFromPosToTime(self):
        Frames_2_Seconds = bpy.data.scenes["Scene"].render.fps / bpy.data.scenes["Scene"].render.fps_base
        sfx.cues[self.MotherNode.name].confirm = False
        sfx.cues[self.MotherNode.name].confirmen = False

        self.length = sfx.cues[self.MotherNode.name].length

        # If the Fcurve 'VelInPos' shows 'VelInTime' data we would travel a length of 
        self.X= np.linspace(0,self.VelInPos.keyframe_points[-1].co[0],num=10000,retstep=False,dtype=np.double)
        self.Y= np.zeros(10000,dtype=np.double)
        for i in range(0,9999):
            self.Y[i]= self.VelInPos.evaluate(self.X[i])
        self.RohLänge = simps(self.Y,self.X,axis=-1)        
        # to travel self.length we have to multiply the x-Axis by 
        F = self.length/(self.RohLänge/100000.0)
        self.XT = self.X*F
        # Control-calculation
        #self.DehnLänge = simps(self.Y,self.XT)

        self.max_Vel                                   = max(self.Y)/100
        sfx.cues[self.MotherNode.name].max_Vel         = self.max_Vel
        self.Acc                                       = np.gradient(self.Y)*100
        self.max_Acc                                   = max(abs(self.Acc))/10.0
        sfx.cues[self.MotherNode.name].max_Acc         = self.max_Acc
        sfx.cues[self.MotherNode.name].duration        = self.XT[-1]/1000.0

        self.action.fcurves.remove(self.VelInTime1)
        self.VelInTime1 = self.action.fcurves.new('Vel In Time Domain Kp')
        self.VelInTime1.lock = True 
        for i in range(0,len(self.Y),10):
            self.VelInTime1.keyframe_points.insert( self.XT[i] * Frames_2_Seconds,self.Y[i])

        self.action.fcurves.remove(self.AccInTime)
        self.AccInTime = self.action.fcurves.new('Acc In Time Domain')
        self.AccInTime.lock = True 
        for i in range(0,len(self.Acc),10):
            self.AccInTime.keyframe_points.insert( self.XT[i] * Frames_2_Seconds,self.Acc[i])

        sfx.cues[self.MotherNode.name].toTime = False
        sfx.cues[self.MotherNode.name].toTime_executed = True

    def CanCueBeConfirmed(self):
        if sfx.cues[self.MotherNode.name].toTime_executed:
            if sfx.cues[self.MotherNode.name].confirm:
                sfx.cues[self.MotherNode.name].confirmed = True
            else:
                sfx.cues[self.MotherNode.name].confirmed = False
        else:
            sfx.cues[self.MotherNode.name].confirm = False
            sfx.cues[self.MotherNode.name].confirmed = False

        self.KP = ''
        try:
            for i in range(0,len(self.VelInPos.keyframe_points)):
                self.KP = self.KP+str(self.VelInPos.keyframe_points[i].co)
        except:
            pass
        self.MD5 = hashlib.md5(self.KP.encode('utf-8')).hexdigest()
        if self.MD5 != self.MD5Old:
            sfx.cues[self.MotherNode.name].toTime_executed = False
            sfx.cues[self.MotherNode.name].confirm = False
            sfx.cues[self.MotherNode.name].confirmed = False
            self.ResetFcurves()

        if not(self.FcurvesInitialized):
            self.InitFcurves()
        if not(self.VelInPosInitialized):
            self.InitVelInPos()
        if not(self.CalcGrenzVelCalculated):
            self.CalcGrenzVel()
        self.FixEndsOfVelInPos()

        if sfx.cues[self.MotherNode.name].toTime:
            self.VelFromPosToTime()                

        if (self.max_Vel > sfx.cues[self.MotherNode.name].Actuator_props.simple_actuator_VelMax_prop or
            self.max_Acc > sfx.cues[self.MotherNode.name].Actuator_props.simple_actuator_AccMax_prop) :
            sfx.cues[self.MotherNode.name].toTime_executed = False
            sfx.cues[self.MotherNode.name].confirm = False
            sfx.cues[self.MotherNode.name].confirmed = False

    def CalcKeypointsHash(self):
        self.KPOld = ''
        try:
            for i in range(0,len(self.VelInPos.keyframe_points)):
                self.KPOld = self.KPOld+str(self.VelInPos.keyframe_points[i].co)
        except:
            pass
        self.MD5Old = hashlib.md5(self.KPOld.encode('utf-8')).hexdigest()

    def ReactToInputs(self):                       
        if not( self.MotherNode.inputs['Go To 1'].bool):
            if (self.MotherNode.inputs['Forward'].bool == True and
                self.MotherNode.inputs['Reverse'].bool == False):
                sfx.cues[self.MotherNode.name].cue_diff_speed = self.target_speed - self.cue_act_speed
                if (self.target_speed - self.cue_act_speed) > 0:
                    sfx.cues[self.MotherNode.name].play_state = 'SpeedUp'
                    self.MotherNode.outputs["Set Vel"].float = self.target_speed_percent
                    sfx.cues[self.MotherNode.name].play_head_percent = self.target_speed_percent
                else:
                    sfx.cues[self.MotherNode.name].play_state = 'Play'
                    self.MotherNode.outputs["Set Vel"].float = self.target_speed_percent
                    sfx.cues[self.MotherNode.name].play_head_percent = self.target_speed_percent                                
            elif (self.MotherNode.inputs['Forward'].bool == False and
                    self.MotherNode.inputs['Reverse'].bool == True):
                sfx.cues[self.MotherNode.name].cue_diff_speed = (-self.target_speed - self.cue_act_speed)
                if (-self.target_speed - self.cue_act_speed) <0 :
                    sfx.cues[self.MotherNode.name].play_state = 'Slowing'
                    self.MotherNode.outputs["Set Vel"].float = -self.target_speed_percent
                    sfx.cues[self.MotherNode.name].play_head_percent = -self.target_speed_percent
                else:  
                    sfx.cues[self.MotherNode.name].play_state = 'Reverse'
                    self.MotherNode.outputs["Set Vel"].float = -self.target_speed_percent
                    sfx.cues[self.MotherNode.name].play_head_percent = -self.target_speed_percent
            else:                                
                sfx.cues[self.MotherNode.name].play_state = 'Pause'
                self.MotherNode.outputs["Set Vel"].float = 0.0
        else:
            sfx.cues[self.MotherNode.name].play_state = 'GoTo1'
            self.MotherNode.outputs["Set Vel"].float = 0.0

    def CalcTargetSpeed(self):
        self.target_speed= self.VelInPos.evaluate(self.cue_act_pos*100.0)/100.0
        max_Vel = float(sfx.cues[self.MotherNode.name].Actuator_props.simple_actuator_VelMax_prop)
        try:
            self.target_speed_percent = (self.target_speed/max_Vel)*100.0
        except ZeroDivisionError:
            self.target_speed_percent =0.0
        sfx.cues[self.MotherNode.name].cue_target_speed = self.target_speed

    def ResetFcurves(self):
        if self.FcurvesInitialized:
            self.action.fcurves.remove(self.VelInPos)
            self.action.fcurves.remove(self.GrenzVel)
            self.action.fcurves.remove(self.VelInTime1)
            self.action.fcurves.remove(self.AccInTime)
            self.FcurvesInitialized = False
            self.VelInPosInitialized = False
            self.CalcGrenzVelCalculated = False
            sfx.cues[self.MotherNode.name].toTime_executed = False