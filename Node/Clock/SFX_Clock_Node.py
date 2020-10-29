import bpy

from ... exchange_data.sfx import sfx
from ... exchange_data.sfx import sfx_clock

class SFX_Clock_Node(bpy.types.Node):
    '''SFX_ClockNode'''
    bl_idname = 'SFX_Clock_Node'
    bl_label = 'clock'
    bl_icon = 'CURVE_NCIRCLE'
    bl_width_min = 340
    bl_width_max = 340

    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname == 'SFX_NodeTree'

    sfx       : bpy.props.PointerProperty(type = sfx)
    sfx_clock : bpy.props.PointerProperty(type = sfx_clock)

    def init(self, context):
        self.draw_model(context)
        self.init_sfxData()
        pass

    def copy(self, node):
        print("copied node", node)

    def free(self):
        sfx.clocks[self.name].operator_started = False
        sfx.clocks.pop(self.name)
        bpy.data.collections.remove(bpy.data.collections.get('ww SFX_Nodes'))
        print('Node destroyed',self)

    def tick(self,context):
        self.draw_buttons(context,self.layout)

    def draw_buttons(self, context, layout):
        box = layout.box()
        col = box.column(align = True)
        row = col.split(factor = 0.3)
        if not(sfx.clocks[self.name].operator_started):
            row.operator('sfx.clock_op',text ='Start')
        else:
           row.operator('sfx.commstarteddiag',text ='Started')
        row1 = row.split(factor = 0.75) 
        row1.prop(sfx.clocks[self.name],'date',text = '')
        row2 = row1.split(factor = 1)
        row2.prop( sfx.clocks[self.name], 'TickTime_prop', text = '')

    def draw_buttons_ext(self, context, layout):
        pass

    def draw_model(self,context):
        collection = bpy.data.collections.new('ww SFX_Nodes')
        bpy.context.scene.collection.children.link(collection)

    def init_sfxData(self):
        sfx.clocks.update({self.name :self.sfx_clock})
        pass

    def update(self):
        pass