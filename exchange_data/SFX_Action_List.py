import bpy

from bpy.types import UIList
from bpy_extras.io_utils import ImportHelper
import os
import json

from .sfx import sfx

def read_some_data(context, filepath, item):
    f = open(filepath, 'r', encoding='utf-8')
    data = f.read()
    f.close()
    Data = data.split(';')
    item.id = float(Data[0])
    item.name = Data[1]
    item.minPos = float(Data[2])
    item.maxPos = float(Data[3])
    item.maxAcc = float(Data[4])
    item.maxVel = float(Data[5])
    item.length = float(Data[6])
    item.Jrk    = Data[7]
    item.Acc    = Data[8]
    item.Vel    = Data[9]
    item.Pos    = Data[10]

    return {'FINISHED'}

class SFX_OT_list_actions(bpy.types.Operator):
    bl_idname = "sfx.list_action"
    bl_label = "List Action"

    action : bpy.props.EnumProperty(
        items=(
            ('UP', "Up", ""),
            ('DOWN', "Down", ""),
            ('REMOVE', "Remove", ""),
            ('ADD', "Add", ""),
            ('SAVE', "Save", "")
        )
    )
    def invoke(self, context, event):
        print('sfx.list_action.invoke')

        MotherNode = context.active_node
        sfx_actions   = sfx.actuators[MotherNode.name].Actuator_basic_props.Actuator_props.SFX_actions

        try:
            item = sfx_actions[sfx.actuators[MotherNode.name].Actuator_basic_props.Actuator_props.SFX_actions_index]
        except IndexError:
            pass
        if (self.action == 'DOWN' and \
            sfx.actuators[MotherNode.name].Actuator_basic_props.Actuator_props.SFX_actions_index < len(sfx_actions)-1):
            sfx.actuators[MotherNode.name].Actuator_basic_props.Actuator_props.SFX_actions_index +=1
            index = sfx.actuators[MotherNode.name].Actuator_basic_props.Actuator_props.SFX_actions_index 
            self.update_fcurves(context, sfx_actions, index) 

        elif (self.action == 'UP' and \
            sfx.actuators[MotherNode.name].Actuator_basic_props.Actuator_props.SFX_actions_index> 0):
            sfx.actuators[MotherNode.name].Actuator_basic_props.Actuator_props.SFX_actions_index -= 1
            index = sfx.actuators[MotherNode.name].Actuator_basic_props.Actuator_props.SFX_actions_index
            self.update_fcurves(context, sfx_actions, index)

        elif self.action == 'REMOVE':
            if sfx.actuators[MotherNode.name].Actuator_basic_props.Actuator_props.SFX_actions_index > 0:
                sfx_actions.remove(sfx.actuators[MotherNode.name].Actuator_basic_props.Actuator_props.SFX_actions_index)
                sfx.actuators[MotherNode.name].Actuator_basic_props.Actuator_props.SFX_actions_index -= 1
                index = sfx.actuators[MotherNode.name].Actuator_basic_props.Actuator_props.SFX_actions_index
                self.update_fcurves(context, sfx_actions, index)

        if self.action == 'ADD':
            bpy.ops.sfx.select_operator('INVOKE_DEFAULT')            
            sfx.actuators[MotherNode.name].Actuator_basic_props.Actuator_props.SFX_actions_index = (len(sfx_actions))

        if self.action == 'SAVE':
            bpy.ops.sfx.save_list('INVOKE_DEFAULT')          

        return {"FINISHED"}

    def update_fcurves(self, context, sfx_actions, index):
        try:
            print('Try',sfx_actions[index])
        except IndexError:
            sfx.actuators[context.active_node.name].Actuator_basic_props.Actuator_props.SFX_actions_index = 0
            index = 0
        try:
            print('Try',sfx_actions[index])
        except:
            print('Index Out of Range')
        else:
            Dataobject = bpy.data.objects[context.active_node.name+'_Connector']
            sfx.actuators[context.active_node.name].Actuator_basic_props.Actuator_props.simple_actuator_HardMin_prop = float(sfx_actions[index].minPos)
            sfx.actuators[context.active_node.name].Actuator_basic_props.Actuator_props.simple_actuator_HardMax_prop = float(sfx_actions[index].maxPos)
            sfx.actuators[context.active_node.name].Actuator_basic_props.Actuator_props.simple_actuator_AccMax_prop  = float(sfx_actions[index].maxAcc)
            sfx.actuators[context.active_node.name].Actuator_basic_props.Actuator_props.simple_actuator_VelMax_prop  = float(sfx_actions[index].maxVel)        
        try:
            Dataobject.driver_remove('["Jrk"]')
            Dataobject.driver_remove('["Acc"]')
            Dataobject.driver_remove('["Vel"]')
            Dataobject.driver_remove('["Pos"]')
        except:
             pass
        Jrkcurve = Dataobject.driver_add('["Jrk"]')
        try:
            Jrkcurve.modifiers.remove(Jrkcurve.modifiers[0])
        except IndexError:
            pass
        Acccurve = Dataobject.driver_add('["Acc"]')
        try:
            Acccurve.modifiers.remove(Acccurve.modifiers[0])
        except IndexError:
            pass
        Velcurve = Dataobject.driver_add('["Vel"]')
        try:
            Velcurve.modifiers.remove(Velcurve.modifiers[0])
        except IndexError:
            pass
        Poscurve = Dataobject.driver_add('["Pos"]')
        try:
            Poscurve.modifiers.remove(Poscurve.modifiers[0])
        except IndexError:
            pass
        J = json.loads(sfx_actions[index].Jrk)
        A = json.loads(sfx_actions[index].Acc)
        V = json.loads(sfx_actions[index].Vel)
        P = json.loads(sfx_actions[index].Pos)
        for i in range(0, len(J)):
            Jrkcurve.keyframe_points.insert( J[i][0] , J[i][1])
        for i in range(0, len(A)):
            Acccurve.keyframe_points.insert( A[i][0] , A[i][1]) 
        for i in range(0, len(V)):
            Velcurve.keyframe_points.insert( V[i][0] , V[i][1]) 
        for i in range(0, len(P)):
            Poscurve.keyframe_points.insert( P[i][0] , P[i][1])

        return

