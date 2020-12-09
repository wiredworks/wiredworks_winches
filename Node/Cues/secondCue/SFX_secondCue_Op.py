import bpy
import time
import math
import hashlib
from scipy.integrate import quad
from scipy.integrate import simps
from scipy.signal import savgol_filter


import numpy as np

from .... SFX_Helpers.SFX_Calc_Default_Cue import SFX_Calc_Default_Cue

from .... exchange_data.sfx import sfx
from . SFX_secondCue_Data import cue_second

class SFX_secondCue_Op(bpy.types.Operator):
    """ simple Cue op"""
    bl_idname = "sfx.secondcue_op"
    bl_label = "Second Cue Operator"

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

                #if self.CalcPos:
                #self.FixEndsOfPosInTime()
                #self.CalcVelAccInTime()

                # self.cue_act_pos = sfx.cues[self.MotherNode.name].cue_act_pos
                # self.cue_act_speed = sfx.cues[self.MotherNode.name].cue_act_speed
       
                # if (sfx.cues[self.MotherNode.name].ActConfirmed or sfx.cues[self.MotherNode.name].ActConfirm):
                #     if sfx.cues[self.MotherNode.name].confirmed:
                #         self.CalcTargetSpeed()                   
                #         self.ReactToInputs()
                # else:
                #     #print('modal',self.FcurvesInitialized)
                #     sfx.cues[self.MotherNode.name].toTime_executed = False
                #     sfx.cues[self.MotherNode.name].confirm = False
                #     sfx.cues[self.MotherNode.name].confirmed = False
                #     self.ResetFcurves()

                # self.CalcKeypointsHash()
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

        for screens in bpy.data.screens:
            for area in screens.areas:
                if area.type == 'GRAPH_EDITOR':
                    for spaces in area.spaces:
                        if spaces.type =='GRAPH_EDITOR':
                            spaces.auto_snap = 'NONE'


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
        self.max_Pos = sfx.cues[self.MotherNode.name].Actuator_props.simple_actuator_HardMax_prop
        self.min_Pos = sfx.cues[self.MotherNode.name].Actuator_props.simple_actuator_HardMin_prop
        self.max_Vel = sfx.cues[self.MotherNode.name].Actuator_props.simple_actuator_VelMax_prop
        self.max_Acc = sfx.cues[self.MotherNode.name].Actuator_props.simple_actuator_AccMax_prop
        self.Time    = sfx.cues[self.MotherNode.name].Actuator_props.simple_actuator_Time_prop 
        self.Length  = sfx.cues[self.MotherNode.name].Actuator_props.simple_actuator_HardMax_prop-\
                       sfx.cues[self.MotherNode.name].Actuator_props.simple_actuator_HardMin_prop
        self.MD5Old  = ''
        self.MD5     = ''
        self.target_speed = 0.0
        self.target_speed_percent = 0.0
        self.cue_act_speed = 0.0
        self.cue_act_pos = 0.0
        # self.max_Vel = 0.0
        # self.max_Acc = 0.0
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
        SFX_Calc_Default_Cue(self.Dataobject, self.Length, self.max_Acc, self.max_Vel )
        sfx.cues[self.MotherNode.name].Actuator_props.simple_actuator_Time_prop = \
            bpy.data.objects[self.MotherNode.name+'_Data'].animation_data.action.fcurves[3].keyframe_points[-1].co[0]
        self.Time    = sfx.cues[self.MotherNode.name].Actuator_props.simple_actuator_Time_prop

        # PosTime = bpy.data.objects[self.MotherNode.name+'_Data'].animation_data.action.fcurves[3]
        # VelTime = bpy.data.objects[self.MotherNode.name+'_Data'].animation_data.action.fcurves[2]
        # AccTime = bpy.data.objects[self.MotherNode.name+'_Data'].animation_data.action.fcurves[1]
        # JrkTime = bpy.data.objects[self.MotherNode.name+'_Data'].animation_data.action.fcurves[0]

        # for j in range(len(PosTime.keyframe_points) - 1, 0, -1):
        #             PosTime.keyframe_points.remove(PosTime.keyframe_points[j])
        # for j in range(len(VelTime.keyframe_points) - 1, 0, -1):
        #             VelTime.keyframe_points.remove(VelTime.keyframe_points[j])
        # for j in range(len(AccTime.keyframe_points) - 1, 0, -1):
        #             AccTime.keyframe_points.remove(AccTime.keyframe_points[j])
        # for j in range(len(PosTime.keyframe_points) - 1, 0, -1):
        #             JrkTime.keyframe_points.remove(JrkTime.keyframe_points[j])
        # Point0 = (self.min_Pos,0)
        # Point1 = (self.Time,self.max_Pos)       
        # PosTime.keyframe_points.insert(Point0[0],Point0[1])
        # # self.PosInTime.keyframe_points[0].handle_left = (Point0[0]-1,0)
        # # self.PosInTime.keyframe_points[0].handle_right = (Point0[0]+1,0)
        # PosTime.keyframe_points.insert(Point1[0],Point1[1])
        # # self.PosInTime.keyframe_points[-1].handle_left = (Point1[0]-1,Point1[1])
        # # self.PosInTime.keyframe_points[-1].handle_right = (Point1[0]+1,Point1[1])                         



    def InitFcurves(self):
        try:
            self.AccInTime = self.action.fcurves.new('Jrk')
            self.AccInTime.lock = True
        except RuntimeError:
            print('Runtime Error')
        try:
            self.AccInTime = self.action.fcurves.new('Acc')
            self.AccInTime.lock = True
        except RuntimeError:
            print('Runtime Error')
        try:
            self.VelInTime = self.action.fcurves.new('Vel')
            self.VelInTime.lock = True
        except RuntimeError:
            print('Runtime Error') 
        try:
            self.PosInTime = self.action.fcurves.new('Pos')
        except RuntimeError:
            print('Runntime Error')
        try:
            self.VelPos    = self.action.fcurves.new('PosTime')
        except RuntimeError:
            print('Runntime Error')



    def FixEndsOfPosInTime(self):
        PosTime = bpy.data.objects[self.MotherNode.name+'_Data'].animation_data.action.fcurves[3]
        Point0 = (self.min_Pos,0)
        Point1 = (self.Time,self.max_Pos)       
        PosTime.keyframe_points[0].co = Point0
        # self.PosInTime.keyframe_points[0].handle_left = (Point0[0]-1,0)
        # self.PosInTime.keyframe_points[0].handle_right = (Point0[0]+1,0)
        PosTime.keyframe_points[-1].co = Point1
        # self.PosInTime.keyframe_points[-1].handle_left = (Point1[0]-1,Point1[1])
        # self.PosInTime.keyframe_points[-1].handle_right = (Point1[0]+1,Point1[1])

    def CalcVelAccInTime(self):
        Teilung = 101
        self.X     = np.linspace(0 , self.Time, num = Teilung, retstep = False, dtype = np.longdouble)
        self.dX    = self.X[1] - self.X[0]
        self.PosC  = np.zeros(Teilung, dtype = np.longdouble)
        self.AccC  = np.zeros(Teilung, dtype = np.longdouble)
        self.VelC  = np.zeros(Teilung, dtype = np.longdouble)
        self.JrkC  = np.zeros(Teilung, dtype = np.longdouble)

        VelPos  = bpy.data.objects[self.MotherNode.name+'_Data'].animation_data.action.fcurves[4]
        PosTime = bpy.data.objects[self.MotherNode.name+'_Data'].animation_data.action.fcurves[3]
        VelTime = bpy.data.objects[self.MotherNode.name+'_Data'].animation_data.action.fcurves[2]
        AccTime = bpy.data.objects[self.MotherNode.name+'_Data'].animation_data.action.fcurves[1]
        JrkTime = bpy.data.objects[self.MotherNode.name+'_Data'].animation_data.action.fcurves[0]

        self.PosC[0] = 0
        for i in range(1, len(self.X)):
            self.PosC[i] = PosTime.evaluate(self.X[i])
            self.VelC[i]= (self.PosC[i] - self.PosC[i-1]) / self.dX
        #self.VelC = savgol_filter(self.VelC, 51, 3) # window size 51, polynomial order 3
        for i in range(0,len(self.VelC)):
            VelTime.keyframe_points.insert( self.X[i] , self.VelC[i])

        for i in range(1, len(self.X)):
            self.VelC[i] = VelTime.evaluate(self.X[i])
            self.AccC[i]= (self.VelC[i] - self.VelC[i-1]) / self.dX 
        #self.AccC = savgol_filter(self.AccC, 51, 3) # window size 51, polynomial order 3                
        for i in range(0,len(self.AccC)):
            AccTime.keyframe_points.insert( self.X[i] , self.AccC[i])

        for i in range(1, len(self.X)):
            self.AccC[i] = AccTime.evaluate(self.X[i])
            self.JrkC[i]= (self.AccC[i] - self.AccC[i-1]) / self.dX 
        #self.AccC = savgol_filter(self.AccC, 51, 3) # window size 51, polynomial order 3                
        for i in range(0,len(self.JrkC)):
            JrkTime.keyframe_points.insert( self.X[i] , self.JrkC[i])

        VelPos.keyframe_points.insert( 0 , 0)
        VelPos.keyframe_points.insert( 10 , 10)
        # VelPos.keyframe_points[0].handle_left   = (VelPos.keyframe_points[0].co[0],-10)
        # VelPos.keyframe_points[0].handle_right  = (VelPos.keyframe_points[0].co[0],10)
        # for i in range(0,len(self.X)):
        #     v = VelTime.evaluate(self.X[i])
        #     p = PosTime.evaluate(self.X[i])
        #     if p > 0.015:
        #         VelPos.keyframe_points.insert( p , v)
        # VelPos.keyframe_points[-1].handle_left   = (VelPos.keyframe_points[-1].co[0],10)
        # VelPos.keyframe_points[-1].handle_right  = (VelPos.keyframe_points[-1].co[0],-10)

        #bpy.ops.sfx.simplify_cue('INVOKE_DEFAULT') 


    # def CanCueBeConfirmed(self):
    #     if sfx.cues[self.MotherNode.name].toTime_executed:
    #         if sfx.cues[self.MotherNode.name].confirm:
    #             sfx.cues[self.MotherNode.name].confirmed = True
    #         else:
    #             sfx.cues[self.MotherNode.name].confirmed = False
    #     else:
    #         sfx.cues[self.MotherNode.name].confirm = False
    #         sfx.cues[self.MotherNode.name].confirmed = False

    #     self.KP = ''
    #     try:
    #         for i in range(0,len(self.VelInPos.keyframe_points)):
    #             self.KP = self.KP+str(self.VelInPos.keyframe_points[i].co)
    #     except:
    #         pass
    #     self.MD5 = hashlib.md5(self.KP.encode('utf-8')).hexdigest()
    #     if self.MD5 != self.MD5Old:
    #         sfx.cues[self.MotherNode.name].toTime_executed = False
    #         sfx.cues[self.MotherNode.name].confirm = False
    #         sfx.cues[self.MotherNode.name].confirmed = False
    #         self.ResetFcurves()

    #     if not(self.FcurvesInitialized):
    #         self.InitFcurves()
    #     if not(self.VelInPosInitialized):
    #         self.InitVelInPos()
    #     if not(self.CalcGrenzVelCalculated):
    #         self.CalcGrenzVel()
    #     self.FixEndsOfVelInPos()

    #     if sfx.cues[self.MotherNode.name].toTime:
    #         self.VelFromPosToTime()                

    #     if (self.max_Vel > sfx.cues[self.MotherNode.name].Actuator_props.simple_actuator_VelMax_prop or
    #         self.max_Acc > sfx.cues[self.MotherNode.name].Actuator_props.simple_actuator_AccMax_prop) :
    #         sfx.cues[self.MotherNode.name].toTime_executed = False
    #         sfx.cues[self.MotherNode.name].confirm = False
    #         sfx.cues[self.MotherNode.name].confirmed = False

    # def CalcKeypointsHash(self):
    #     self.KPOld = ''
    #     try:
    #         for i in range(0,len(self.VelInPos.keyframe_points)):
    #             self.KPOld = self.KPOld+str(self.VelInPos.keyframe_points[i].co)
    #     except:
    #         pass
    #     self.MD5Old = hashlib.md5(self.KPOld.encode('utf-8')).hexdigest()

    # def ReactToInputs(self):                       
    #     if not( self.MotherNode.inputs['Go To 1'].bool):
    #         if (self.MotherNode.inputs['Forward'].bool == True and
    #             self.MotherNode.inputs['Reverse'].bool == False):
    #             sfx.cues[self.MotherNode.name].cue_diff_speed = self.target_speed - self.cue_act_speed
    #             if (self.target_speed - self.cue_act_speed) > 0:
    #                 sfx.cues[self.MotherNode.name].play_state = 'SpeedUp'
    #                 self.MotherNode.outputs["Set Vel"].float = self.target_speed_percent
    #                 sfx.cues[self.MotherNode.name].play_head_percent = self.target_speed_percent
    #             else:
    #                 sfx.cues[self.MotherNode.name].play_state = 'Play'
    #                 self.MotherNode.outputs["Set Vel"].float = self.target_speed_percent
    #                 sfx.cues[self.MotherNode.name].play_head_percent = self.target_speed_percent                                
    #         elif (self.MotherNode.inputs['Forward'].bool == False and
    #                 self.MotherNode.inputs['Reverse'].bool == True):
    #             sfx.cues[self.MotherNode.name].cue_diff_speed = (-self.target_speed - self.cue_act_speed)
    #             if (-self.target_speed - self.cue_act_speed) <0 :
    #                 sfx.cues[self.MotherNode.name].play_state = 'Slowing'
    #                 self.MotherNode.outputs["Set Vel"].float = -self.target_speed_percent
    #                 sfx.cues[self.MotherNode.name].play_head_percent = -self.target_speed_percent
    #             else:  
    #                 sfx.cues[self.MotherNode.name].play_state = 'Reverse'
    #                 self.MotherNode.outputs["Set Vel"].float = -self.target_speed_percent
    #                 sfx.cues[self.MotherNode.name].play_head_percent = -self.target_speed_percent
    #         else:                                
    #             sfx.cues[self.MotherNode.name].play_state = 'Pause'
    #             self.MotherNode.outputs["Set Vel"].float = 0.0
    #     else:
    #         sfx.cues[self.MotherNode.name].play_state = 'GoTo1'
    #         self.MotherNode.outputs["Set Vel"].float = 0.0

    # def CalcTargetSpeed(self):
    #     self.target_speed= self.VelInPos.evaluate(self.cue_act_pos*100.0)/100.0
    #     max_Vel = float(sfx.cues[self.MotherNode.name].Actuator_props.simple_actuator_VelMax_prop)
    #     try:
    #         self.target_speed_percent = (self.target_speed/max_Vel)*100.0
    #     except ZeroDivisionError:
    #         self.target_speed_percent =0.0
    #     sfx.cues[self.MotherNode.name].cue_target_speed = self.target_speed

    # def ResetFcurves(self):
    #     if self.FcurvesInitialized:
    #         # self.action.fcurves.remove(self.VelInPos)
    #         # self.action.fcurves.remove(self.GrenzVel)
    #         # self.action.fcurves.remove(self.VelInTime1)
    #         # self.action.fcurves.remove(self.AccInTime)
    #         # self.FcurvesInitialized = False
    #         # self.VelInPosInitialized = False
    #         # self.CalcGrenzVelCalculated = False
    #         # sfx.cues[self.MotherNode.name].toTime_executed = False
    #         pass