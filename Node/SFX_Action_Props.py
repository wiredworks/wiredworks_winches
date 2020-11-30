import bpy

class SFX_Action_Props(bpy.types.PropertyGroup):
    id :   bpy.props.IntProperty(name = 'ID',
                                 description = 'ID',
                                 default = 0)
    name : bpy.props.StringProperty(name = 'Name',
                                 description = 'Name',
                                 default = 'Name')
    minPos : bpy.props.FloatProperty(name = 'Min Pos',
                                 description = 'Min Pos',
                                 default = 0)
    maxPos : bpy.props.FloatProperty(name = 'Max Pos',
                                 description = 'Max Pos',
                                 default = 0)
    maxAcc : bpy.props.FloatProperty(name = 'Max Acc',
                                 description = 'Max Acc',
                                 default = 0)
    maxVel : bpy.props.FloatProperty(name = 'Max Vel',
                                 description = 'Max Vel',
                                 default = 0)
    length : bpy.props.FloatProperty(name = 'Length',
                                 description = 'Length',
                                 default = 0)
    Jrk : bpy.props.StringProperty(name = 'Jrk',
                                 description = 'Jrk',
                                 default = '')
    Acc : bpy.props.StringProperty(name = 'Acc',
                                 description = 'Acc',
                                 default = '')
    Vel : bpy.props.StringProperty(name = 'Vel',
                                 description = 'Vel',
                                 default = '')
    Pos : bpy.props.StringProperty(name = 'Pos',
                                 description = 'Pos',
                                 default = '')