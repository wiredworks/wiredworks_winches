import bpy

from .. exchange_data.SFX_Joystick_Inset import SFX_Joystick_Inset
from .. exchange_data.SFX_actuator_basic_Inset import SFX_actuator_basic_Inset
from .. exchange_data.SFX_simple_actuator_Inset import SFX_simple_Actuator_Inset 

class sensor_base():
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
            if not(Node_root == 'linrail' or
                   Node_root == 'joystick'):
                Op = 'bpy.ops.sfx.'+Node_root+'_op(\'INVOKE_DEFAULT\')'
                exec(Op)
        else:
            sfx.sensors[self.MotherNode.name].operator_running_modal = False
            self.MotherNode.sfx_update()

class sensor_joystick(bpy.types.PropertyGroup,sensor_base):
    ''' Defines sfx_sensor'''
    bl_idname = "sfx_sensor"

    Joystick_props : bpy.props.PointerProperty(type = SFX_Joystick_Inset)

    actuator_connected_bit1 : bpy.props.BoolProperty(name = "Connected",
                                    description = " Actuator Connected ?",
                                    default = False)
    actuator_connected_bit2 : bpy.props.BoolProperty(name = "Connected",
                                    description = " Actuator Connected ?",
                                    default = False)

    sensor_name: bpy.props.StringProperty(name = "Actuator Name",
                                    description = "Name of Actuator",
                                    default = "Joystick")    
    socket_ip: bpy.props.StringProperty(name = "Socket ip",
                                    description = "IP of Actuator",
                                    default = "127.0.0.1")
    rsocket_port: bpy.props.StringProperty(name = "Receive Socket port",
                                    description = "Receive Port of Actuator",
                                    default = "15017")
    ssocket_port: bpy.props.StringProperty(name = "Send Socket port",
                                    description = "Send Port of Actuator",
                                    default = "15018")

    expand_Joystick_data : bpy.props.BoolProperty(name = "Joystick Data",
                                    description = "Show Joystick Data",
                                    default = False)

class cue_base():
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
            if not(Node_root == 'linrail' or
                   Node_root == 'joystick'):
                Op = 'bpy.ops.sfx.'+Node_root+'_op(\'INVOKE_DEFAULT\')'
                exec(Op)
        else:
            sfx.cues[self.MotherNode.name].operator_running_modal = False
            self.MotherNode.sfx_update()

