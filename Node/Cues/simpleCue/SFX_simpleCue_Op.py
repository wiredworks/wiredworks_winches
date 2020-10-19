import bpy
import time
import math
import hashlib
from scipy.integrate import quad
from scipy.integrate import simps
import numpy as np

class SFX_simpleCue_Op(bpy.types.Operator):
    """ simple Cue op"""
    bl_idname = "sfx.simplecue_op"
    bl_label = "Simple Cue Operator"

    def modal(self, context, event):
        if event.type == 'TIMER':
            if self.MotherNode.operator_started:
                self.MotherNode.operator_running_modal = True
                self.MotherNode.color = (0,0.4,0.1)
                self.MotherNode.use_custom_color = True 
                # Trigger Node Update
                self.MotherNode.TickTime_prop = (time.time_ns() - self.old_time)/1000000.0

                self.cue_act_pos = self.MotherNode.cue_act_pos
                self.cue_act_speed = self.MotherNode.cue_act_speed
                if self.MotherNode.confirm:
                    self.MotherNode.confirmed = True
                self.KP = ''
                try:
                    for i in range(0,len(self.VelInPos.keyframe_points)):
                        self.KP = self.KP+str(self.VelInPos.keyframe_points[i].co)
                except:
                    pass
                self.MD5 = hashlib.md5(self.KP.encode('utf-8')).hexdigest()
                if self.MD5 != self.MD5Old:
                    self.MotherNode.toTime_executed = False
                    self.MotherNode.confirm = False
                    self.MotherNode.confirmed = False                

                if (self.max_Vel > self.MotherNode.Actuator_props.simple_actuator_VelMax_prop or
                    self.max_Acc > self.MotherNode.Actuator_props.simple_actuator_AccMax_prop) :
                    self.MotherNode.confirm = False
                    self.MotherNode.confirmed = False
                    self.MotherNode.toTime_executed = False
                if (self.MotherNode.ActConfirmed or self.MotherNode.ActConfirm):
                    if not(self.FcurvesInitialized):
                        self.initFcurves()
                    if not(self.VelInPosInitialized):
                        self.InitializeVelInPos()
                    if not(self.CalculateGrenzVelCalculated):
                        self.CalculateGrenzVel()
                    self.FixEndsOfVelInPos()
                    if self.MotherNode.toTime:
                        self.VelFromPosToTime()
                    if (self.max_Acc > self.MotherNode.Actuator_props.simple_actuator_VelMax_prop) or \
                       (self.max_Vel > self.MotherNode.Actuator_props.simple_actuator_AccMax_prop):
                        self.MotherNode.confirm = False
                        self.MotherNode.confirmed = False
                    if self.MotherNode.confirmed:
                        self.target_speed= self.VelInPos.evaluate(self.cue_act_pos*100.0)/100.0
                        max_Vel = float(self.MotherNode.Actuator_props.simple_actuator_VelMax_prop)
                        try:
                            self.target_speed_percent = (self.target_speed/max_Vel)*100.0
                        except ZeroDivisionError:
                            self.target_speed_percent =0.0
                        self.MotherNode.cue_target_speed = self.target_speed                        
                        if not(self.MotherNode.inputs['Go To 1'].bool):
                            if (self.MotherNode.inputs['Forward'].bool == True and
                                self.MotherNode.inputs['Reverse'].bool == False):
                                self.MotherNode.cue_diff_speed = self.target_speed - self.cue_act_speed
                                if (self.target_speed - self.cue_act_speed) > 0:
                                    self.MotherNode.play_state = 'SpeedUp'
                                    self.MotherNode.outputs["Set Vel"].ww_out_value = self.target_speed_percent
                                else:
                                    self.MotherNode.play_state = 'Play'
                                    self.MotherNode.outputs["Set Vel"].ww_out_value = self.target_speed_percent                                
                            elif (self.MotherNode.inputs['Forward'].bool == False and
                                  self.MotherNode.inputs['Reverse'].bool == True):
                                self.MotherNode.cue_diff_speed = (-self.target_speed - self.cue_act_speed)
                                if (self.target_speed - self.cue_act_speed) < 0:
                                    self.MotherNode.play_state = 'Slowing'
                                    self.MotherNode.outputs["Set Vel"].ww_out_value = -self.target_speed_percent
                                else:  
                                    self.MotherNode.play_state = 'Reverse'
                                    self.MotherNode.outputs["Set Vel"].ww_out_value = -self.target_speed_percent
                            else:                                
                                self.MotherNode.play_state = 'Pause'
                                self.MotherNode.outputs["Set Vel"].ww_out_value = 0.0
                        else:
                            self.MotherNode.play_state = 'GoTo1'
                            self.MotherNode.outputs["Set Vel"].ww_out_value = 0.0
                else:
                    if self.FcurvesInitialized:
                        self.action.fcurves.remove(self.VelInPos)
                        self.action.fcurves.remove(self.GrenzVel)
                        self.action.fcurves.remove(self.VelInTime1)
                        self.action.fcurves.remove(self.GradInTime)
                        self.FcurvesInitialized = False
                        self.VelInPosInitialized = False
                        self.CalculateGrenzVelCalculated = False
                        self.MotherNode.toTime_executed = False

                self.KPOld = ''
                try:
                    for i in range(0,len(self.VelInPos.keyframe_points)):
                        self.KPOld = self.KPOld+str(self.VelInPos.keyframe_points[i].co)
                except:
                    pass
                self.MD5Old = hashlib.md5(self.KPOld.encode('utf-8')).hexdigest()

                self.old_time = time.time_ns()
                return {'PASS_THROUGH'}
            self.MotherNode.operator_running_modal = False
            self.MotherNode.use_custom_color = False
            return{'CANCELLED'}
        return {'PASS_THROUGH'}
    def execute(self, context):
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        if not(context.active_node.operator_started):
            self.old_time = time.time_ns()
            self.MotherNode = context.active_node            
            self.MotherNode.operator_started = True
            
            self.length = self.MotherNode.length
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
            self.CalculateGrenzVelCalculated = False
            if (self.MotherNode.operator_restart):
                self.Dataobject =  bpy.data.objects[self.MotherNode.name+'_Data']
                self.Dataobject.animation_data_clear()
                bpy.data.actions.remove(bpy.data.actions.get(self.MotherNode.name+'_Cue'))
                if not self.Dataobject.animation_data:
                    self.Dataobject.animation_data_create()
                if not self.Dataobject.animation_data.action:
                    self.Dataobject.animation_data.action = \
                bpy.data.actions.new(self.MotherNode.name+"_Cue")# or bpy.data.actions.get(self.MotherNode.name+"_Cue")
                self.action = self.Dataobject.animation_data.action
                self.FcurvesInitialized = False
                self.VelInPosInitialized = False
                self.CalculateGrenzVelCalculated = False
                self.MotherNode.toTime_executed = False
                self.initGraph()
                return self.execute(context)
            else:
                # Do Init Stuff
                self.initGraph()
                return self.execute(context)
        else:
            return {'CANCELLED'}

    def draw(self,context):
        pass

    def initGraph(self):
        self.Dataobject =  bpy.data.objects[self.MotherNode.name+'_Data']
        if not self.Dataobject.animation_data:
            self.Dataobject.animation_data_create()
        if not self.Dataobject.animation_data.action:
            self.Dataobject.animation_data.action = \
                bpy.data.actions.new(self.MotherNode.name+"_Cue")# or bpy.data.actions.get(self.MotherNode.name+"_Cue")
        self.action = self.Dataobject.animation_data.action
        self.initFcurves()
        self.CalculateGrenzVel()
        self.InitializeVelInPos() 

    def initFcurves(self):
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
            self.GradInTime = self.action.fcurves.new('Grad In Time Domain')
        except RuntimeError:
            err = True
        if not(err):
            self.GradInTime.lock = True

        self.FcurvesInitialized = True

    def CalculateGrenzVel(self):
        self.GrenzVel.lock = True
        self.GrenzVel.mute = True        
        max_Pos = self.MotherNode.Actuator_props.simple_actuator_HardMax_prop
        min_Pos = self.MotherNode.Actuator_props.simple_actuator_HardMin_prop
        max_Vel = self.MotherNode.Actuator_props.simple_actuator_VelMax_prop
        max_Acc = self.MotherNode.Actuator_props.simple_actuator_AccMax_prop

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
            self.GrenzVel.keyframe_points.insert( Point2[0],Point2[1] )
        self.GrenzVel.keyframe_points[2].interpolation ='LINEAR'
        if len(self.GrenzVel.keyframe_points)>3:
            self.GrenzVel.keyframe_points[3].co = Point3
        else:
            self.GrenzVel.keyframe_points.insert( Point3[0],Point3[1] )

        self.CalculateGrenzVelCalculated = True

    def InitializeVelInPos(self):
        max_Pos = self.MotherNode.Actuator_props.simple_actuator_HardMax_prop
        min_Pos = self.MotherNode.Actuator_props.simple_actuator_HardMin_prop
        max_Vel = self.MotherNode.Actuator_props.simple_actuator_VelMax_prop
        max_Acc = self.MotherNode.Actuator_props.simple_actuator_AccMax_prop

        Point0 = (min_Pos*100,0)
        Point1 = ((min_Pos+((max_Vel*max_Vel)/(2.0*max_Acc))*1.5)*100,max_Vel*90)
        Point2 = ((max_Pos-((max_Vel*max_Vel)/(2.0*max_Acc))*1.5)*100,max_Vel*90)
        Point3 = (max_Pos*100,0)
        mid_KPos = (max_Pos-min_Pos)/2.0

        if Point1[0]>Point2[0]:
            Point1=(mid_KPos*100,math.sqrt(((max_Pos-min_Pos)/2.0)*max_Acc)*90)
            Point2 = Point1
        
        self.VelInPos.keyframe_points[0].co = Point0
        self.VelInPos.keyframe_points[0].handle_left_type = 'FREE'#'VECTOR'
        self.VelInPos.keyframe_points[0].handle_right_type = 'FREE'#'VECTOR'
        self.VelInPos.keyframe_points[0].handle_left = (Point0[0]-500,0)
        self.VelInPos.keyframe_points[0].handle_right = (Point0[0]+500,0)
        self.VelInPos.keyframe_points[0].interpolation ='BEZIER'             
        self.VelInPos.keyframe_points[1].co = Point1
        self.VelInPos.keyframe_points[1].handle_left_type = 'AUTO_CLAMPED'#'FREE'#'VECTOR'#
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
        self.VelInPos.keyframe_points[3].handle_left_type = 'FREE'#'VECTOR'
        self.VelInPos.keyframe_points[3].handle_right_type = 'FREE'#'VECTOR'
        self.VelInPos.keyframe_points[3].handle_left = (Point3[0]-500,Point3[1])
        self.VelInPos.keyframe_points[3].handle_right = (Point3[0]+500,Point3[1])

        self.VelInPosInitialized = True

    def FixEndsOfVelInPos(self):
        max_Pos = self.MotherNode.Actuator_props.simple_actuator_HardMax_prop
        min_Pos = self.MotherNode.Actuator_props.simple_actuator_HardMin_prop
        Point0 = (min_Pos*100,0)
        Point3 = (max_Pos*100,0)        
        self.VelInPos.keyframe_points[0].co = Point0
        self.VelInPos.keyframe_points[0].handle_left = (Point0[0]-500,0)
        self.VelInPos.keyframe_points[0].handle_right = (Point0[0]+500,0)
        self.VelInPos.keyframe_points[-1].co = Point3
        self.VelInPos.keyframe_points[-1].handle_left = (Point3[0]-500,0)
        self.VelInPos.keyframe_points[-1].handle_right = (Point3[0]+500,0)

    def VelFromPosToTime(self):
        self.MotherNode.toTime = False
        self.MotherNode.confirm = False
        self.MotherNode.confirmen = False
        self.length = self.MotherNode.length
        print('To Time')

        # Wenn der VelInPos Graph ein VelInTime graph wäre hätten wir eine Strecke von 
        self.X= np.linspace(0,self.VelInPos.keyframe_points[-1].co[0],num=10000,retstep=False,dtype=np.double)
        self.Y= np.zeros(10000,dtype=np.double)
        for i in range(0,9999):
            self.Y[i]= self.VelInPos.evaluate(self.X[i])
        self.RohLänge = simps(self.Y,self.X,axis=-1)        
        # zurückgelegt ----- um eine Strecke von self.length zurück zu legen muss die x-Achse um den Faktor 
        F = self.length/(self.RohLänge/100000.0)
        # gedehnt (gestaucht) werden.
        self.XT = self.X*F
        # Kontrollrechnung
        #self.DehnLänge = simps(self.Y,self.XT)

        self.max_Vel = max(self.Y)/100
        self.MotherNode.max_Vel = self.max_Vel
        self.Acc = np.gradient(self.Y)*100
        self.max_Acc =  max(abs(self.Acc))/10.0
        self.MotherNode.max_Acc = self.max_Acc
        self.MotherNode.duration = self.XT[-1]/1000.0
        self.MotherNode.toTime_executed = True

        # Zur Visualisierung

        self.action.fcurves.remove(self.VelInTime1)
        self.VelInTime1 = self.action.fcurves.new('Vel In Time Domain Kp')
        self.VelInTime1.lock = True 
        for i in range(0,len(self.Y),10):
            self.VelInTime1.keyframe_points.insert( self.XT[i],self.Y[i])

        self.action.fcurves.remove(self.GradInTime)
        self.GradInTime = self.action.fcurves.new('Grad In Time Domain')
        self.GradInTime.lock = True 
        for i in range(0,len(self.Acc),10):
            self.GradInTime.keyframe_points.insert( self.XT[i],self.Acc[i])