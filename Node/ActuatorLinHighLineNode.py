import bpy
import time
import ctypes

class ww_ActuatorLinHighLineNode(bpy.types.Node):
    '''ww Linear Actuator High Line'''
    bl_idname = 'ww_ActuatorLinHighLine'
    bl_label = 'High Line Actuator'
    bl_icon = 'ARROW_LEFTRIGHT'
    bl_width_min = 920
    bl_width_max = 5000

    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname == 'ww_NodeTree'