class SFX_OT_save_List(bpy.types.Operator):
    bl_idname = "sfx.save_list"
    bl_label = "Save Action"
    bl_description = "Save Action"

    def execute(self, context):        
        bpy.ops.sfx.save_action('INVOKE_DEFAULT')        
        return{'FINISHED'}


class SFX_OT_SelectOperator(bpy.types.Operator, ImportHelper):
    """This appears in the tooltip of the operator and in the generated docs"""
    bl_idname = "sfx.select_operator"
    bl_label = "Action Selector"
    bl_options = {'PRESET', 'UNDO'}

    # ImportHelper mixin class uses this
    filename_ext = ".sfxact"

    filter_glob : bpy.props.StringProperty(
            default="*.sfxact",
            options={'HIDDEN'},
            )

    # Selected files
    files : bpy.props.CollectionProperty(type=bpy.types.PropertyGroup)

    def execute(self, context):
        MotherNode = context.active_node
        sfx_actions       = sfx.actuators[MotherNode.name].Actuator_basic_props.Actuator_props.SFX_actions
        
        # get the folder
        folder = (os.path.dirname(self.filepath))

        # iterate through the selected files
        for i in self.files:
            # generate full path to file
            path_to_file = (os.path.join(folder, i.name))   
            item = sfx_actions.add()
            item.id = len(sfx_actions)
            item.name = i.name # assign name of selected object
            read_some_data(context, path_to_file, item)
        
        self.report({'INFO'}, "Files Added")
        return {'FINISHED'}

# custom list
class SFX_UL_List(UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        split = layout.split(factor = 0.7)
        split.prop(item, "name", text="", emboss=False, translate=False, icon='DRIVER')
        split.label(text="Index: %d" % (index))

    def invoke(self, context, event):
        pass

class SFX_OT_clear_List(bpy.types.Operator):
    bl_idname = "sfx.clear_list"
    bl_label = "Clear List"
    bl_description = "Clear all items in the list"

    def execute(self, context):
        MotherNode = context.active_node
        sfx_actions       = sfx.actuators[MotherNode.name].Actuator_basic_props.Actuator_props.SFX_actions

        if len(sfx_actions) > 1:
             # reverse range to remove last item first but keep first
            for i in range(len(sfx_actions)-1,0,-1):
                sfx_actions.remove(i)
        else:
            pass

        return{'FINISHED'}