class cue_simple(bpy.types.PropertyGroup,cue_base):
    ''' Defines sfx_cue'''
    bl_idname = "sfx_cue"

    play_state_items = (('Play','Play','Play','PLAY',1),
                        ('Pause','Pause','Pause','PAUSE',2),
                        ('SpeedUp','Speed Up','Speeding Up to Play Speed','FF',3),
                        ('Slowing','Slowing','Slowing Down from Play Speed','REW',4),
                        ('Reverse','Reverse','Playing Reverse','PLAY_REVERSE',5),
                        ('GoTo1','Go To 1','Going To Start Position','FRAME_PREV',6))
        
    max_Vel : bpy.props.FloatProperty(name='Max Vel',
                                      description='Max Vel of Cue',
                                      default = 0.0)
    max_Acc : bpy.props.FloatProperty(name='Max Acc',
                                      description='Max Acc of Cue',
                                      default = 0.0)
    duration : bpy.props.FloatProperty(name='Duration',
                                      description='Duration of Cue',
                                      default = 0.0)
    play_head_percent : bpy.props.FloatProperty(name='Play Head',
                                      description='Play Head',
                                      default = 60.0,
                                      soft_max = 100.0,
                                      soft_min = -100.0)
    play_head : bpy.props.FloatProperty(name='Play Head',
                                      description='Play Head',
                                      default = 0.0)
    play_state : bpy.props.EnumProperty(name='Play State',
                                       description = 'Play State of Cue',
                                       items = play_state_items,
                                       default = 'Pause')
    cue_min_pos: bpy.props.FloatProperty(name='Cue Min Pos',
                                      description='Cue Min Pos',
                                      default = 0.0) 
    cue_max_pos: bpy.props.FloatProperty(name='Cue Max Pos',
                                      description='Cue Max Pos',
                                      default = 0.0)
    cue_set_pos: bpy.props.FloatProperty(name='Cue Set Pos',
                                      description='Cue Set Pos',
                                      default = 0.0)
    cue_act_pos: bpy.props.FloatProperty(name='Cue Actual Pos',
                                      description='Cue Actual Pos',
                                      default = 0.0)
    cue_act_speed: bpy.props.FloatProperty(name='Cue Actual Speed',
                                      description='Cue Actual Speed',
                                      default = 0.0)
    cue_target_speed: bpy.props.FloatProperty(name='Cue Target Speed',
                                      description='Cue Target Speed',
                                      default = 0.0)                                                                           
    cue_diff_pos: bpy.props.FloatProperty(name='Cue Dif Pos',
                                      description='Difference Set Act Pos',
                                      default = 0.0)
    cue_diff_speed: bpy.props.FloatProperty(name='Cue Dif Speed',
                                      description='Difference Target Act Speed',
                                      default = 0.0) 
    confirm : bpy.props.BoolProperty(name = "Confirm Cue",
                                    description = "Confirm Cue",
                                    default = False)
    confirmed: bpy.props.BoolProperty(name = "Confiremd Cue",
                                    description = "The Confirmed Cue can be executed",
                                    default = False)
    ActConfirm: bpy.props.BoolProperty(name = "Actuator Confiremd",
                                    description = "The connected Actuator has confirmed properties",
                                    default = False)
    ActConfirmed: bpy.props.BoolProperty(name = "Actuator Confiremd",
                                    description = "The connected Actuator has confirmed properties",
                                    default = False)
    toTime : bpy.props.BoolProperty(name = "To Vel/Time",
                                    description = "To Vel over Time",
                                    default = False)                                            
    toTime_executed : bpy.props.BoolProperty(name = "To Vel/Time",
                                    description = "To Vel over Time",
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


class sfx_kinematic(bpy.types.PropertyGroup):
    ''' Defines sfx_kinematic'''
    bl_idname = "sfx_kinematic"

    X_Achse : bpy.props.FloatProperty(name = "X-Achse",
                                    description = "X-Achse",
                                    precision = 3,
                                    default = 0.001)

class helper_base():
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
            if not(Node_root == 'linrail' or
                   Node_root == 'joystick'):
                Op = 'bpy.ops.sfx.'+Node_root+'_op(\'INVOKE_DEFAULT\')'
                exec(Op)
        else:
            sfx.helpers[self.MotherNode.name].operator_running_modal = False
            self.MotherNode.sfx_update()

class helper_demux(bpy.types.PropertyGroup,helper_base):
    ''' Defines sfx_demux'''
    bl_idname = "sfx_demux"
    pass

class helper_adder(bpy.types.PropertyGroup,helper_base):
    ''' Defines sfx_adder'''
    bl_idname = "sfx_adder"

    Actuator_basic_props : bpy.props.PointerProperty(type =SFX_actuator_basic_Inset)

    expand_Actuator_basic_data : bpy.props.BoolProperty(name = "Expand Basic Data",
                                    description = "Expand Basic Data",
                                    default = False)

class helper_mixer(bpy.types.PropertyGroup,helper_base):
    ''' Defines sfx_mixer'''
    bl_idname = "sfx_mixer"

    Actuator_basic_props : bpy.props.PointerProperty(type =SFX_actuator_basic_Inset)

    expand_Actuator_basic_data : bpy.props.BoolProperty(name = "Expand Basic Data",
                                    description = "Expand Basic Data",
                                    default = False)

    factor : bpy.props.FloatProperty(name='Factor',
                                      description='Factor',
                                      default = 50.0,
                                      soft_max = 100.0,
                                      soft_min = 0.0)


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
            if not(Node_root == 'linrail' or
                   Node_root == 'joystick'):
                Op = 'bpy.ops.sfx.'+Node_root+'_op(\'INVOKE_DEFAULT\')'
                exec(Op)
        else:
            sfx.actuator[self.MotherNode.name].operator_running_modal = False
            self.MotherNode.sfx_update()

class actuator_linrail(bpy.types.PropertyGroup,actuator_base):
    ''' Defines sfx_actuator'''
    bl_idname = "sfx_actuator"

    set_Vel : bpy.props.IntProperty(name = "Set Vel",
                                        description = "Set Vel",
                                        default = 0)
    enable_Act : bpy.props.BoolProperty(name='enable',
                                    description = 'Enable Actuator',
                                    default = False)
    selected_Act : bpy.props.BoolProperty(name='selected',
                                    description = 'Select Actuator',
                                    default = False)

    Actuator_basic_props : bpy.props.PointerProperty(type =SFX_actuator_basic_Inset)

    actuator_connected_bit1 : bpy.props.BoolProperty(name = "Connected",
                                        description = " Actuator Connected ?",
                                        default = False)
    actuator_connected_bit2 : bpy.props.BoolProperty(name = "Connected",
                                        description = " Actuator Connected ?",
                                        default = False)
    actuator_name: bpy.props.StringProperty(name = "Actuator Name",
                                        description = "Name of Actuator",
                                        default = "Anton")    
    socket_ip: bpy.props.StringProperty(name = "Socket ip",
                                        description = "IP of Actuator",
                                        default = "127.0.0.1")
    rsocket_port: bpy.props.StringProperty(name = "Receive Socket port",
                                        description = "Receive Port of Actuator",
                                        default = "15021")
    ssocket_port: bpy.props.StringProperty(name = "Send Socket port",
                                        description = "Send Port of Actuator",
                                        default = "15022")

    expand_Actuator_basic_data : bpy.props.BoolProperty(name = "Expand Basic Data",
                                    description = "Expand Basic Data",
                                    default = False)

class clock(bpy.types.PropertyGroup):
    ''' Defines sfx_clock'''
    bl_idname = "sfx_clock"

    def a_update(self,context):
        self.sfx_update(context)

    operator_started : bpy.props.BoolProperty(name = "Operator Started",
                                    description = "Operator Started",
                                    default = False,
                                    update = a_update)
    operator_running_modal: bpy.props.BoolProperty(name = "Operator Running Modal",
                                    description = "Operator Running Modal",
                                    default = False)
    date :bpy.props.StringProperty(name='Date',
                                    description='Date',
                                    default = 'Sun Jun 20 23:21:05 1993')
    TickTime_prop: bpy.props.FloatProperty(name = "Tick Time",
                                    description ="Sanity Check message round trip Time",
                                    default=0.1,
                                    precision=2)

    def sfx_update(self,context):
        self.MotherNode = context.active_node
        if self.operator_started:
            Node_root = self.MotherNode.name.split('.')[0]
            Op = 'bpy.ops.sfx.'+Node_root+'_op(\'INVOKE_DEFAULT\')'
            exec(Op)
        else:
            sfx.clocks[self.MotherNode.name].operator_running_modal = False
            node_tree = bpy.context.space_data.edit_tree.name
            for key in bpy.data.node_groups[node_tree].nodes.keys():
                Node = bpy.data.node_groups[node_tree].nodes[key]
                bpy.data.node_groups[node_tree].nodes.active = Node
                try:
                    sfx.sensors[Node.name].operator_running_modal    = False
                except KeyError:
                    pass
                try:
                    sfx.cues[Node.name].operator_running_modal       = False
                except KeyError:
                    pass
                try:
                    sfx.kinematics[Node.name].operator_running_modal = False
                except KeyError:
                    pass
                try:
                    sfx.helpers[Node.name].operator_running_modal    = False
                except KeyError:
                    pass
                try:
                    sfx.actuators[Node.name].operator_running_modal    = False
                except KeyError:
                    pass
                Node.sfx_update() 

class sfx(bpy.types.PropertyGroup):
    ''' Defines sfx '''
    bl_idname = "SFX"

    clocks     ={}
    sensors    ={}
    cues       ={}
    kinematics ={}
    helpers    ={}
    actuators  ={}

