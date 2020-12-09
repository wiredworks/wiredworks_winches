import bpy

def drawMenu(self, context):
    if context.space_data.tree_type != "SFX_NodeTree": return

    layout = self.layout
    layout.operator_context = "INVOKE_DEFAULT"

    layout.operator('sfx.clock_in', text = 'Clock', icon = "CURVE_NCIRCLE" )

    layout.menu("SFX_MT_sensors_menu", text= "Sensors", icon = "IMPORT")
    layout.menu("SFX_MT_cues_menu", text= "Cues", icon = "STROKE")
    layout.menu("SFX_MT_kinematics_menu", text= "Kinematics", icon = "SPHERECURVE")
    layout.menu("SFX_MT_helpers_menu", text= "Helpers", icon = "GHOST_DISABLED")
    layout.menu("SFX_MT_actuator_menu", text= "Actuators", icon = "EXPORT")


class SFX_SensorsMenu(bpy.types.Menu):
    bl_idname = "SFX_MT_sensors_menu"
    bl_label = "Sensors Menu"

    def draw(self,context):
        layout = self.layout
        layout.operator('sfx.joystick_in',text = 'Joystick', icon='ARROW_LEFTRIGHT')

class SFX_CuesMenu(bpy.types.Menu):
    bl_idname = "SFX_MT_cues_menu"
    bl_label = "Cues Menu"
    def draw(self,context):
        layout = self.layout
        layout.operator('sfx.simplecue_in',text = 'simple Cue', icon='ARROW_LEFTRIGHT')
        layout.operator('sfx.secondcue_in',text = 'second Cue', icon='ARROW_LEFTRIGHT')

class SFX_KinematicsMenu(bpy.types.Menu):
    bl_idname = "SFX_MT_kinematics_menu"
    bl_label = "Kinematics Menu"
    def draw(self,context):
        layout = self.layout
        pass

class SFX_HelpersMenu(bpy.types.Menu):
    bl_idname = "SFX_MT_helpers_menu"
    bl_label = "Helper Menu"
    def draw(self,context):
        layout = self.layout
        layout.operator('sfx.joydemux_in',text = 'Demux', icon='TRACKING_FORWARDS')
        layout.operator('sfx.mixer_in',text = 'Mixer', icon='SNAP_MIDPOINT')
        layout.operator('sfx.adder_in',text = 'Adder', icon='FULLSCREEN_EXIT')

class SFX_ActMenu(bpy.types.Menu):
    bl_idname = "SFX_MT_actuator_menu"
    bl_label = "Actuator Menu"

    def draw(self,context):
        layout = self.layout
        layout.menu("SFX_MT_actuatorLin_menu", text= "Linear", icon = "EXPORT")
        layout.menu("SFX_MT_actuatorRot_menu", text= "Rotational", icon = "EXPORT")

class SFX_ActRotMenu(bpy.types.Menu):
    bl_idname = "SFX_MT_actuatorRot_menu"
    bl_label = "Rotatianal Menu"

    def draw(self,context):
        layout = self.layout
        layout.operator('sfx.simplerot_in',text = 'Rotation', icon='MESH_CIRCLE')

class SFX_ActLinMenu(bpy.types.Menu):
    bl_idname = "SFX_MT_actuatorLin_menu"
    bl_label = "Linear Menu"

    def draw(self,context):
        layout = self.layout
        layout.operator('sfx.telescope_in',text = 'Telescope', icon='ARROW_LEFTRIGHT')
        layout.operator('sfx.simplelin_in',text = 'Linear', icon='ARROW_LEFTRIGHT')     
        layout.operator('sfx.linrail_in',text = 'Rail', icon='ARROW_LEFTRIGHT')        


def insertNode(layout, type, text, settings = {}, icon = "NONE"):
    operator = layout.operator("node.add_node", text = text, icon = icon)
    operator.type = type
    operator.use_transform = True
    for name, value in settings.items():
        item = operator.settings.add()
        item.name = name
        item.value = value
    return operator

def register():
    bpy.types.NODE_MT_add.append(drawMenu)

def unregister():
    bpy.types.NODE_MT_add.remove(drawMenu)
