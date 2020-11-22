import bpy

class SFX_Actuators_ListProps(bpy.types.PropertyGroup):
    id :   bpy.props.IntProperty(name = 'ID',
                                 description = 'ID',
                                 default = 0)
    name : bpy.props.StringProperty(name = 'Name',
                                 description = 'Name',
                                 default = 'Name')
    path : bpy.props.StringProperty(name = 'Path',
                                 description = 'Path',
                                 default = '')