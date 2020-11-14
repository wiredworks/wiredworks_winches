import bpy

class SFX_simplelin_Model():
    '''Draws Simple Lin in 3D_View'''
    bl_idname = 'SFX_SimpleLin_Model'

    def __init__(self,name):
        pass        

    def draw_model(self,name):
                
        if 'ww SFX_Nodes' in bpy.context.scene.collection.children.keys():            
            Actcollection = bpy.data.collections.new(name)
            bpy.data.collections.get("ww SFX_Nodes").children.link(Actcollection)
            width   = 0.1
            height  = 0.1
            length  = 1
            Prism = self.create_prism(name, width, height, length)
            Actcollection.objects.link(Prism)

            In = bpy.data.objects.new(name+"_In", None )
            In.empty_display_size = 0.1
            In.empty_display_type = 'ARROWS'
            In.parent = Prism
            In.location = ( 0, 0, 0 )
            In.rotation_euler[2] = 3.1415926
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
            Out.parent = Prism
            Out.location = ( length/2, 0, 0 )
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
            Connector.parent = Prism
            Connector.location = ( -length/2.0, 0, 0 )
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

    def vertex_prism(self, width, length, z):
        verts = []

        verts.append(( length,  width/2.0, z)) 
        verts.append(( 0,       width/2.0, z))
        verts.append(( 0,      -width/2.0, z))
        verts.append(( length, -width/2.0, z))

        return verts

    def create_prism(self, name, width, height, length):
        '''Make a Prism'''

        data = {
                'verts' : [],
                'edges' : [],
                'faces' : [],
                }
                
        data['verts'].extend(self.vertex_prism(width, length, z = -height/2.0))
        data['verts'].extend(self.vertex_prism(width, length, z =  height/2.0))
        
        data['faces'].append(( 0, 1, 5, 4 ))
        data['faces'].append(( 1, 2, 6, 5 ))
        data['faces'].append(( 2, 3, 7, 6 ))
        data['faces'].append(( 3, 0, 4, 7 ))        
        data['faces'].append(( 0, 1, 2, 3 ))
        data['faces'].append(( 4, 5, 6, 7 )) 
        
        mesh = bpy.data.meshes.new(name) 
        mesh.from_pydata(data['verts'], data['edges'], data['faces']) 
        obj = bpy.data.objects.new(name, mesh)

        return obj