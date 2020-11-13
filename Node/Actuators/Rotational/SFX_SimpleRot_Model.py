import bpy
import math

class SFX_SimpleRot_Model():
    '''Draws Rail in 3D_View'''
    bl_idname = 'SFX_LinRail_Model'

    def __init__(self,name):
        pass        

    def draw_model(self,name):
                
        if 'ww SFX_Nodes' in bpy.context.scene.collection.children.keys():            
            Actcollection = bpy.data.collections.new(name)
            bpy.data.collections.get("ww SFX_Nodes").children.link(Actcollection)
            radius   = 0.5
            height   = 0.05
            segments = 32
            Cylinder = self.create_cylinder(name, radius, height, segments)
            Actcollection.objects.link(Cylinder)
            VertexGroupLower = Cylinder.vertex_groups.new(name='Lower')
            for i in range(segments):
                VertexGroupLower.add([i],1,"ADD")
            
            VertexGroupUpper = Cylinder.vertex_groups.new(name='Upper')
            for i in range(segments):
                VertexGroupUpper.add([segments+i],1,"ADD")

            In = bpy.data.objects.new(name+"_In", None )
            In.empty_display_size = 0.1
            In.empty_display_type = 'ARROWS'
            In.parent = Cylinder
            In.location = (0,0,-height/2)
            In.rotation_euler[0] = 3.1415926
            In.lock_location[0] = True
            In.lock_location[1] = True
            In.lock_location[2] = True
            In.lock_rotation[0] = True
            In.lock_rotation[1] = True
            In.lock_rotation[2] = True            
            Actcollection.objects.link(In)

            Out = bpy.data.objects.new(name+"_Out", None )
            Out.empty_display_size = 0.1
            Out.empty_display_type = 'ARROWS'
            Out.parent = Cylinder
            Out.location = (0,0,height/2)
            Out.lock_location[0] = True
            Out.lock_location[1] = True
            Out.lock_location[2] = True
            Out.lock_rotation[0] = True
            Out.lock_rotation[1] = True
            Out.lock_rotation[2] = True 
            Actcollection.objects.link(Out)

            Connector = bpy.data.objects.new(name+"_Connector", None )
            Connector.empty_display_size = 0.5
            Connector.empty_display_type = 'PLAIN_AXES'
            Connector.parent = Cylinder
            Connector.location = (0,0,height/2)
            Connector.lock_location[0] = True
            Connector.lock_location[1] = True
            Connector.lock_location[2] = True
            Connector.lock_rotation[0] = True
            Connector.lock_rotation[1] = True
            Connector.lock_rotation[2] = True 
            Actcollection.objects.link( Connector )

            # Out.location = (0,0,5)
            # if name[-4] == '.':
            #     Extr.location = (float(name[-3:]) ,float(name[-3:]),0)
            #     Path.location =(float(name[-3:]),float(name[-3:]),0)
            #     In.location = (float(name[-3:]),float(name[-3:]),0)
            #     Out.location = (float(name[-3:]),float(name[-3:]),5)                
        else:
            print('ww SFX Collection not existing')

    def vertex_circle(self, radius, segments, z):
        verts = []
        for i in range(segments):
            angle = (math.pi*2) * i / segments 
            verts.append((radius*math.cos(angle), radius*math.sin(angle), z)) 
        return verts

    def create_cylinder(self, name, radius, height, segments):
        '''Make a Cylinder'''

        data = {
                'verts' : [],
                'edges' : [],
                'faces' : [],
                }
                
        data['verts'].extend(self.vertex_circle(radius, segments, z = -height/2))
        data['verts'].extend(self.vertex_circle(radius, segments, z = height/2))
        
        for i in range(segments -1):
            data['faces'].append((i ,i+1, segments+i+1, segments+i))
        data['faces'].append((segments-1 ,0, segments, 2*segments-1))
        
        data['verts'].append((0, 0, -height/2))        
        center_vert = len(data['verts'])-1        
        for i in range(segments-1):
            data['faces'].append((i,i+1,center_vert))            
        data['faces'].append((segments-1,0,center_vert))
        
        data['verts'].append((0, 0, height/2))        
        center_vert = len(data['verts'])-1                         
        for i in range(segments-1):
            data['faces'].append((segments + i, segments + i+1, center_vert))            
        data['faces'].append((2*segments-1 , segments, center_vert))
        
        mesh = bpy.data.meshes.new(name) 
        mesh.from_pydata(data['verts'], data['edges'], data['faces']) 
        obj = bpy.data.objects.new(name, mesh)

        return obj