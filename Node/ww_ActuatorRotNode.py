import bpy

class ww_ActuatorRotNode(bpy.types.Node):
    '''ww Rotational Actuator'''
    bl_idname = 'ww_ActuatorRot'
    bl_label = 'Rot Actuator'
    bl_icon = 'PROP_CON'

    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname == 'ww_NodeTree'

    intProp : bpy.props.IntProperty()

    def init(self, context):
        # makes a new output socket of type 'NodeSocketInt' with the
        #   label 'output' on it
        # NOTE: no elements will be drawn for output sockets
        self.outputs.new('NodeSocketInt', "output")

    def copy(self, node):
        print("copied node", node)

    def free(self):
        print("Node removed", self)

    def draw_buttons(self, context, layout):
        # create a slider for int values
        layout.prop(self, 'intProp')

    # this method lets you design how the node properties
    #   are drawn on the side panel (to the right)
    #   if it is not defined, draw_buttons will be used instead
    #def draw_buttons_ext(self, context, layout):

    #OPTIONAL
    #we can use this function to dynamically define the label of
    #   the node, however defining the bl_label explicitly overrides it
    #def draw_label(self):
    #   return "this label is shown"

