import bpy


from .... exchange_data.sfx import sfx
from .... exchange_data.sfx import SFX_Joystick_Inset
from .SFX_simpleCue_Data import cue_simple

class SFX_simpleCue_Node(bpy.types.Node):
    ''' A simple cue to play an actuator'''
    bl_idname = 'SFX_simpleCue'
    bl_label = 'simplecue'
    bl_icon = 'ANCHOR_LEFT'
    bl_width_min = 580
    bl_width_max = 580

    sfx_type ='Cue'

    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname == 'SFX_NodeTree'

    sfx     : bpy.props.PointerProperty(type = sfx)
    sfx_cue : bpy.props.PointerProperty(type = cue_simple)
    
    def init(self, context):
        self.init_sfxData()

        self.outputs.new('SFX_Cue_Float', "Set Vel")
        self.outputs["Set Vel"].default_value_set = SFX_Joystick_Inset
        self.outputs["Set Vel"].ww_out_value = 0.0

        self.inputs.new('SFX_Cue_bool','Forward')
        self.inputs["Forward"].bool = False

        self.inputs.new('SFX_Cue_bool',name= 'Reverse')
        self.inputs["Reverse"].bool = False

        self.inputs.new('SFX_Cue_bool',name= 'Go To 1')
        self.inputs["Reverse"].bool = False

        self.spawnDataobject()

    def copy(self, node):
        print("copied node", node)
        
    def free(self):
        sfx.cues[self.name].operator_opened = False
        sfx.cues.pop(self.name)
        bpy.data.objects.remove(bpy.data.objects[self.name+'_Data'], do_unlink=True)
        bpy.data.actions.remove(bpy.data.actions[self.name+'_Cue'])

    def draw_buttons(self, context, layout):
        try:
            sfx.sensors[self.name]
        except KeyError:
            self.init_sfxData()
        split = layout.split(factor=0.65)
        col = split.column()
        box = col.box()
        col = box.column()
        row = col.row()
        row.prop(sfx.cues[self.name],'play_state',text='')
        row.prop(sfx.cues[self.name],'play_head',text='')
        row.prop(sfx.cues[self.name],'play_head_percent',text='',slider = True)
        row.prop(sfx.cues[self.name],'confirm',text='')
        row.prop(sfx.cues[self.name],'confirmed',text='')
        row = box.row()
        col = row.column()
        col.label(text='Min Pos')
        col.prop(sfx.cues[self.name],'cue_min_pos',text = '')
        col = row.column()
        col.label(text='Set Pos')
        col.prop(sfx.cues[self.name],'cue_set_pos',text='')
        col.label(text='Act Speed')
        col.prop(sfx.cues[self.name],'cue_act_speed',text ='')
        col = row.column()
        col.label(text='Act Pos')
        col.prop(sfx.cues[self.name],'cue_act_pos',text='')
        col.label(text='Target Speed')
        col.prop(sfx.cues[self.name],'cue_target_speed',text='')
        col = row.column()
        col.label(text='Delta')
        col.prop(sfx.cues[self.name],'cue_diff_pos',text='')
        col.label(text='Delta')
        col.prop(sfx.cues[self.name],'cue_diff_speed',text='')
        col = row.column()
        col.label(text='Max Pos')
        col.prop(sfx.cues[self.name],'cue_max_pos',text='')

        col1 = split.column()
        box = col1.box()
        col = box.column()
        row4 = col.split(factor=0.75)         # Tick Time
        row5 = row4.split(factor=0.9)       # running modal
        row6 = row5.split(factor=0.9)       # started
        row7 = row6.split(factor=1)        # start
        row4.prop( sfx.cues[self.name], 'TickTime_prop', text = '')
        row5.prop(sfx.cues[self.name], 'operator_running_modal', text = '')
        row6.prop(sfx.cues[self.name], 'operator_started', text = '')
        if not(sfx.cues[self.name].operator_started):
            row7.label(text ='Stoped')
        else:
            row7.label(text ='Started')

        row = layout.row(align=True)
        row.prop(sfx.cues[self.name], 'expand_Actuator_props')

        if sfx.cues[self.name].expand_Actuator_props:
            row = layout.row(align=True)
            box = row.box()
            row = box.row()
            split2 = row.split(factor = 1)
            col2 = split2.column()
            split5 = row.split(factor = 1)
            col5 = split5.column()
            split6 = row.split(factor = 1)
            col6 = split6.column()
            split7 = row.split(factor = 1)
            col7 = split7.column()
            split8 = row.split(factor = 1)
            col8 = split8.column()
            split9 = row.split(factor = 1)
            col9 = split9.column()
            split10 = row.split(factor = 1)
            col10 = split10.column()
            split11 = row.split(factor = 1)
            col11 = split11.column()
            split12 = row.split(factor = 1)
            col12 = split12.column()
            split13 = row.split(factor = 1)
            col13 = split13.column()

            col2.prop(sfx.cues[self.name],'toTime',text='')
            col5.prop(sfx.cues[self.name],'toTime_executed',text='')
            col6.label(text='C Max Vel')
            col7.prop(sfx.cues[self.name],'max_Vel',text='')
            col8.label(text='C Max Acc')
            col9.prop(sfx.cues[self.name],'max_Acc',text='')
            col10.label(text='C Dur')
            col11.prop(sfx.cues[self.name],'duration',text='')
            col12.prop(sfx.cues[self.name],'confirm',text='')
            col13.prop(sfx.cues[self.name],'confirmed',text='')

            row = box.row()
            sfx.cues[self.name].Actuator_props.drawActuatorSetup(context, row)
                
    def draw_buttons_ext(self, context, layout):
        pass

    def init_sfxData(self):
        sfx.cues.update({self.name :self.sfx_cue})
        pass

    def sfx_update(self):
        if sfx.cues[self.name].operator_running_modal:
            self.color = (0,0.4,0.1)
            self.use_custom_color = True
        else:
            self.use_custom_color = False
        try:
            out1 = self.outputs["Set Vel"]
            inp1 = self.inputs["Forward"]
            inp2 = self.inputs["Reverse"]
            inp3 = self.inputs['Go To 1']
            can_continue = True
        except:
            can_continue = False
        if can_continue:
            if inp1.is_linked:
                for i1 in inp1.links:
                    if i1.is_valid:
                        self.inputs["Forward"].bool=i1.from_socket.node.outputs[i1.from_socket.name].ww_out
                        pass
            if inp2.is_linked:
                for i2 in inp2.links:
                    if i2.is_valid:
                        self.inputs["Reverse"].bool=i2.from_socket.node.outputs[i2.from_socket.name].ww_out
                        pass
            if inp3.is_linked:
                for i3 in inp3.links:
                    if i3.is_valid:
                        self.inputs["Go To 1"].bool=i3.from_socket.node.outputs[i3.from_socket.name].ww_out
                        pass
            if out1.is_linked:
                 for o in out1.links:
                    if o.is_valid:
                        o.to_socket.node.inputs[o.to_socket.name].set_vel = self.outputs["Set Vel"].ww_out_value
                        if o.to_socket.node.sfx_type =='Actuator':
                            sfx.cues[self.name].Actuator_props.simple_actuator_HardMax_prop  = sfx.actuators[o.to_socket.node.name].Actuator_basic_props.Actuator_props.simple_actuator_HardMax_prop
                            sfx.cues[self.name].Actuator_props.simple_actuator_HardMin_prop  = sfx.actuators[o.to_socket.node.name].Actuator_basic_props.Actuator_props.simple_actuator_HardMin_prop
                            sfx.cues[self.name].Actuator_props.simple_actuator_VelMax_prop   = sfx.actuators[o.to_socket.node.name].Actuator_basic_props.Actuator_props.simple_actuator_VelMax_prop
                            sfx.cues[self.name].Actuator_props.simple_actuator_AccMax_prop   = sfx.actuators[o.to_socket.node.name].Actuator_basic_props.Actuator_props.simple_actuator_AccMax_prop
                            sfx.cues[self.name].Actuator_props.simple_actuator_confirm       = sfx.actuators[o.to_socket.node.name].Actuator_basic_props.Actuator_props.simple_actuator_confirm
                            sfx.cues[self.name].Actuator_props.simple_actuator_confirmed     = sfx.actuators[o.to_socket.node.name].Actuator_basic_props.Actuator_props.simple_actuator_confirmed
                            sfx.cues[self.name].cue_act_pos   = sfx.actuators[o.to_socket.node.name].Actuator_basic_props.ist_Pos
                            sfx.cues[self.name].cue_act_speed = sfx.actuators[o.to_socket.node.name].Actuator_basic_props.ist_Vel
                            sfx.cues[self.name].length        = sfx.actuators[o.to_socket.node.name].Actuator_basic_props.DigTwin_basic_props.length
                        elif o.to_socket.node.sfx_type =='Helper':
                            sfx.cues[self.name].Actuator_props.simple_actuator_HardMax_prop  = sfx.helpers[o.to_socket.node.name].Actuator_basic_props.Actuator_props.simple_actuator_HardMax_prop
                            sfx.cues[self.name].Actuator_props.simple_actuator_HardMin_prop  = sfx.helpers[o.to_socket.node.name].Actuator_basic_props.Actuator_props.simple_actuator_HardMin_prop
                            sfx.cues[self.name].Actuator_props.simple_actuator_VelMax_prop   = sfx.helpers[o.to_socket.node.name].Actuator_basic_props.Actuator_props.simple_actuator_VelMax_prop
                            sfx.cues[self.name].Actuator_props.simple_actuator_AccMax_prop   = sfx.helpers[o.to_socket.node.name].Actuator_basic_props.Actuator_props.simple_actuator_AccMax_prop
                            sfx.cues[self.name].Actuator_props.simple_actuator_confirm       = sfx.helpers[o.to_socket.node.name].Actuator_basic_props.Actuator_props.simple_actuator_confirm
                            sfx.cues[self.name].Actuator_props.simple_actuator_confirmed     = sfx.helpers[o.to_socket.node.name].Actuator_basic_props.Actuator_props.simple_actuator_confirmed
                            sfx.cues[self.name].cue_act_pos   = sfx.helpers[o.to_socket.node.name].Actuator_basic_props.ist_Pos
                            sfx.cues[self.name].cue_act_speed = sfx.helpers[o.to_socket.node.name].Actuator_basic_props.ist_Vel
                            sfx.cues[self.name].length        = sfx.helpers[o.to_socket.node.name].Actuator_basic_props.DigTwin_basic_props.length
                        sfx.cues[self.name].ActConfirm    = sfx.cues[self.name].Actuator_props.simple_actuator_confirm
                        sfx.cues[self.name].ActConfirmed  = sfx.cues[self.name].Actuator_props.simple_actuator_confirmed
                        sfx.cues[self.name].cue_min_pos   = sfx.cues[self.name].Actuator_props.simple_actuator_HardMin_prop
                        sfx.cues[self.name].cue_diff_pos  = sfx.cues[self.name].cue_act_pos - sfx.cues[self.name].cue_set_pos
                        sfx.cues[self.name].cue_max_pos   = sfx.cues[self.name].Actuator_props.simple_actuator_HardMax_prop
                    else:
                        sfx.cues[self.name].ActConfirm   = False
                        sfx.cues[self.name].ActConfirmed = False
                        sfx.cues[self.name].cue_min_pos  = 0.0
                        sfx.cues[self.name].cue_act_pos  = 0.0
                        sfx.cues[self.name].cue_diff_pos = 0.0
                        sfx.cues[self.name].cue_max_pos  = 0.0
                        sfx.cues[self.name].length       = 0.0

    def spawnDataobject(self):
        if 'ww SFX_Nodes' in bpy.context.scene.collection.children.keys():
            coll = bpy.data.collections.get("ww SFX_Nodes")
            self.Dataobject = bpy.data.objects.new( self.name+"_Data", None )
            self.Dataobject.empty_display_size = 2
            self.Dataobject.empty_display_type = 'CIRCLE'
            self.Dataobject.location = (0,0,0)
            coll.objects.link(self.Dataobject)