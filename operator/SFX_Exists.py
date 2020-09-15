import bpy

class SFX_Exists(bpy.types.Operator):
    ''' If not ww SFX_Nodes collectionEnabeles Dialog '''
    bl_idname = "ww.sfxexists"
    bl_label = "SFX Exists"

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def draw(self,context):
        self.layout.label(text='You have to have a ww SFX_Node collection ')
        self.layout.label(text='please remove this node')