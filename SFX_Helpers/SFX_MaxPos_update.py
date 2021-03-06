import bpy
import json

from ..exchange_data.sfx import sfx

from .. SFX_Helpers.SFX_Calc_Default_Move import SFX_Calc_Default_Move

class SFX_OT_MaxPos_update(bpy.types.Operator):
    bl_idname = "sfx.maxpos_update"
    bl_label = "Update Max Pos"

    def invoke(self, context, event):
        if context.active_node.sfx_type == 'Actuator':
            HardMax     = sfx.actuators[context.active_node.name].Actuator_basic_props.Actuator_props.simple_actuator_HardMax_prop
            ActionIndex = sfx.actuators[context.active_node.name].Actuator_basic_props.Actuator_props.SFX_actions_index
            Actions     = sfx.actuators[context.active_node.name].Actuator_basic_props.Actuator_props.SFX_actions
            Length      = sfx.actuators[context.active_node.name].Actuator_basic_props.Actuator_props.simple_actuator_HardMax_prop-\
                        sfx.actuators[context.active_node.name].Actuator_basic_props.Actuator_props.simple_actuator_HardMin_prop
            LengthOld   = Actions[ActionIndex].length
            HardMaxOld  = Actions[ActionIndex].maxPos
            sfx.actuators[context.active_node.name].Actuator_basic_props.DigTwin_basic_props.length = Length
        
            if HardMax != HardMaxOld and Length != LengthOld:
                action0 = sfx.actuators[context.active_node.name].Actuator_basic_props.Actuator_props.SFX_actions.add()
                action0.id = len(sfx.actuators[context.active_node.name].Actuator_basic_props.Actuator_props.SFX_actions)
                action0.name = context.active_node.name+'_'+str(action0.id)+'_mod.sfxact'
                self.mod_action(context, context.active_node.name, action0)
                sfx.actuators[context.active_node.name].Actuator_basic_props.Actuator_props.SFX_actions_index =\
                    len(sfx.actuators[context.active_node.name].Actuator_basic_props.Actuator_props.SFX_actions)-1

        elif context.active_node.sfx_type == 'Cue':
            HardMax     = sfx.cues[context.active_node.name].Actuator_props.simple_actuator_HardMax_prop
            ActionIndex = sfx.cues[context.active_node.name].Actuator_props.SFX_actions_index
            Actions     = sfx.cues[context.active_node.name].Actuator_props.SFX_actions
            Length      = sfx.cues[context.active_node.name].Actuator_props.simple_actuator_HardMax_prop-\
                        sfx.cues[context.active_node.name].Actuator_props.simple_actuator_HardMin_prop
            LengthOld   = Actions[ActionIndex].length
            HardMaxOld  = Actions[ActionIndex].maxPos

            if HardMax != HardMaxOld and Length != LengthOld:
                action0 = sfx.cues[context.active_node.name].Actuator_props.SFX_actions.add()
                action0.id = len(sfx.cues[context.active_node.name].Actuator_props.SFX_actions)
                action0.name = context.active_node.name+'_'+str(action0.id)+'_mod.sfxact'
                self.mod_action(context, context.active_node.name, action0)
                sfx.cues[context.active_node.name].Actuator_props.SFX_actions_index =\
                    len(sfx.cues[context.active_node.name].Actuator_props.SFX_actions)-1

        return {"FINISHED"}

    def mod_action(self, context, name, action0):
        if context.active_node.sfx_type == 'Actuator':
            action0.minPos = sfx.actuators[name].Actuator_basic_props.Actuator_props.simple_actuator_HardMin_prop
            action0.maxPos = sfx.actuators[name].Actuator_basic_props.Actuator_props.simple_actuator_HardMax_prop
            action0.length = action0.maxPos - action0.minPos
            action0.maxAcc = sfx.actuators[name].Actuator_basic_props.Actuator_props.simple_actuator_AccMax_prop
            action0.maxVel = sfx.actuators[name].Actuator_basic_props.Actuator_props.simple_actuator_VelMax_prop

            A = SFX_Calc_Default_Move(action0.length, action0.maxAcc, action0.maxVel )
            Jrk_Data,Acc_Data,Vel_Data,Pos_Data,Vel_Pos_Data = SFX_Calc_Default_Move.out(A)
    
            sfx.actuators[name].Actuator_basic_props.Actuator_props.simple_actuator_Time_prop = Jrk_Data[0][-1]
            action0.duration = sfx.actuators[name].Actuator_basic_props.Actuator_props.simple_actuator_Time_prop

        elif context.active_node.sfx_type == 'Cue':
            action0.minPos = sfx.cues[name].Actuator_props.simple_actuator_HardMin_prop
            action0.maxPos = sfx.cues[name].Actuator_props.simple_actuator_HardMax_prop
            action0.length = action0.maxPos - action0.minPos
            action0.maxAcc = sfx.cues[name].Actuator_props.simple_actuator_AccMax_prop
            action0.maxVel = sfx.cues[name].Actuator_props.simple_actuator_VelMax_prop

            A = SFX_Calc_Default_Move(action0.length, action0.maxAcc, action0.maxVel )
            Jrk_Data,Acc_Data,Vel_Data,Pos_Data,Vel_Pos_Data = SFX_Calc_Default_Move.out(A)
    
            sfx.cues[name].Actuator_props.simple_actuator_Time_prop = Jrk_Data[0][-1] 
            action0.duration = sfx.cues[name].Actuator_props.simple_actuator_Time_prop         

        action0.Jrk = json.dumps(Jrk_Data)
        action0.Acc = json.dumps(Acc_Data)
        action0.Vel = json.dumps(Vel_Data)
        action0.Pos = json.dumps(Pos_Data)
        action0.VP  = json.dumps(Vel_Pos_Data) 