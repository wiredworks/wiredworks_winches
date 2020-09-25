import bpy

def drawMenu(self, context):
    if context.space_data.tree_type != "SFX_NodeTree": return

    layout = self.layout
    layout.operator_context = "INVOKE_DEFAULT"

    layout.menu("SFX_MT_actuator_menu", text= "Actuator", icon = "CON_TRANSFORM")

class SFX_ActMenu(bpy.types.Menu):
    bl_idname = "SFX_MT_actuator_menu"
    bl_label = "Actuator Menu"

    def draw(self,context):
        layout = self.layout
        insertNode(layout, "SFX_JoyStartNode", "Start", {}, "CURVE_NCIRCLE")
        insertNode(layout, "SFX_JoyDemuxNode", "Demux", {}, "TRACKING_FORWARDS")
        insertNode(layout, "SFX_LinRailNode",  "Rail",  {}, "ARROW_LEFTRIGHT")

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
