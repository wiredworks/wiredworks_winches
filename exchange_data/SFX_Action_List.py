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
    item.id          = float(Data[0])
    item.name        = Data[1]
    item.saved       = bool(Data[2])
    item.path        = Data[3]
    item.minPos      = float(Data[4])
    item.maxPos      = float(Data[5])
    item.maxAcc      = float(Data[6])
    item.maxVel      = float(Data[7])
    item.length      = float(Data[8])
    item.Jrk         = Data[9]
    item.Acc         = Data[10]
    item.Vel         = Data[11]
    item.Pos         = Data[12]
    item.VP          = Data[13]
    item.description = Data[14]

    return {'FINISHED'}

class SFX_OT_list_actions(bpy.types.Operator):
    bl_idname = "sfx.list_action"
    bl_label = "List Action"

    action : bpy.props.EnumProperty(
        items=(
            ('NIX', 'Nix', ""),
            ('UP', "Up", ""),
            ('DOWN', "Down", ""),
            ('REMOVE', "Remove", ""),
            ('ADD', "Add", ""),
            ('SAVE', "Save", "")
            )
        )
    def invoke(self, context, event):
        MotherNode = context.active_node
        sfx_actions   = sfx.actuators[MotherNode.name].Actuator_basic_props.Actuator_props.SFX_actions
        if self.action == 'NIX':
            index = sfx.actuators[MotherNode.name].Actuator_basic_props.Actuator_props.SFX_actions_index
            self.update_fcurves(context, sfx_actions, index)
            return {'PASS_THROUGH'}
        try:
            item = sfx_actions[sfx.actuators[MotherNode.name].Actuator_basic_props.Actuator_props.SFX_actions_index]
        except IndexError:
            pass
        if self.action == 'REMOVE':
            if len(sfx.actuators[MotherNode.name].Actuator_basic_props.Actuator_props.SFX_actions) > 1:
                sfx_actions.remove(sfx.actuators[MotherNode.name].Actuator_basic_props.Actuator_props.SFX_actions_index)
                if sfx.actuators[MotherNode.name].Actuator_basic_props.Actuator_props.SFX_actions_index > 0:
                    sfx.actuators[MotherNode.name].Actuator_basic_props.Actuator_props.SFX_actions_index -= 1
                index = sfx.actuators[MotherNode.name].Actuator_basic_props.Actuator_props.SFX_actions_index
        if self.action == 'ADD':
            bpy.ops.sfx.select_operator('INVOKE_DEFAULT')            
            sfx.actuators[MotherNode.name].Actuator_basic_props.Actuator_props.SFX_actions_index = (len(sfx_actions)-1)
        if self.action == 'SAVE':
            bpy.ops.sfx.save_list('INVOKE_DEFAULT')          

        return {"FINISHED"}

    def update_fcurves(self, context, sfx_actions, index):
        try:
            IndexTest = sfx_actions[index]
        except IndexError:
            sfx.actuators[context.active_node.name].Actuator_basic_props.Actuator_props.SFX_actions_index = 0
            index = 0
        try:
            IndexTest =sfx_actions[index]
        except:
            info ='Index Out of Range'
            self.report({'INFO'}, info)
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
            Dataobject.driver_remove('["Pos"]')
            Dataobject.driver_remove('["Vel-Time"]')
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
        VPcurve = Dataobject.driver_add('["Vel-Time"]')
        try:
            VPcurve.modifiers.remove(VPcurve.modifiers[0])
        except IndexError:
            pass
        J  = json.loads(sfx_actions[index].Jrk)
        A  = json.loads(sfx_actions[index].Acc)
        V  = json.loads(sfx_actions[index].Vel)
        P  = json.loads(sfx_actions[index].Pos)
        VP = json.loads(sfx_actions[index].VP)
        for i in range(0, len(J[0])):
            Jrkcurve.keyframe_points.insert( J[0][i] , J[1][i], options =  {'FAST'})
        for i in range(0, len(A[0])):
            Acccurve.keyframe_points.insert( A[0][i] , A[1][i], options =  {'FAST'}) 
        for i in range(0, len(V[0])):
            Velcurve.keyframe_points.insert( V[0][i] , V[1][i], options =  {'FAST'}) 
        for i in range(0, len(P[0])):
            Poscurve.keyframe_points.insert(P[0][i] , P[1][i], options =  {'FAST'})
        for i in range(0, len(VP[0])):
            VPcurve.keyframe_points.insert( VP[0][i] , VP[1][i], options = {'FAST'})
        return

class SFX_OT_save_List(bpy.types.Operator):
    bl_idname = "sfx.save_list"
    bl_label = "Save Action"
    bl_description = "Save Action"

    description : bpy.props.StringProperty(name = 'Description',
                                 description = 'Describe the Charactristics of that Action',
                                 default = 'Default Description')

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

    description : bpy.props.StringProperty(name = 'Description',
                                            description = 'Describe the Charactristics of that Action',
                                            default = 'Default Description')


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
        split = layout.split(factor = 0.95)
        split.prop(item, "description", text="", emboss=False, translate=False, icon='DRIVER')
        if item.saved == False:
            split.label(text='', icon ='CHECKBOX_DEHLT')
        else:
            split.label(text='', icon ='CHECKBOX_HLT')           
            

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
            sfx.actuators[MotherNode.name].Actuator_basic_props.Actuator_props.SFX_actions_index = 0
        else:
            pass
        return{'FINISHED'}