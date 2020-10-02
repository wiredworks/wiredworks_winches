import bpy
import time
import math
from scipy.integrate import quad

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
            self.length = self.MotherNode.length
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

        #self.VelInPos.update()


    def FixEndsOfVelInPos(self):
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
        #self.VelInPos.update()

    def VelFromPosToTime(self):
        self.MotherNode.toTime = False
        #self.VelInPos.update()
        print('To Time')
        max_Pos = self.MotherNode.Actuator_props.simple_actuator_HardMax_prop
        min_Pos = self.MotherNode.Actuator_props.simple_actuator_HardMin_prop
        self.VelInTime = self.action.fcurves.new('Vel In Time Domain')
        self.VelInTime.keyframe_points.insert( 0, 0 )
        Point0=(min_Pos,0)
        self.VelInTime.keyframe_points[0].co = (Point0[0],0)
        self.VelInTime.keyframe_points[0].handle_left_type = 'VECTOR'
        self.VelInTime.keyframe_points[0].handle_right_type = 'VECTOR'
        self.VelInTime.keyframe_points[0].handle_left = (Point0[0]-50,0)
        self.VelInTime.keyframe_points[0].handle_right = (Point0[0]+50,0)
        self.VelInTime.keyframe_points[0].interpolation ='BEZIER'

        print('VelInTime 0',len(self.VelInTime.keyframe_points))
        print(self.VelInTime.keyframe_points[0].co)

        for i in range(1,len(self.VelInPos.keyframe_points)-1):
            self.VelInTime.keyframe_points.insert( i, i )

        print('VelInTime 1',len(self.VelInTime.keyframe_points))
        print('VelInPos',len(self.VelInPos.keyframe_points))

        for i in range(1,len(self.VelInPos.keyframe_points)-1):
            print(i)            
            self.VelInTime.keyframe_points[i].co =self.VelInPos.keyframe_points[i].co
            print(self.VelInTime.keyframe_points[i].co)
            self.VelInTime.keyframe_points[i].handle_left_type = 'AUTO_CLAMPED'
            self.VelInTime.keyframe_points[i].handle_right_type = 'AUTO_CLAMPED'
            self.VelInTime.keyframe_points[i].handle_left = self.VelInPos.keyframe_points[i].handle_left
            self.VelInTime.keyframe_points[i].handle_right = self.VelInPos.keyframe_points[i].handle_right
            self.VelInTime.keyframe_points[i].interpolation ='BEZIER'

        print('VelInTime 2',len(self.VelInTime.keyframe_points))
        self.VelInTime.keyframe_points.insert(self.VelInPos.keyframe_points[-1].co[0],self.VelInPos.keyframe_points[-1].co[1])       
        self.VelInTime.keyframe_points[-1].handle_left_type = 'VECTOR'
        self.VelInTime.keyframe_points[-1].handle_right_type = 'VECTOR'
        self.VelInTime.keyframe_points[-1].handle_left = self.VelInPos.keyframe_points[-1].handle_left
        self.VelInTime.keyframe_points[-1].handle_right = self.VelInPos.keyframe_points[-1].handle_right
        
        #self.VelInTime.update()
        print('VelInTime 3',len(self.VelInTime.keyframe_points))

        for i in range(0,len(self.VelInPos.keyframe_points)):
            print('VelInTime Coords          ',self.VelInTime.keyframe_points[i].co)
            print('VelInTime LeftHandle Type ',self.VelInTime.keyframe_points[i].handle_left_type)
            print('VelInTime RightHandle Type',self.VelInTime.keyframe_points[i].handle_right_type)
            print('VelInTime LeftHandle      ',self.VelInTime.keyframe_points[i].handle_left)
            print('VelInTime RightHandle     ',self.VelInTime.keyframe_points[i].handle_right)

        for i in range(0,len(self.VelInPos.keyframe_points)):
            print('VelInPos Values          ',self.VelInPos.keyframe_points[i].co)
            print('VelInPos LeftHandle Type ',self.VelInPos.keyframe_points[i].handle_left_type)
            print('VelInPos RightHandle Type',self.VelInPos.keyframe_points[i].handle_right_type)
            print('VelInPos LeftHandle      ',self.VelInPos.keyframe_points[i].handle_left)
            print('VelInPos RightHandle     ',self.VelInPos.keyframe_points[i].handle_right)



        # TraveledDistance = (quad(lambda x: self.VelInTime.evaluate(x),min_Pos*100,max_Pos*100))
        # print(TraveledDistance)
        # print('#')
        # while TraveledDistance[0]/100000 -self.length < 0:
        #     for i in range(1,len(self.VelInTime.keyframe_points)):
        #        self.VelInTime.keyframe_points[i].co[0]*1.01
        #     TraveledDistance = quad(lambda x: self.VelInTime.evaluate(x),min_Pos*100,max_Pos*100)[0]/10000
        #     print(TraveledDistance)