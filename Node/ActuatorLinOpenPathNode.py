import bpy
import time
import ctypes

class ww_ActuatorLinOpenPathNode(bpy.types.Node):
    '''ww Linear Actuator Open Path'''
    bl_idname = 'ww_ActuatorOpenPath'
    bl_label = 'Open Path Line Actuator'
    bl_icon = 'ARROW_LEFTRIGHT'
    bl_width_min = 920
    bl_width_max = 5000

    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname == 'ww_NodeTree'