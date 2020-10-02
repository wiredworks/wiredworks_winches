import bpy
import time
import math
from scipy.integrate import quad
import wx

class SFX_simpleCueOp(bpy.types.Operator):
    """ simple Cue op"""
    bl_idname = "sfx.editsimplecueop"
    bl_label = "Simple Cue Operator"

    def modal(self, context, event):
        if event.type == 'TIMER':
            if self.MotherNode.operator_edit:
                self.MotherNode.operator_editing = True
                # Trigger Node Update
                self.MotherNode.TickTime1_prop = (time.time_ns() - self.old_time)/1000000.0                
                pass
                self.old_time = time.time_ns()
                return {'PASS_THROUGH'}
            self.MotherNode.operator_running_modal = False
            return{'CANCELLED'}
        return {'PASS_THROUGH'}
    def execute(self, context):
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def invoke(self, context, event):        
        #if not(context.active_node.operator_started_bit1):
        self.old_time = time.time_ns()
        self.MotherNode = context.active_node
        self.MotherNode.operator_edit = True
        self.initGraph()

        return{'FINISHED'}

            #return self.execute(context)

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
        for i in range(10000):
            self.VelInPos.keyframe_points.insert( i, i )    
            pass

