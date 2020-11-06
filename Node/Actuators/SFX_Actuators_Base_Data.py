import bpy

from ... exchange_data.sfx import sfx

class actuator_base():
    def a_update(self,context):
        self.sfx_update(context)

    operator_started : bpy.props.BoolProperty(name = "Demux Operator Started",
                                    description = "Demux Operator Started",
                                    default = False,
                                    update = a_update)
    operator_running_modal: bpy.props.BoolProperty(name = "Demux Operator Running Modal",
                                    description = "Demux Operator Running Modal",
                                    default = False)        
    TickTime_prop : bpy.props.FloatProperty(default=0.0)

    def sfx_update(self,context):
        self.MotherNode = context.active_node
        if self.operator_started:
            Node_root = self.MotherNode.name.split('.')[0]
            Op = 'bpy.ops.sfx.'+Node_root+'_op(\'INVOKE_DEFAULT\')'
            exec(Op)
        else:
            sfx.actuators[self.MotherNode.name].operator_running_modal = False
            self.MotherNode.sfx_update()