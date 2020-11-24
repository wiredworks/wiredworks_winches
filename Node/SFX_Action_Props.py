import bpy

class SFX_Action_Props(bpy.types.PropertyGroup):
    id :   bpy.props.StringProperty(name = 'ID',
                                 description = 'ID',
                                 default = '')
    name : bpy.props.StringProperty(name = 'Name',
                                 description = 'Name',
                                 default = 'Name')
    path : bpy.props.StringProperty(name = 'Path',
                                 description = 'Path',
                                 default = '')