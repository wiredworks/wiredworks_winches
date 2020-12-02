import bpy
import json

from ..exchange_data.sfx import sfx

from .. SFX_Helpers.SFX_Calc_Default_Move import SFX_Calc_Default_Move

class SFX_OT_MaxVel_update(bpy.types.Operator):  
    bl_idname = "sfx.maxvel_update"
    bl_label = "Update Max Vel"

    def invoke(self, context, event):
        VelMax      = sfx.actuators[context.active_node.name].Actuator_basic_props.Actuator_props.simple_actuator_VelMax_prop
        ActionIndex = sfx.actuators[context.active_node.name].Actuator_basic_props.Actuator_props.SFX_actions_index
        Actions     = sfx.actuators[context.active_node.name].Actuator_basic_props.Actuator_props.SFX_actions
        VelMaxOld  = Actions[ActionIndex].maxVel 
        if VelMax != VelMaxOld:
            action0 = sfx.actuators[context.active_node.name].Actuator_basic_props.Actuator_props.SFX_actions.add()
            action0.id = len(sfx.actuators[context.active_node.name].Actuator_basic_props.Actuator_props.SFX_actions)
            action0.name = context.active_node.name+'_'+str(action0.id)+'_mod.sfxact'

            self.mod_action(context, context.active_node.name, action0)
            sfx.actuators[context.active_node.name].Actuator_basic_props.Actuator_props.SFX_actions_index =\
                len(sfx.actuators[context.active_node.name].Actuator_basic_props.Actuator_props.SFX_actions)-1 

        return {"FINISHED"}

    def mod_action(self, context, name, action0):

        Dataobject = bpy.data.objects[name+'_Connector']
        action0.minPos = sfx.actuators[name].Actuator_basic_props.Actuator_props.simple_actuator_HardMin_prop
        action0.maxPos = sfx.actuators[name].Actuator_basic_props.Actuator_props.simple_actuator_HardMax_prop
        action0.length = action0.maxPos - action0.minPos
        action0.maxAcc = sfx.actuators[name].Actuator_basic_props.Actuator_props.simple_actuator_AccMax_prop
        action0.maxVel = sfx.actuators[name].Actuator_basic_props.Actuator_props.simple_actuator_VelMax_prop

        ret = self.DefaultMove = SFX_Calc_Default_Move(Dataobject, action0.length, action0.maxAcc, action0.maxVel )

        Jrk_Data =[]
        for i in range(0,len(bpy.data.objects[name+'_Connector'].animation_data.drivers[0].keyframe_points)):
            Jrk_Data.append((bpy.data.objects[name+'_Connector'].animation_data.drivers[0].keyframe_points[i].co[0],
            bpy.data.objects[name+'_Connector'].animation_data.drivers[0].keyframe_points[i].co[1]))
        Acc_Data =[]
        for i in range(0,len(bpy.data.objects[name+'_Connector'].animation_data.drivers[1].keyframe_points)):
            Acc_Data.append((bpy.data.objects[name+'_Connector'].animation_data.drivers[1].keyframe_points[i].co[0],
            bpy.data.objects[name+'_Connector'].animation_data.drivers[1].keyframe_points[i].co[1]))
        Vel_Data =[]
        for i in range(0,len(bpy.data.objects[name+'_Connector'].animation_data.drivers[2].keyframe_points)):
            Vel_Data.append((bpy.data.objects[name+'_Connector'].animation_data.drivers[2].keyframe_points[i].co[0],
            bpy.data.objects[name+'_Connector'].animation_data.drivers[2].keyframe_points[i].co[1]))
        Pos_Data =[]
        for i in range(0,len(bpy.data.objects[name+'_Connector'].animation_data.drivers[3].keyframe_points)):
            Pos_Data.append((bpy.data.objects[name+'_Connector'].animation_data.drivers[3].keyframe_points[i].co[0],
            bpy.data.objects[name+'_Connector'].animation_data.drivers[3].keyframe_points[i].co[1]))

        action0.Jrk = json.dumps(Jrk_Data)
        action0.Acc = json.dumps(Acc_Data)
        action0.Vel = json.dumps(Vel_Data)
        action0.Pos = json.dumps(Pos_Data)