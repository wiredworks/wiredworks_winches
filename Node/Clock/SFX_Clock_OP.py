import bpy
import time

class SFX_OT_Clock_Op(bpy.types.Operator):
    """ This operator Starts the Clock"""
    bl_idname = "sfx.clock_op"
    bl_label = "Clock Start"

    def modal(self, context, event):
        if event.type == 'TIMER':
            self.MotherNode.TickTime_prop = (time.time_ns() - self.old_time)/100000.0
            if not(self.MotherNode.operator_started):
                self.MotherNode.operator_running_modal = False
                self.MotherNode.use_custom_color = False
                ret =self.End_Comm(context)
                return ret
            else:
                self.MotherNode.operator_running_modal = True
                self.MotherNode.color = (0,0.4,0.1)
                self.MotherNode.use_custom_color = True 
                self.MotherNode.date = time.asctime()
                self.old_time = time.time_ns()
                return {'PASS_THROUGH'}
        return {'PASS_THROUGH'}

    def execute(self, context):
        self._timer = context.window_manager.event_timer_add(0.001, window=context.window)
        self._timer1 = context.window_manager.event_timer_add(0.001, window=context.window)
        self._timer2 = context.window_manager.event_timer_add(0.001, window=context.window)
        context.window_manager.modal_handler_add(self)
        self.old_time = time.time_ns()
        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        if not(context.active_node.operator_started):
            self.old_time = time.time_ns()
            self.MotherNode = context.active_node
            self.MotherNode.operator_started=True
            if (self.MotherNode.operator_restart): 
                return self.execute(context)
            else:
                # Do Init Stuff
                return self.execute(context)
        else:
            return {'CANCELLED'}

    def End_Comm(self,context):        
        context.window_manager.event_timer_remove(self._timer)
        context.window_manager.event_timer_remove(self._timer1)
        context.window_manager.event_timer_remove(self._timer2)
        return {'CANCELLED'} 

 