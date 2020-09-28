import bpy

class SFX_ClockNode(bpy.types.Node):
    '''SFX_ClockNode'''
    bl_idname = 'SFX_ClockNode'
    bl_label = 'Clock'
    bl_icon = 'CURVE_NCIRCLE'
    bl_width_min = 340
    bl_width_max = 340

    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname == 'SFX_NodeTree'

    def update_value(self,context):
        self.update()
        pass

    operator_started_bit1 : bpy.props.BoolProperty(name = "Operator Started",
                                    description = "Operator Started",
                                    default = False)
    date :bpy.props.StringProperty(name='Date',
                                description='Date',
                                default = 'Sun Jun 20 23:21:05 1993')

    TickTime_prop: bpy.props.FloatProperty(name = "Tick Time",
                                    description ="Sanity Check message round trip Time",
                                    default=0.1,
                                    precision=1,
                                    update = update_value)

    def init(self, context):
        self.draw_model(context)
        pass

    def copy(self, node):
        print("copied node", node)

    def free(self):
        self.operator_started_bit1 = False
        print('Node destroyed',self)

    def draw_buttons(self, context, layout):
        box = layout.box()
        col = box.column(align = True)
        row = col.split(factor = 0.3)
        if not(self.operator_started_bit1):
            row.operator('sfx.clockstartop',text ='Start')
        else:
           row.operator('sfx.commstarteddiag',text ='Started')
        row1 = row.split(factor = 0.75) 
        row1.prop(self,'date',text = '')
        row2 = row1.split(factor = 1)
        row2.prop( self, 'TickTime_prop', text = '')


    def draw_buttons_ext(self, context, layout):
        pass

    def draw_model(self,context):
        collection = bpy.data.collections.new('ww SFX_Nodes')
        bpy.context.scene.collection.children.link(collection)

    def update(self):
        pass