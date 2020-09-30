import bpy
import time

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
                max_Pos = self.MotherNode.Actuator_props.simple_actuator_HardMax_prop
                min_Pos = self.MotherNode.Actuator_props.simple_actuator_HardMin_prop
                max_Vel = self.MotherNode.Actuator_props.simple_actuator_VelMax_prop
                max_Acc = self.MotherNode.Actuator_props.simple_actuator_AccMax_prop
                self.cue.keyframe_points[0].co = (min_Pos,0)
                self.cue.keyframe_points[1].co = ((max_Pos-min_Pos)/2.0,max_Vel)
                self.cue.keyframe_points[2].co = (max_Pos,0)


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
                value = self.cue.evaluate(self.f)
                #print(self.f,value)
                self.MotherNode.outputs["Set Vel"].ww_out_value = value
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

            self.initCue()
            self.f = 0.0
            return self.execute(context)

    def draw(self,context):
        pass

    def initCue(self):
        self.Dataobject =  bpy.data.objects[self.MotherNode.name+'_Data']
        if not self.Dataobject.animation_data:
            self.Dataobject.animation_data_create()
        if not self.Dataobject.animation_data.action:
            self.Dataobject.animation_data.action = bpy.data.actions.new(self.MotherNode.name+"_Cue")
        action = self.Dataobject.animation_data.action
        self.cue = action.fcurves.new('Cue')
        self.cue.select = True
        self.cue.keyframe_points.insert( 0, 0 )
        self.cue.keyframe_points.insert( 60, 100 )
        self.cue.keyframe_points.insert( 120, 0 )
