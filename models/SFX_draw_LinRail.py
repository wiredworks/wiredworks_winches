import bpy

class SFX_drawLinRail():
    '''Draws Rail in 3D_View'''
    bl_idname = 'SFX_draw_LinRail'

    def __init__(self,name):
        pass        

    def draw_model(self,name):
                
        if 'ww SFX_Nodes' in bpy.context.scene.collection.children.keys():            
            ww_Actcollection = bpy.data.collections.new(name)
            bpy.data.collections.get("ww SFX_Nodes").children.link(ww_Actcollection)
            #Add Bevel Thingy
            coords_list = ([[0.01,0.02,0], [0.06,0.06,0],[0.02,0.01,0],[0.02,-0.01,0],
                            [0.06,-0.06,0], [0.01,-0.02,0],[-0.01,-0.02,0],[-0.06,-0.06,0],
                            [-0.02,-0.01,0], [-0.02,0.01,0],[-0.06,0.06,0],[-0.01,0.02,0],[0.01,0.02,0]])
            extr = bpy.data.curves.new('crv', 'CURVE')
            extr.dimensions = '3D'
            spline = extr.splines.new(type='POLY')
            spline.points.add(len(coords_list)-1) # theres already one point by default
            for p, new_co in zip(spline.points, coords_list):
                p.co = (new_co + [1.0]) # (add nurbs weight)
            Extr = bpy.data.objects.new(name+'_extr', extr)
            Extr.location = (0,0,0)
            ww_Actcollection.objects.link(Extr)
            # Add Path
            coords_list = ([[0,0,0], [0,0,0]])
            path = bpy.data.curves.new(name+'_path', 'CURVE')
            path.dimensions = "3D"
            spline = path.splines.new(type='POLY')
            spline.points.add(len(coords_list)-1)
            for p, new_co in zip(spline.points, coords_list):
                p.co = (new_co + [1.0]) # (add nurbs weight)
            Path = bpy.data.objects.new(name+'_Path', path)
            Path.location =(0,0,0)
            ww_Actcollection.objects.link(Path)
            # Bevel Bevel Thingy
            Path.data.bevel_object = Extr
            # Add Empties as hooks
            # In hook 
            In = bpy.data.objects.new( name+"_In", None )
            In.empty_display_size = 2
            In.empty_display_type = 'ARROWS'
            In.location = (0,0,0)
            ww_Actcollection.objects.link( In )
            # Out hook
            Out = bpy.data.objects.new(name+"_Out", None )
            Out.empty_display_size = 2
            Out.empty_display_type = 'ARROWS'
            Out.location = (0,0,0)
            ww_Actcollection.objects.link( Out )
            # hook modifier left
            hook_left = Path.modifiers.new(name= 'hook_left', type = 'HOOK')
            Path.modifiers['hook_left'].object = bpy.data.objects[name+'_In']
            Path.modifiers['hook_left'].vertex_indices_set([0])
            # hook modifier right 
            hook_right = Path.modifiers.new(name= 'hook_right', type = 'HOOK')
            Path.modifiers['hook_right'].object = bpy.data.objects[name+'_Out']
            Path.modifiers['hook_right'].vertex_indices_set([1])
            # Object Connect 
            Connector = bpy.data.objects.new(name+"_Connector", None )
            Connector.empty_display_size = 0.25
            Connector.empty_display_type = 'SPHERE'
            Connector.location = (0,0,0)
            Connector.constraints.new(type = 'FOLLOW_PATH')
            Connector.constraints['Follow Path'].target = Path
            Connector.constraints['Follow Path'].use_curve_follow = True
            Connector.constraints['Follow Path'].use_curve_radius = True
            ww_Actcollection.objects.link( Connector )
            Out.location = (0,0,5)
            if name[-4] == '.':
                Extr.location = (float(name[-3:]) ,float(name[-3:]),0)
                Path.location =(float(name[-3:]),float(name[-3:]),0)
                In.location = (float(name[-3:]),float(name[-3:]),0)
                Out.location = (float(name[-3:]),float(name[-3:]),5)                
        else:
            bpy.ops.sfx.collnotexisttdiag('INVOKE_DEFAULT')