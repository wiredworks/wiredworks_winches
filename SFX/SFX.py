import bpy

class SFX:
    class Comm():
        Type : bpy.props.StringProperty(name        = "Type",
                                        description = "Type of Communication",
                                        default     = "UDP")
        class Adress():
            Name : bpy.props.StringProperty(name        = "Name",
                                            description = "Name of Communication",
                                            default     = "Anton")
            IP   : bpy.props.StringProperty(name        = "IP",
                                            description = "IP of Communication",
                                            default     = "127.0.0.1")
            Send_Port : bpy.props.StringProperty(name        = "Send Port",
                                            description = "Send Port of Communication",
                                            default     = "15022")
            Rec_Port : bpy.props.StringProperty(name        = "Send Port",
                                            description = "Send Port of Communication",
                                            default     = "15022")
        valid  : bpy.props.BoolProperty(name        = "valid",
                                        description = "Data is valid",
                                        default     = False)
        TickTime_prop: bpy.props.FloatProperty(name = "Tick Time",
                                description         ="Sanity Check message round trip Time",
                                default             =0.1,
                                precision           =1)
        In_Msg : bpy.props.StringProperty(name      = "In Message",
                                        description = "Message from Act to Blender",
                                        default     = "")
        Out_Msg : bpy.props.StringProperty(name      = "In Message",
                                        description = "Message from Act to Blender",
                                        default     = "")
    class Act():
        class Attr():
            Max: bpy.props.FloatProperty(name = "Tick Time",
                                description         ="Sanity Check message round trip Time",
                                default             =0.1,
                                precision           =1)
            Min: bpy.props.FloatProperty(name = "Tick Time",
                                description         ="Sanity Check message round trip Time",
                                default             =0.1,
                                precision           =1)
            Set: bpy.props.FloatProperty(name = "Tick Time",
                                description         ="Sanity Check message round trip Time",
                                default             =0.1,
                                precision           =1)
            Ist: bpy.props.FloatProperty(name = "Tick Time",
                                description         ="Sanity Check message round trip Time",
                                default             =0.1,
                                precision           =1)
            Controller : bpy.props.StringProperty(name = "Controler",
                                description         = "Controler",
                                default             = "")
            def Attr_draw(self,context,layout):
                box1 = layout.box()
                row = box1.row()
                row.label(text = 'Min')
                row.prop(self,'Min', text='')
                row.label(text = 'Max')
                row.prop(self,'Max', text='')
                row.label(text = 'Set')
                row.prop(self,'Set', text='')
                row.label(text = 'Ist')
                row.prop(self,'Ist', text='')

        class Acc(Attr):
            def draw(self,context,layout):
                box = layout.box()
                row = box.row()
                row.label(text='Acc')
                row = box.row()
                Attr_draw(self,context,row)
        class Vel(Attr):
            def draw(self,context,layout):
                box = layout.box()
                row = box.row()
                row.label(text='Vel')
                row = box.row()
                Attr_draw(self,context,row)
        class Pos(Attr):
            Length: bpy.props.FloatProperty(name = "Length",
                            description         ="Length of Path",
                            default             =0.1,
                            precision           =1)                
            def draw(self,context,layout):
                box = layout.box()
                row = box.row()
                row.label(text='Vel')
                row.prop(self,'Length',text='')
                row = box.row()
                Attr_draw(self,context,row)
