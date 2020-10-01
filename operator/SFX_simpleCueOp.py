import bpy
import time
import math

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
                self.CalculateVelInPos()



                if (self.MotherNode.inputs['Forward'].default_value == True and
                    self.MotherNode.inputs['Reverse'].default_value == False):
                    self.f = self.f+(time.time_ns() - self.old_time)/1000000000.0
                    #print('Up')
                elif (self.MotherNode.inputs['Forward'].default_value == False and
                    self.MotherNode.inputs['Reverse'].default_value == True):
                    self.f = self.f-(time.time_ns() - self.old_time)/1000000000.0
                    #print('Down')
                else:
                    #print('e')
                    pass
                self.f =max(0,min(self.f,120))
                #value = self.Cue_Vel.evaluate(self.f)
                #print(self.f,value)
                #self.MotherNode.outputs["Set Vel"].ww_out_value = value
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
            self.MotherNode.operator_started_bit1 = True
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
            self.Dataobject.animation_data.action = bpy.data.actions.new(self.MotherNode.name+"_Cue")
        action = self.Dataobject.animation_data.action
        self.VelInPos = action.fcurves.new('Vel In Pos Domain')
        self.VelInPos.keyframe_points.insert( 0, 1 )
        self.VelInPos.keyframe_points.insert( 1, 1 )
        self.VelInPos.keyframe_points.insert( 2, 1 )
        self.VelInPos.keyframe_points.insert( 3, 1 )
        self.VelInPos.select = True
        self.VelInTime = action.fcurves.new('Vel In Time Domain')
        self.VelInTime.keyframe_points.insert( 0, 2 )
        self.VelInTime.keyframe_points.insert( 1, 2 )
        self.VelInTime.keyframe_points.insert( 2, 2 )
        self.VelInTime.keyframe_points.insert( 3, 2 )
        self.VelInTime.select = True
        self.GrenzVel = action.fcurves.new('Vel Limit')
        self.GrenzVel.keyframe_points.insert( 0, 0 )
        self.GrenzVel.keyframe_points.insert( 1, 0 )
        self.GrenzVel.keyframe_points.insert( 2, 0 )
        self.GrenzVel.keyframe_points.insert( 3, 0 )
        self.GrenzVel.select = True
        self.GrenzVel.lock = True
        self.GrenzVel.mute = True

        self.CalculateGrenzVel()
        self.InitializeVelInPos()

    def CalculateGrenzVel(self):
        self.GrenzVel.lock = True
        self.GrenzVel.mute = True        
        max_Pos = self.MotherNode.Actuator_props.simple_actuator_HardMax_prop
        min_Pos = self.MotherNode.Actuator_props.simple_actuator_HardMin_prop
        max_Vel = self.MotherNode.Actuator_props.simple_actuator_VelMax_prop
        max_Acc = self.MotherNode.Actuator_props.simple_actuator_AccMax_prop

        Point0 = (min_Pos*100,0)
        Point1 = ((min_Pos+(max_Vel*max_Vel)/(2*max_Acc))*100,max_Vel)
        Point2 = ((max_Pos-(max_Vel*max_Vel)/(2*max_Acc))*100,max_Vel)
        Point3 = (max_Pos*100,0)
        mid_KPos = (max_Pos-min_Pos)/2.0

        if Point1[0]>Point2[0]:
            Point1=(mid_KPos*100,math.sqrt((max_Pos-min_Pos)*max_Acc))
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
        Point1 = ((min_Pos+(max_Vel*max_Vel)/(2*max_Acc))*100,max_Vel*0.9)
        Point2 = ((max_Pos-(max_Vel*max_Vel)/(2*max_Acc))*100,max_Vel*0.9)
        Point3 = (max_Pos*100,0)
        mid_KPos = (max_Pos-min_Pos)/2.0

        if Point1[0]>Point2[0]:
            Point1=(mid_KPos*100,math.sqrt((max_Pos-min_Pos)*max_Acc)*0.9)
            Point2 = Point1
        
        self.VelInPos.keyframe_points[0].co = Point0
        self.VelInPos.keyframe_points[0].handle_left_type = 'VECTOR'
        self.VelInPos.keyframe_points[0].handle_right_type = 'VECTOR'
        self.VelInPos.keyframe_points[0].handle_left = (Point0[0]-50,0)
        self.VelInPos.keyframe_points[0].handle_right = (Point0[0]+50,0)
        self.VelInPos.keyframe_points[0].interpolation ='BEZIER'             
        self.VelInPos.keyframe_points[1].co = Point1
        self.VelInPos.keyframe_points[1].handle_left_type = 'AUTO_CLAMPED'
        self.VelInPos.keyframe_points[1].handle_right_type = 'AUTO_CLAMPED'
        self.VelInPos.keyframe_points[1].handle_left = (Point1[0]-50,max_Vel)
        self.VelInPos.keyframe_points[1].handle_right = (Point1[0] +50,max_Vel)
        self.VelInPos.keyframe_points[1].interpolation ='BEZIER'
        if len(self.VelInPos.keyframe_points)>2:
            self.VelInPos.keyframe_points[2].co = Point2
        else:
            self.VelInPos.keyframe_points.insert(Point2)
        self.VelInPos.keyframe_points[2].handle_left_type = 'AUTO_CLAMPED'
        self.VelInPos.keyframe_points[2].handle_right_type = 'AUTO_CLAMPED'
        self.VelInPos.keyframe_points[2].handle_left = (Point2[0] -50,Point2[1])
        self.VelInPos.keyframe_points[2].handle_right = ((Point2[0] +50),Point2[1])
        self.VelInPos.keyframe_points[2].interpolation ='BEZIER'
        if len(self.VelInPos.keyframe_points)>3:
            self.VelInPos.keyframe_points[3].co = Point3
        else:
            self.VelInPos.keyframe_points.insert(Point3)        
        self.VelInPos.keyframe_points[3].handle_left_type = 'VECTOR'
        self.VelInPos.keyframe_points[3].handle_right_type = 'VECTOR'
        self.VelInPos.keyframe_points[3].handle_left = (Point3[0]-50,Point3[1])
        self.VelInPos.keyframe_points[3].handle_right = (Point3[0]+50,Point3[1])

    def CalculateVelInPos(self):
        max_Pos = self.MotherNode.Actuator_props.simple_actuator_HardMax_prop
        min_Pos = self.MotherNode.Actuator_props.simple_actuator_HardMin_prop
        #max_Vel = self.MotherNode.Actuator_props.simple_actuator_VelMax_prop
        #max_Acc = self.MotherNode.Actuator_props.simple_actuator_AccMax_prop
        Point0 = (min_Pos*100,0)
        Point3 = (max_Pos*100,0)        
        self.VelInPos.keyframe_points[0].co = Point0
        self.VelInPos.keyframe_points[0].handle_left = (Point0[0]-50,0)
        self.VelInPos.keyframe_points[0].handle_right = (Point0[0]+50,0)
        self.VelInPos.keyframe_points[-1].co = Point3
        self.VelInPos.keyframe_points[-1].handle_left = (Point3[0]-50,0)
        self.VelInPos.keyframe_points[-1].handle_right = (Point3[0]+50,0)
 