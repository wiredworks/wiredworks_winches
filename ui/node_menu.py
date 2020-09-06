import bpy

def drawMenu(self, context):
    if context.space_data.tree_type != "ww_NodeTree": return

    layout = self.layout
    layout.operator_context = "INVOKE_DEFAULT"

    layout.menu("WW_MT_actuator_menu", text= "Actuator", icon = "CON_TRANSFORM")

class ActuatorMenu(bpy.types.Menu):
    bl_idname = "WW_MT_actuator_menu"
    bl_label = "Actuator Menu"

    def draw(self,context):
        layout = self.layout
        insertNode(layout, "ww_ActuatorLin", "Linear",{},"ARROW_LEFTRIGHT")
        insertNode(layout, "ww_ActuatorRot", "Rotational",{},"PROP_CON")


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
