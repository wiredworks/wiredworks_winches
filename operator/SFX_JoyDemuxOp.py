import bpy
import time

class SFX_OT_JoyDemuxOp(bpy.types.Operator):
    """ This operator updates the demux nodes"""
    bl_idname = "sfx.joydemuxop"
    bl_label = "Demux Updater"

    def modal(self, context, event):
        if event.type == 'TIMER':
            if self.MotherNode.demux_operator_started_bit1:
                self.MotherNode.demux_operator_running_modal = True
                # Trigger Node Update
                self.MotherNode.TickTime_prop = (time.time_ns() - self.old_time)/1000000.0
                self.old_time = time.time_ns()
                pass
                return {'PASS_THROUGH'}
            self.MotherNode.demux_operator_running_modal = False
            return{'CANCELLED'}
        return {'PASS_THROUGH'}
    def execute(self, context):
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def invoke(self, context, event):        
        if not(context.active_node.demux_operator_started_bit1):
            self.old_time = time.time_ns()
            self.MotherNode = context.active_node
            self.MotherNode.demux_operator_started_bit1 = True
            return self.execute(context)

    def draw(self,context):
        pass

