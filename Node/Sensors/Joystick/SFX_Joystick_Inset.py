import bpy

class SFX_Joystick_Inset(bpy.types.PropertyGroup):
    bl_idname = "SFX_Joystick_Inset"

    def update_func(self,context):
        pass

    X_Achse : bpy.props.FloatProperty(name = "X-Achse",
                                    description = "X-Achse",
                                    precision = 3,
                                    default = 0.001)
    Y_Achse : bpy.props.FloatProperty(name = "Y-Achse",
                                    description = "Y-Achse",
                                    precision = 3,
                                    default = 0.001)
    Z_Achse : bpy.props.FloatProperty(name = "Z-Achse",
                                    description = "Z-Achse",
                                    precision = 3,
                                    default = 0.001)
    X_Rot : bpy.props.FloatProperty(name = "X-Rot",
                                    description = "X-Rot",
                                    precision = 3,
                                    default = 0.001)
    Y_Rot : bpy.props.FloatProperty(name = "Y-Rot",
                                    description = "Y-Rot",
                                    precision = 3,
                                    default = 0.001)
    Z_Rot : bpy.props.FloatProperty(name = "Z-Rot",
                                    description = "Z-Rot",
                                    precision = 3,
                                    default = 0.001)
    Slider : bpy.props.FloatProperty(name = "Z-Rot",
                                    description = "Z-Rot",
                                    precision = 3,
                                    default = 0.001)
    Button1 : bpy.props.BoolProperty(name = "Button 1",
                                    description = "Button 1",
                                    default = 0)
    Button2 : bpy.props.BoolProperty(name = "Button 1",
                                    description = "Button 1",
                                    default = 0)
    Button3 : bpy.props.BoolProperty(name = "Button 1",
                                    description = "Button 1",
                                    default = 0)
    Button4 : bpy.props.BoolProperty(name = "Button 1",
                                    description = "Button 1",
                                    default = 0)
    Button5 : bpy.props.BoolProperty(name = "Button 1",
                                    description = "Button 1",
                                    default = 0)
    Button6 : bpy.props.BoolProperty(name = "Button 1",
                                    description = "Button 1",
                                    default = 0)
    Button7 : bpy.props.BoolProperty(name = "Button 1",
                                    description = "Button 1",
                                    default = 0)
    Button8 : bpy.props.BoolProperty(name = "Button 1",
                                    description = "Button 1",
                                    default = 0)
    Button9 : bpy.props.BoolProperty(name = "Button 1",
                                    description = "Button 1",
                                    default = 0)
    Button10: bpy.props.BoolProperty(name = "Button 1",
                                    description = "Button 1",
                                    default = 0)
    Button11: bpy.props.BoolProperty(name = "Button 1",
                                    description = "Button 1",
                                    default = 0)
    Button12: bpy.props.BoolProperty(name = "Button 1",
                                    description = "Button 1",
                                    default = 0)                                                                                                                                                                                                                                                                                                                                                                                                            
    HAT_Switch : bpy.props.IntProperty(name = "HAT-Switch",
                                    description = "Hat-Switch",
                                    default = 0)

    def draw_Joystick_props(self, context, layout):
        box = layout.box()
        row = box.row()
        row.label(text='Joystick Data')        

        split = box.split()
        col = split.column()        
        col.prop(self, 'X_Achse'    , text = 'X-Achse') 
        col.prop(self, 'Y_Achse'    , text = 'Y-Achse')
        col.prop(self, 'Z_Achse'    , text = 'Z-Achse')
        col.prop(self, 'X_Rot'      , text = 'X-Rot')
        col.prop(self, 'Y_Rot'      , text = 'X-Rot')
        col.prop(self, 'Z_Rot'      , text = 'X-Rot')
        col.prop(self, 'HAT_Switch' , text = 'HAT')

        row = box.row()
        row.prop(self,'Button1',  text = '')
        row.prop(self,'Button2',  text = '')
        row.prop(self,'Button3',  text = '')
        row.prop(self,'Button4',  text = '')
        row.prop(self,'Button5',  text = '')
        row.prop(self,'Button6',  text = '')
        row.prop(self,'Button7',  text = '')
        row.prop(self,'Button8',  text = '')
        row.prop(self,'Button9',  text = '')
        row.prop(self,'Button10', text = '')
        row.prop(self,'Button11', text = '')
        row.prop(self,'Button12', text = '')