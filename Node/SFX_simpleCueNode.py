import bpy

from .. exchange_data.SFX_Joystick_Inset import SFX_Joystick_Inset
from .. exchange_data.SFX_simple_actuator_Inset import SFX_simple_Actuator_Inset

class SFX_simpleCueNode(bpy.types.Node):
    ''' Takes Joystick Data and outputs selected Data'''
    bl_idname = 'SFX_simpleCueNode'
    bl_label = 'SimpleCue Node'
    bl_icon = 'ANCHOR_LEFT'
    bl_width_min = 500
    bl_width_max = 500

    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname == 'SFX_NodeTree'

    def update_value(self, context):
        self.update ()
        
    TickTime_prop : bpy.props.FloatProperty(default=0.0,
                                            update = update_value)
    TickTime1_prop : bpy.props.FloatProperty(default=0.0,
                                            update = update_value)

    operator_started_bit1 : bpy.props.BoolProperty(name = "Operator Started",
                                    description = "Operator Started",
                                    default = False)
    operator_running_modal: bpy.props.BoolProperty(name = "Operator Running Modal",
                                    description = "Operator Running Modal",
                                    default = False)

    operator_edit : bpy.props.BoolProperty(name = "Operator Edit",
                                    description = "Operator Edit",
                                    default = False)
    operator_editing : bpy.props.BoolProperty(name = "Operator Edit",
                                    description = "Operator Edit",
                                    default = False)

    expand_Actuator_props : bpy.props.BoolProperty(name = "Expand Basic Data",
                                    description = "Expand Basic Data",
                                    default = False)
    length : bpy.props.FloatProperty(name = 'Length',
                                     description = 'Length of Actuator',
                                     default = 0)

    Actuator_props : bpy.props.PointerProperty(type = SFX_simple_Actuator_Inset)

    def init(self, context):
        self.outputs.new('SFX_Cue_Float', "Set Vel")
        self.outputs["Set Vel"].default_value_set = SFX_Joystick_Inset
        self.outputs["Set Vel"].ww_out_value = 0.0

        self.inputs.new('SFX_Cue_bool',name= 'Forward')
        self.inputs["Forward"].default_value = False

        self.inputs.new('SFX_Cue_bool',name= 'Reverse')
        self.inputs["Reverse"].default_value = False

        self.spawnDataobject()

    def copy(self, node):
        print("copied node", node)
        
    def free(self):
        bpy.data.objects.remove(bpy.data.objects[self.name+'_Data'], do_unlink=True)
        bpy.data.actions.remove(bpy.data.actions[self.name+'_Cue'])
        self.operator_started_bit1 = False

    def draw_buttons(self, context, layout):
        split = layout.split(factor=0.65)
        col = split.column()
        col1 = split.column()
        box = col1.box()
        col = box.column()
        row4 = col.split(factor=0.75)         # Tick Time
        row5 = row4.split(factor=0.9)       # running modal
        row6 = row5.split(factor=0.9)       # started
        row7 = row6.split(factor=1)        # start
        row4.prop( self, 'TickTime_prop', text = '')
        row5.prop(self, 'operator_running_modal', text = '')
        row6.prop(self, 'operator_started_bit1', text = '')
        if not(self.operator_started_bit1):
            row7.operator('sfx.simplecueop',text ='Start')
        else:
            row7.operator('sfx.commstarteddiag',text ='Started')

        row = layout.row(align=True)
        row.prop(self, 'expand_Actuator_props')

        if self.expand_Actuator_props:
            row = layout.row(align=True)
            box = row.box()
            row = box.row()
            split = row.split(factor = 0.3)
            row.operator('sfx.editsimplecueop', text = 'Edit')
            row.prop(self,'operator_edit',text='')
            row.prop(self,'operator_editing',text = '')
            row.prop(self,'TickTime1_prop',text='')
            col1 = split.column()
            row = col1.row()
            row.label(text = 'Length')
            row.prop(self,'length', text ='')
            row = box.row()
            self.Actuator_props.drawActuatorSetup(context, row)

    def update(self):
        try:
            out1 = self.outputs["Set Vel"]
            inp1 = self.inputs["Forward"]
            inp2 = self.inputs["Reverse"]
            can_continue = True
        except:
            can_continue = False
        if can_continue:
            #print(self.outputs["Set Vel"].default_value)
            if inp1.is_linked:
                for i1 in inp1.links:
                    if i1.is_valid:
                        #print(i1.from_socket.node.outputs[i1.from_socket.name].ww_out)
                        self.inputs["Forward"].default_value=i1.from_socket.node.outputs[i1.from_socket.name].ww_out
                        #print(self.inputs["Forward"].default_value)
                        pass
            if inp2.is_linked:
                for i2 in inp2.links:
                    if i2.is_valid:
                        self.inputs["Reverse"].default_value=i2.from_socket.node.outputs[i2.from_socket.name].ww_out
                        pass
            if out1.is_linked:
                 for o in out1.links:
                    if o.is_valid:
                        o.to_socket.node.inputs[o.to_socket.name].set_vel = self.outputs["Set Vel"].ww_out_value
                        self.Actuator_props.simple_actuator_HardMax_prop = o.to_socket.node.Actuator_basic_props.Actuator_props.simple_actuator_HardMax_prop
                        self.Actuator_props.simple_actuator_HardMin_prop = o.to_socket.node.Actuator_basic_props.Actuator_props.simple_actuator_HardMin_prop
                        self.Actuator_props.simple_actuator_VelMax_prop = o.to_socket.node.Actuator_basic_props.Actuator_props.simple_actuator_VelMax_prop
                        self.Actuator_props.simple_actuator_AccMax_prop = o.to_socket.node.Actuator_basic_props.Actuator_props.simple_actuator_AccMax_prop
                        self.Actuator_props.simple_actuator_confirm = o.to_socket.node.Actuator_basic_props.Actuator_props.simple_actuator_confirm
                        self.Actuator_props.simple_actuator_confirmed = o.to_socket.node.Actuator_basic_props.Actuator_props.simple_actuator_confirmed
                        self.length = o.to_socket.node.Actuator_basic_props.DigTwin_basic_props.length
                        pass

    def spawnDataobject(self):
        if 'ww SFX_Nodes' in bpy.context.scene.collection.children.keys():
            coll = bpy.data.collections.get("ww SFX_Nodes")
            self.Dataobject = bpy.data.objects.new( self.name+"_Data", None )
            self.Dataobject.empty_display_size = 2
            self.Dataobject.empty_display_type = 'CIRCLE'
            self.Dataobject.location = (0,0,0)
            coll.objects.link(self.Dataobject)