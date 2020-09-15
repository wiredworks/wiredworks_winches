import bpy

class ww_railModel():

    def draw_model(self,context):

        #Add Extrude Thingy
        coords_list = ([[0.01,0.02,0], [0.06,0.06,0],[0.02,0.01,0],[0.02,-0.01,0],
                        [0.06,-0.06,0], [0.01,-0.02,0],[-0.01,-0.02,0],[-0.06,-0.06,0],
                        [-0.02,-0.01,0], [-0.02,0.01,0],[-0.06,0.06,0],[-0.01,0.02,0],[0.01,0.02,0]])
        extr = bpy.data.curves.new('crv', 'CURVE')
        extr.dimensions = '3D'
        spline = extr.splines.new(type='POLY')
        spline.points.add(len(coords_list)-1) # theres already one point by default
        for p, new_co in zip(spline.points, coords_list):
            p.co = (new_co + [1.0]) # (add nurbs weight)
        Extr = bpy.data.objects.new(self.name+'_extr', extr)
        bpy.context.scene.collection.objects.link(Extr)

        # Add Path
        coords_list = ([[0,0,0], [0,0,0]])
        path = bpy.data.curves.new(self.name+'_path', 'CURVE')
        path.dimensions = "3D"
        spline = path.splines.new(type='POLY')
        spline.points.add(len(coords_list)-1)
        for p, new_co in zip(spline.points, coords_list):
            p.co = (new_co + [1.0]) # (add nurbs weight)
        Path = bpy.data.objects.new(self.name+'_Path', path)
        bpy.context.scene.collection.objects.link(Path)

        Path.data.bevel_object = Extr

        # Add Empties as hooks 
        bpy.ops.object.empty_add(type='ARROWS')
        In = bpy.data.objects['Empty'].name = self.name+'_In'
        #bpy.data.objects[self.name+'_In'].hide_select = True
        bpy.ops.object.empty_add(type='ARROWS')
        Out = bpy.data.objects['Empty'].name = self.name+'_Out'
        #bpy.data.objects[self.name+'_Out'].hide_select = True
        bpy.data.objects[self.name+'_Out'].location =[1,0,0]

        hook_left = Path.modifiers.new(name= 'hook_left', type = 'HOOK')
        Path.modifiers['hook_left'].object = bpy.data.objects[self.name+'_In']
        Path.modifiers['hook_left'].vertex_indices_set([0])

        hook_right = Path.modifiers.new(name= 'hook_right', type = 'HOOK')
        Path.modifiers['hook_right'].object = bpy.data.objects[self.name+'_Out']
        Path.modifiers['hook_right'].vertex_indices_set([1]) 