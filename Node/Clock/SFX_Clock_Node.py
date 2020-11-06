import bpy

from ... exchange_data.sfx import sfx
from .SFX_Clock_Data import clock

class SFX_Clock_Node(bpy.types.Node):
    '''SFX_ClockNode'''
    bl_idname = 'SFX_Clock_Node'
    bl_label = 'clock'
    bl_icon = 'CURVE_NCIRCLE'
    bl_width_min = 350
    bl_width_max = 350

    sfx_type = 'Clock'

    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname == 'SFX_NodeTree'

    sfx       : bpy.props.PointerProperty(type = sfx)
    sfx_clock : bpy.props.PointerProperty(type = clock)

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

    def draw_buttons(self, context, layout):
        try:
            sfx.sensors[self.name]
        except KeyError:
            self.init_sfxData()
        box  = layout.box()
        col  = box.column(align = True)
        row  = col.split(factor = 0.85)
        row1 = row.split(factor = 0.4)
        row2 = row1.split(factor = 0.85)
        row3 = row2.split(factor = 0.85)
        row4 = row3.split(factor = 1)
        row.prop( sfx.clocks[self.name], 'TickTime_prop', text = '')
        row1.prop(sfx.clocks[self.name],'date',text = '')
        row2.prop(sfx.clocks[self.name], 'operator_running_modal', text = '')
        row3.prop(sfx.clocks[self.name], 'operator_started', text = '')
        if not(sfx.clocks[self.name].operator_started):
            row4.label(text ='Stoped')
        else:
           row4.label(text ='Started')
           
    def draw_buttons_ext(self, context, layout):
        pass
    
    def init_sfxData(self):
        sfx.clocks.update({self.name :self.sfx_clock})
        pass

    def sfx_update(self):
        if sfx.clocks[self.name].operator_running_modal:
            self.color = (0,0.4,0.1)
            self.use_custom_color = True
        else:
            self.use_custom_color = False
        pass

    def draw_model(self,context):
        collection = bpy.data.collections.new('ww SFX_Nodes')
        bpy.context.scene.collection.children.link(collection)

