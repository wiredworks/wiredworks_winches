import bpy
import time
import ctypes

class ww_ActuatorLinDistanceNode(bpy.types.Node):
    '''ww Linear Actuator Distance'''
    bl_idname = 'ww_ActuatorDistance'
    bl_label = 'Distance Actuator'
    bl_icon = 'ARROW_LEFTRIGHT'
    bl_width_min = 920
    bl_width_max = 5000

    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname == 'ww_NodeTree'