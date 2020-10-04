import bpy
import time
import math
from scipy.integrate import quad
from scipy.integrate import simps
import numpy as np

class SFX_simpleCueOp(bpy.types.Operator):
    """ simple Cue op"""
    bl_idname = "sfx.simplecueop"
    bl_label = "Simple Cue Operator"

    def modal(self, context, event):
        if event.type == 'TIMER':
            if self.MotherNode.operator_started_bit1:
                self.MotherNode.operator_running_modal = True
                # Trigger Node Update
                self.MotherNode.TickTime_prop = (time.time_ns() - self.old_time)/1000000.0                
                pass
                self.CalculateGrenzVel()
                self.FixEndsOfVelInPos()
                if self.MotherNode.toTime:
                    self.VelFromPosToTime()
                if (self.max_Acc > self.MotherNode.Actuator_props.simple_actuator_VelMax_prop) or \
                   (self.max_Vel > self.MotherNode.Actuator_props.simple_actuator_AccMax_prop):
                    self.MotherNode.confirm = False
                    self.MotherNode.confirmed = False
                if self.MotherNode.confirmed:
                    if not(self.MotherNode.inputs['Go To 1'].default_value):
                        if (self.MotherNode.inputs['Forward'].default_value == True and
                            self.MotherNode.inputs['Reverse'].default_value == False):
                            self.MotherNode.play_state = 'Play'
                            #self.f = self.f+(time.time_ns() - self.old_time)/1000000000.0
                            #print('Up')
                        elif (self.MotherNode.inputs['Forward'].default_value == False and
                            self.MotherNode.inputs['Reverse'].default_value == True):
                            self.MotherNode.play_state = 'Reverse'
                            self.f = self.f-(time.time_ns() - self.old_time)/1000000000.0
                            #print('Down')
                        else:
                            #print('e')
                            pass
                        # self.f =max(0,min(self.f,120))
                        # value = self.Cue_Vel.evaluate(self.f)
                        # print(self.f,value)
                        # self.MotherNode.outputs["Set Vel"].ww_out_value = value
                    else:
                        self.MotherNode.play_state = 'GoTo1'
                        print('Going to one')
                self.old_time = time.time_ns()
                return {'PASS_THROUGH'}
            self.MotherNode.operator_running_modal = False
            return{'CANCELLED'}
        return {'PASS_THROUGH'}
    def execute(self, context):
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def invoke(self, context, event):        
        if not(context.active_node.operator_started_bit1):
            self.old_time = time.time_ns()
            self.MotherNode = context.active_node
            self.length = self.MotherNode.length
            self.MotherNode.operator_started_bit1 = True
            self.max_Acc = 0.0
            self.max_Vel = 0.0
            self.initGraph()
            self.f = 0.0
            return self.execute(context)

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
        self.VelInPos = self.action.fcurves.new('Vel In Pos Domain')
        self.VelInPos.keyframe_points.insert( 0, 1 )
        self.VelInPos.keyframe_points.insert( 1, 1 )
        self.VelInPos.keyframe_points.insert( 2, 1 )
        self.VelInPos.keyframe_points.insert( 3, 1 )
        self.VelInPos.select = True

        self.GrenzVel = self.action.fcurves.new('Vel Limit')
        self.GrenzVel.keyframe_points.insert( 0, 0 )
        self.GrenzVel.keyframe_points.insert( 1, 0 )
        self.GrenzVel.keyframe_points.insert( 2, 0 )
        self.GrenzVel.keyframe_points.insert( 3, 0 )
        self.GrenzVel.select = True
        self.GrenzVel.lock = True
        self.GrenzVel.mute = True

        self.VelInTime = self.action.fcurves.new('Vel In Time Domain')
        self.VelInTime.lock = True

        self.CalculateGrenzVel()
        self.InitializeVelInPos() 
        #self.InitializeVelInTime()

    def CalculateGrenzVel(self):
        self.GrenzVel.lock = True
        self.GrenzVel.mute = True        
        max_Pos = self.MotherNode.Actuator_props.simple_actuator_HardMax_prop
        min_Pos = self.MotherNode.Actuator_props.simple_actuator_HardMin_prop
        max_Vel = self.MotherNode.Actuator_props.simple_actuator_VelMax_prop
        max_Acc = self.MotherNode.Actuator_props.simple_actuator_AccMax_prop

        Point0 = (min_Pos*100,0)
        Point1 = ((min_Pos+(max_Vel*max_Vel)/(2*max_Acc))*100,max_Vel*100)
        Point2 = ((max_Pos-(max_Vel*max_Vel)/(2*max_Acc))*100,max_Vel*100)
        Point3 = (max_Pos*100,0)
        mid_KPos = (max_Pos-min_Pos)/2.0

        if Point1[0]>Point2[0]:
            Point1=(mid_KPos*100,math.sqrt((max_Pos-min_Pos)*max_Acc)*100)
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

    def InitializeVelInPos(self):
        max_Pos = self.MotherNode.Actuator_props.simple_actuator_HardMax_prop
        min_Pos = self.MotherNode.Actuator_props.simple_actuator_HardMin_prop
        max_Vel = self.MotherNode.Actuator_props.simple_actuator_VelMax_prop
        max_Acc = self.MotherNode.Actuator_props.simple_actuator_AccMax_prop

        Point0 = (min_Pos*100,0)
        Point1 = ((min_Pos+(max_Vel*max_Vel)/(2*max_Acc))*100,max_Vel*90)
        Point2 = ((max_Pos-(max_Vel*max_Vel)/(2*max_Acc))*100,max_Vel*90)
        Point3 = (max_Pos*100,0)
        mid_KPos = (max_Pos-min_Pos)/2.0

        if Point1[0]>Point2[0]:
            Point1=(mid_KPos*100,math.sqrt((max_Pos-min_Pos)*max_Acc)*90)
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
        self.VelInPos.keyframe_points[1].handle_left = (Point1[0]-500,max_Vel)
        self.VelInPos.keyframe_points[1].handle_right = (Point1[0] +500,max_Vel)
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

    def FixEndsOfVelInPos(self):
        max_Pos = self.MotherNode.Actuator_props.simple_actuator_HardMax_prop
        min_Pos = self.MotherNode.Actuator_props.simple_actuator_HardMin_prop
        #max_Vel = self.MotherNode.Actuator_props.simple_actuator_VelMax_prop
        #max_Acc = self.MotherNode.Actuator_props.simple_actuator_AccMax_prop
        Point0 = (min_Pos*100,0)
        Point3 = (max_Pos*100,0)        
        self.VelInPos.keyframe_points[0].co = Point0
        self.VelInPos.keyframe_points[0].handle_left = (Point0[0]-500,0)
        self.VelInPos.keyframe_points[0].handle_right = (Point0[0]+500,0)
        self.VelInPos.keyframe_points[-1].co = Point3
        self.VelInPos.keyframe_points[-1].handle_left = (Point3[0]-500,0)
        self.VelInPos.keyframe_points[-1].handle_right = (Point3[0]+500,0)
        #self.VelInPos.update()

    def VelFromPosToTime(self):
        self.MotherNode.toTime = False
        self.MotherNode.confirm = False
        self.MotherNode.confirmen = False
        self.length = self.MotherNode.length
        #self.VelInPos.update()
        print('To Time')
        max_Pos = self.MotherNode.Actuator_props.simple_actuator_HardMax_prop
        min_Pos = self.MotherNode.Actuator_props.simple_actuator_HardMin_prop

        self.action.fcurves.remove(self.VelInTime)
        self.VelInTime = self.action.fcurves.new('Vel In Time Domain')
        self.VelInTime.lock = True       

        self.VelInTime.keyframe_points.insert( 0, 0 )
        Point0=(min_Pos,0)
        self.VelInTime.keyframe_points[0].co = (Point0[0],0)
        self.VelInTime.keyframe_points[0].handle_left_type = 'FREE'#'VECTOR'
        self.VelInTime.keyframe_points[0].handle_right_type = 'FREE'#'VECTOR'
        self.VelInTime.keyframe_points[0].handle_left = (Point0[0]-500,0)
        self.VelInTime.keyframe_points[0].handle_right = (Point0[0]+500,0)
        self.VelInTime.keyframe_points[0].interpolation ='BEZIER'

        for i in range(1,len(self.VelInPos.keyframe_points)-1):
            self.VelInTime.keyframe_points.insert( i, i )

        for i in range(1,len(self.VelInPos.keyframe_points)-1):
            self.VelInTime.keyframe_points[i].co =self.VelInPos.keyframe_points[i].co
            self.VelInTime.keyframe_points[i].handle_left_type = self.VelInPos.keyframe_points[i].handle_left_type
            self.VelInTime.keyframe_points[i].handle_right_type = self.VelInPos.keyframe_points[i].handle_right_type
            self.VelInTime.keyframe_points[i].handle_left = self.VelInPos.keyframe_points[i].handle_left
            self.VelInTime.keyframe_points[i].handle_right = self.VelInPos.keyframe_points[i].handle_right
            self.VelInTime.keyframe_points[i].interpolation ='BEZIER'

        self.VelInTime.keyframe_points.insert(self.VelInPos.keyframe_points[-1].co[0],self.VelInPos.keyframe_points[-1].co[1])       
        self.VelInTime.keyframe_points[-1].handle_left_type = 'FREE'#'VECTOR'
        self.VelInTime.keyframe_points[-1].handle_right_type = 'FREE'#'VECTOR'
        self.VelInTime.keyframe_points[-1].handle_left = self.VelInPos.keyframe_points[-1].handle_left
        self.VelInTime.keyframe_points[-1].handle_right = self.VelInPos.keyframe_points[-1].handle_right
        
        # # debug print
        # print('VelInTime',len(self.VelInTime.keyframe_points))
        # print('VelInPos',len(self.VelInPos.keyframe_points))
        # print('')

        # for i in range(0,len(self.VelInTime.keyframe_points)):
        #     print('')
        #     print('VelInTime Coords          ',self.VelInTime.keyframe_points[i].co)
        #     print('VelInTime LeftHandle Type ',self.VelInTime.keyframe_points[i].handle_left_type)
        #     print('VelInTime RightHandle Type',self.VelInTime.keyframe_points[i].handle_right_type)
        #     print('VelInTime LeftHandle      ',self.VelInTime.keyframe_points[i].handle_left)
        #     print('VelInTime RightHandle     ',self.VelInTime.keyframe_points[i].handle_right)
        # print('')
        # for i in range(0,len(self.VelInPos.keyframe_points)):
        #     print('')
        #     print('VelInPos Values          ',self.VelInPos.keyframe_points[i].co)
        #     print('VelInPos LeftHandle Type ',self.VelInPos.keyframe_points[i].handle_left_type)
        #     print('VelInPos RightHandle Type',self.VelInPos.keyframe_points[i].handle_right_type)
        #     print('VelInPos LeftHandle      ',self.VelInPos.keyframe_points[i].handle_left)
        #     print('VelInPos RightHandle     ',self.VelInPos.keyframe_points[i].handle_right)

        # Wenn der VelInPos Graph ein VelInTime graph wäre hätten wir eine Strecke von 
        self.X= np.linspace(0,self.VelInPos.keyframe_points[-1].co[0],num=10000,retstep=False,dtype=np.double)
        self.Y= np.zeros(10000,dtype=np.double)
        for i in range(0,9999):
            self.Y[i]= self.VelInPos.evaluate(self.X[i])
        self.RohLänge = simps(self.Y,self.X,axis=-1)        
        print('Rohlaenge',self.RohLänge) 
        # zurückgelegt ----- um eine Strecke von self.length zurück zu legen muss die x-Achse um den Faktor 
        F = self.length/(self.RohLänge/100000.0)
        # gedehnt (gestaucht) werden.
        print('Dehnung ',F )
        self.XT = self.X*F
        # Kontrollrechnung
        self.DehnLänge = simps(self.Y,self.XT)
        print('DehnLaenge',self.DehnLänge)
        self.max_Vel = max(self.Y)/100
        self.MotherNode.max_Vel = self.max_Vel
        self.Acc= np.zeros(10000,dtype=np.double)
        for i in range(0,len(self.Y)-2):
            self.Acc[i] = (self.Y[i+1]-self.Y[i])/(self.X[i+1]-self.X[i])
        self.max_Acc =  max(self.Acc)
        self.MotherNode.max_Acc = self.max_Acc
        self.MotherNode.duration = self.XT[-1]/100.0
        # Zur Visualisierung
        for j in range(1,len(self.VelInTime.keyframe_points)):
            self.VelInTime.keyframe_points[j].co[0] = self.VelInTime.keyframe_points[j].co[0]*F
            self.VelInTime.keyframe_points[j].handle_left =(self.VelInPos.keyframe_points[j].handle_left[0]*F,\
                                                            self.VelInPos.keyframe_points[j].handle_left[1])
            self.VelInTime.keyframe_points[j].handle_right =(self.VelInPos.keyframe_points[j].handle_right[0]*F,\
                                                             self.VelInPos.keyframe_points[j].handle_right[1])
