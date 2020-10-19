import bpy
import time

class SFX_OT_Adder_Op(bpy.types.Operator):
    """ This operator updates the mixer nodes"""
    bl_idname = "sfx.adder_op"
    bl_label = "Adder Updater"

    def modal(self, context, event):
        if event.type == 'TIMER':
            if self.MotherNode.operator_started:
                self.MotherNode.operator_running_modal = True
                self.MotherNode.color = (0,0.4,0.1)
                self.MotherNode.use_custom_color = True 
                # Trigger Node Update
                self.MotherNode.TickTime_prop = (time.time_ns() - self.old_time)/1000000.0
                self.old_time = time.time_ns()
                pass
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
            if (self.MotherNode.operator_restart): 
                return self.execute(context)
            else:
                # Do Init Stuff
                return self.execute(context)
        else:
            return {'CANCELLED'}
            
    def draw(self,context):
        pass

