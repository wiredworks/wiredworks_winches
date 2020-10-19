import bpy
import time

class SFX_OT_Clock_Op(bpy.types.Operator):
    """ This operator Starts the Clock"""
    bl_idname = "sfx.clock_op"
    bl_label = "Clock Start"

    def modal(self, context, event):
        if event.type == 'TIMER':
            self.MotherNode.TickTime_prop = (time.time_ns() - self.old_time)/1000000.0
            if not(self.MotherNode.operator_started_bit1):             # destroy
                ret =self.End_Comm(context)
                return ret
            else: 
                self.MotherNode.date = time.asctime()
                self.old_time = time.time_ns()
                return {'PASS_THROUGH'}
        return {'PASS_THROUGH'}

    def execute(self, context):
        print('Clock Start -- execute')
        self._timer = context.window_manager.event_timer_add(0.001, window=context.window)
        self._timer1 = context.window_manager.event_timer_add(0.001, window=context.window)
        self._timer2 = context.window_manager.event_timer_add(0.001, window=context.window)
        context.window_manager.modal_handler_add(self)
        self.old_time = time.time_ns()
        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        print('Clock Start -- invoke')
        self.MotherNode = context.active_node
        self.MotherNode.operator_started_bit1=True
 
        return self.execute(context)

    def End_Comm(self,context):        
        print('Clock Start -- end timer')
        self.MotherNode.operator_started_bit1 = False
        context.window_manager.event_timer_remove(self._timer)
        return {'CANCELLED'} 

 