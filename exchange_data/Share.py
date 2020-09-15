import bpy

class Shared(bpy.types.PropertyGroup):
    bl_idname = 'ww_Share'

    ww_base_data = { "Ptime"           : 0,
                     "Btime"           : 0,
                     "X-Soll"          : -1.0 ,
                     "Y-Soll"          : -1.0,
                     "Z-Soll"          : -1,
                     "X-Ist"           : 0.0,
                     "Y-Ist"           : 0.0,
                     "Z-Ist"           : 0.0,
                     "EndCommOPerator" : False,
                     "Destroy"         : False}

    ww_base_Joy = { 'Ptime'            : 0,
                    'Btime'            : 0,
                    'X-Achse'          : 0,
                    'Y-Achse'          : 0,
                    'Z-Achse'          : 0,
                    'X-Rot'            : 0,
                    'Y-Rot'            : 0,
                    'Z-Rot'            : 0,
                    'Slider'           : 0,
                    'Buttons'          : 0,
                    'HAT-Switch'       : 0,
                    'EndCommOPerator' : False,
                    'Destroy'         : False}

    ww_data = {"Name_IP_RPort_SPort": ww_base_data}
    ww_Joy  = {"Name_IP_RPort_SPort": ww_base_Joy}
