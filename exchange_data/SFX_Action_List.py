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
    data = json.loads(data)
    Data = data.split(';')
    item.id          = float(Data[0])
    item.name        = Data[1]
    item.saved       = bool(Data[2])
    item.path        = Data[3]
    item.description = Data[4]
    item.signed      = bool(Data[5])
    item.maxAcc      = float(Data[6])
    item.maxVel      = float(Data[7])
    item.minPos      = float(Data[8])
    item.maxPos      = float(Data[9])
    item.length      = float(Data[10])
    item.Duration    = float(Data[11])
    item.Pos_SM      = Data[12]   
    item.Jrk         = Data[13] 
    item.Acc         = Data[14] 
    item.Vel         = Data[15]
    item.Pos         = Data[16] 
    item.VP          = Data[17] 

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
        if MotherNode.sfx_type == 'Actuator':
            sfx_actions   = sfx.actuators[MotherNode.name].Actuator_basic_props.Actuator_props.SFX_actions
            if self.action == 'NIX':
                index = sfx.actuators[MotherNode.name].Actuator_basic_props.Actuator_props.SFX_actions_index
                self.update_fcurves(context, sfx_actions, index, MotherNode.sfx_type)
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

        elif MotherNode.sfx_type == 'Cue':
            sfx_actions   = sfx.cues[MotherNode.name].Actuator_props.SFX_actions
            if self.action == 'NIX':
                index = sfx.cues[MotherNode.name].Actuator_props.SFX_actions_index
                self.update_fcurves(context, sfx_actions, index, MotherNode.sfx_type)
                return {'PASS_THROUGH'}
            try:
                item = sfx_actions[sfx.cues[MotherNode.name].Actuator_props.SFX_actions_index]
            except IndexError:
                pass
            if self.action == 'REMOVE':
                if len(sfx.cues[MotherNode.name].Actuator_props.SFX_actions) > 1:
                    sfx_actions.remove(sfx.cues[MotherNode.name].Actuator_props.SFX_actions_index)
                    if sfx.cues[MotherNode.name].Actuator_props.SFX_actions_index > 0:
                        sfx.cues[MotherNode.name].Actuator_props.SFX_actions_index -= 1
                    index = sfx.cues[MotherNode.name].Actuator_props.SFX_actions_index
            if self.action == 'ADD':
                bpy.ops.sfx.select_operator('INVOKE_DEFAULT')            
                sfx.cues[MotherNode.name].Actuator_props.SFX_actions_index = (len(sfx_actions)-1)
            if self.action == 'SAVE':
                bpy.ops.sfx.save_list('INVOKE_DEFAULT')                 

        return {"FINISHED"}

    def update_fcurves(self, context, sfx_actions, index, Nodetype):
        try:
            IndexTest = sfx_actions[index]
        except IndexError:
            if Nodetype == 'Actuator':
                sfx.actuators[context.active_node.name].Actuator_basic_props.Actuator_props.SFX_actions_index = 0
            elif Nodetype == 'Cue':
                sfx.cues[context.active_node.name].Actuator_basic_props.Actuator_props.SFX_actions_index = 0
            index = 0
        try:
            IndexTest =sfx_actions[index]
        except:
            info ='Index Out of Range'
            self.report({'INFO'}, info)
        else:
            if Nodetype == 'Actuator':
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
                Jrk  = json.loads(sfx_actions[index].Jrk)
                Acc  = json.loads(sfx_actions[index].Acc)
                Vel  = json.loads(sfx_actions[index].Vel)
                Pos  = json.loads(sfx_actions[index].Pos)
                VP   = json.loads(sfx_actions[index].VP)

                sfx.actuators[context.active_node.name].Actuator_basic_props.Actuator_props.simple_actuator_Time_prop = Jrk[0][-1]

                Jrkcurve.keyframe_points.insert(0,0) 
                for i in range(0,len(Jrk[0])):
                    if Jrk[0][i]>0.01:
                        A=Jrkcurve.keyframe_points.insert(Jrk[0][i],Jrk[1][i], options =  {'FAST'}) 
                        A.interpolation = 'LINEAR'
                Acccurve.keyframe_points.insert(0,0)
                for i in range(0,len(Acc[0])):
                    if Acc[0][i]>0.01:
                        A=Acccurve.keyframe_points.insert(Acc[0][i],Acc[1][i], options =  {'FAST'}) 
                        A.interpolation = 'LINEAR'
                Velcurve.keyframe_points.insert(0,0)
                for i in range(0,len(Vel[0])):
                    if Vel[0][i]>0.01:
                        A=Velcurve.keyframe_points.insert(Vel[0][i],Vel[1][i], options =  {'FAST'}) 
                        A.interpolation = 'LINEAR'
                Poscurve.keyframe_points.insert(0,0)
                for i in range(0,len(Pos[0])):
                    if Pos[0][i]>0.01:
                        A=Poscurve.keyframe_points.insert(Pos[0][i],Pos[1][i], options =  {'FAST'}) 
                        A.interpolation = 'LINEAR'
                VPcurve.keyframe_points.insert(0,0)         
                for i in range(0,len(VP[0])):
                    if VP[0][i]>0.01:
                        A=VPcurve.keyframe_points.insert(VP[0][i],VP[1][i], options =  {'FAST'}) 
                        A.interpolation = 'LINEAR'

                # VPcurve.keyframe_points[-1].handle_right = (VPcurve.keyframe_points[-1].co[0],-5)
                # VPcurve.keyframe_points[-1].handle_left  = (VPcurve.keyframe_points[-1].co[0],VPcurve.keyframe_points[-2].co[1]/3.0)
                try:
                    VPcurve.keyframe_points[0].handle_right = (VPcurve.keyframe_points[0].co[0],VPcurve.keyframe_points[1].co[1]/2.0)
                    VPcurve.keyframe_points[0].handle_left  = (VPcurve.keyframe_points[0].co[0],-5)
                except IndexError:
                    pass
                return
            elif Nodetype == 'Cue':
                Dataobject = bpy.data.objects[context.active_node.name+'_Data']
                sfx.cues[context.active_node.name].Actuator_props.simple_actuator_HardMin_prop = float(sfx_actions[index].minPos)
                sfx.cues[context.active_node.name].Actuator_props.simple_actuator_HardMax_prop = float(sfx_actions[index].maxPos)
                sfx.cues[context.active_node.name].Actuator_props.simple_actuator_AccMax_prop  = float(sfx_actions[index].maxAcc)
                sfx.cues[context.active_node.name].Actuator_props.simple_actuator_VelMax_prop  = float(sfx_actions[index].maxVel)
                for i in range(0,len(Dataobject.animation_data.action.fcurves)):
                    Dataobject.animation_data.action.fcurves.remove(Dataobject.animation_data.action.fcurves[0])
                # Dataobject.animation_data.action.fcurves.remove(Dataobject.animation_data.action.fcurves[1])
                # Dataobject.animation_data.action.fcurves.remove(Dataobject.animation_data.action.fcurves[2])
                # Dataobject.animation_data.action.fcurves.remove(Dataobject.animation_data.action.fcurves[3])
                # Dataobject.animation_data.action.fcurves.remove(Dataobject.animation_data.action.fcurves[4])
                try:
                    JrkInTime = Dataobject.animation_data.action.fcurves.new('Jrk')
                    JrkInTime.lock = True
                except RuntimeError:
                    print('Runtime Error')
                try:
                    AccInTime = Dataobject.animation_data.action.fcurves.new('Acc')
                    AccInTime.lock = True
                except RuntimeError:
                    print('Runtime Error')
                try:
                    VelInTime = Dataobject.animation_data.action.fcurves.new('Vel')
                    VelInTime.lock = True
                except RuntimeError:
                    print('Runtime Error') 
                try:
                    PosInTime = Dataobject.animation_data.action.fcurves.new('Pos')
                except RuntimeError:
                    print('Runntime Error')
                try:
                    VelPos    = Dataobject.animation_data.action.fcurves.new('PosTime')
                except RuntimeError:
                    print('Runntime Error')

                Jrk  = json.loads(sfx_actions[index].Jrk)
                Acc  = json.loads(sfx_actions[index].Acc)
                Vel  = json.loads(sfx_actions[index].Vel)
                Pos  = json.loads(sfx_actions[index].Pos)
                VP   = json.loads(sfx_actions[index].VP)

                sfx.cues[context.active_node.name].Actuator_props.simple_actuator_Time_prop = Jrk[0][-1]

                JrkInTime.keyframe_points.insert(0,0) 
                for i in range(0,len(Jrk[0])):
                    if Jrk[0][i]>0.01:
                        A=JrkInTime.keyframe_points.insert(Jrk[0][i],Jrk[1][i], options =  {'FAST'}) 
                        A.interpolation = 'LINEAR'
                AccInTime.keyframe_points.insert(0,0)
                for i in range(0,len(Acc[0])):
                    if Acc[0][i]>0.01:
                        A=AccInTime.keyframe_points.insert(Acc[0][i],Acc[1][i], options =  {'FAST'}) 
                        A.interpolation = 'LINEAR'
                VelInTime.keyframe_points.insert(0,0)
                for i in range(0,len(Vel[0])):
                    if Vel[0][i]>0.01:
                        A=VelInTime.keyframe_points.insert(Vel[0][i],Vel[1][i], options =  {'FAST'}) 
                        A.interpolation = 'LINEAR'
                PosInTime.keyframe_points.insert(0,0)
                for i in range(0,len(Pos[0])):
                    if Pos[0][i]>0.01:
                        A=PosInTime.keyframe_points.insert(Pos[0][i],Pos[1][i], options =  {'FAST'}) 
                        A.interpolation = 'LINEAR'
                VelPos.keyframe_points.insert(0,0)         
                for i in range(0,len(VP[0])):
                    if VP[0][i]>0.01:
                        A=VelPos.keyframe_points.insert(VP[0][i],VP[1][i], options =  {'FAST'}) 
                        A.interpolation = 'LINEAR'

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
        if MotherNode.sfx_type == 'Action':
            sfx_actions       = sfx.actuators[MotherNode.name].Actuator_basic_props.Actuator_props.SFX_actions
        elif MotherNode.sfx_type == 'Cue':
            sfx_actions       = sfx.cues[MotherNode.name].Actuator_props.SFX_actions
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
        split1 = layout.split(factor = 0.5)
        if item.signed == False:
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
        if MotherNode.sfx_type == 'Action':
            sfx_actions       = sfx.actuators[MotherNode.name].Actuator_basic_props.Actuator_props.SFX_actions
            if len(sfx_actions) > 1:
                # reverse range to remove last item first but keep first
                for i in range(len(sfx_actions)-1,0,-1):
                    sfx_actions.remove(i)
                sfx.actuators[MotherNode.name].Actuator_basic_props.Actuator_props.SFX_actions_index = 0
            else:
                pass
        elif MotherNode.sfx_type == 'Cue':
            sfx_actions       = sfx.cues[MotherNode.name].Actuator_props.SFX_actions
            if len(sfx_actions) > 1:
                # reverse range to remove last item first but keep first
                for i in range(len(sfx_actions)-1,0,-1):
                    sfx_actions.remove(i)
                sfx.actuators[MotherNode.name].Actuator_props.SFX_actions_index = 0            
        return{'FINISHED'}