import bpy
import time

from ... exchange_data.sfx import sfx

class SFX_OT_Clock_Op(bpy.types.Operator):
    """ This operator Starts the Clock"""
    bl_idname = "sfx.clock_op"
    bl_label = "Clock Start"

    def modal(self, context, event):
        if event.type == 'TIMER':
            try:
                sfx.clocks[self.MotherNode.name].TickTime_prop = (time.time_ns() - self.old_time)/100000.0
            except KeyError:
                self.sfx_entry_exists = False
                ret = self.End_Timers
                return ret
            if self.sfx_entry_exists:
                self.MotherNode.sfx_update()
                if not(sfx.clocks[self.MotherNode.name].operator_started):
                    sfx.clocks[self.MotherNode.name].operator_running_modal = False
                    ret =self.End_Timers(context)
                    return ret
                else:
                    sfx.clocks[self.MotherNode.name].operator_running_modal = True
                    sfx.clocks[self.MotherNode.name].date = time.asctime() 
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
        self.sfx_entry_exists = True
        self.MotherNode = context.active_node
        if not(sfx.clocks[self.MotherNode.name].operator_started):
            self.old_time = time.time_ns()
            sfx.clocks[self.MotherNode.name].operator_started = True
            return self.execute(context)
        else:
            return {'CANCELLED'}
            
    def draw(self,context):
        pass

    def End_Timers(self,context):        
        context.window_manager.event_timer_remove(self._timer)
        context.window_manager.event_timer_remove(self._timer1)
        context.window_manager.event_timer_remove(self._timer2)
        return {'CANCELLED'} 

 