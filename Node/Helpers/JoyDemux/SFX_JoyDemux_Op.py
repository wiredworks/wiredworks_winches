import bpy
import time

from .... exchange_data.sfx import sfx

class SFX_OT_JoyDemux_Op(bpy.types.Operator):
    """ This operator updates the demux nodes"""
    bl_idname = "sfx.joydemux_op"
    bl_label = "Demux Updater"

    def modal(self, context, event):
        if event.type == 'TIMER':
            try:
                sfx.helpers[self.MotherNode.name].TickTime_prop = (time.time_ns() - self.old_time)/100000.0
            except KeyError:
                self.sfx_entry_exists = False
                return {'CANCELLED'}
            if self.sfx_entry_exists: 
                self.MotherNode.sfx_update()   
                if not(sfx.helpers[self.MotherNode.name].operator_started):
                    sfx.helpers[self.MotherNode.name].operator_running_modal = False
                    return{'CANCELLED'}
                else:
                    sfx.helpers[self.MotherNode.name].operator_running_modal = True
                    self.old_time = time.time_ns()
                    return {'PASS_THROUGH'}
        return {'PASS_THROUGH'}

    def execute(self, context):
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        self.sfx_entry_exists = True
        self.MotherNode = context.active_node       
        if not(sfx.helpers[self.MotherNode.name].operator_started):
            self.old_time = time.time_ns()
            sfx.helpers[self.MotherNode.name].operator_started = True
            return self.execute(context)
        else:
            return{'CANCELLED'}

    def draw(self,context):
        pass

