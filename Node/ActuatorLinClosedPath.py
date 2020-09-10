import bpy
import time
import ctypes

class ww_ActuatorLinClosedPathNode(bpy.types.Node):
    '''ww Linear Actuator Closed Path'''
    bl_idname = 'ww_ActuatorClosedPath'
    bl_label = 'Closed Path Line Actuator'
    bl_icon = 'ARROW_LEFTRIGHT'
    bl_width_min = 920
    bl_width_max = 5000

    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname == 'ww_NodeTree'