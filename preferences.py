import os
import sys
import bpy
from bpy.props import BoolProperty,PointerProperty

addonName = os.path.basename(os.path.dirname(__file__))

class DeveloperProperties(bpy.types.PropertyGroup):
    bl_idname = "ACT_DeveloperProperties"

    #profiling: PointerProperty(type = ProfilingProperties)

    debug: BoolProperty(name = "Debug", default = False,
        description = "Enable some print statements")

    runTests: BoolProperty(name = "Run Tests", default = False,
        description = "Run the test suite when Blender starts")

class NodesPreferences(bpy.types.AddonPreferences):
    bl_idname = addonName

    developer: PointerProperty(type = DeveloperProperties)
    
    showUninstallInfo: BoolProperty(name = "Show Deinstall Info", default = False,
        options = {"SKIP_SAVE"})

    def draw(self, context):
        layout = self.layout

        col = layout.column(align = True)
        col.split(factor = 0.25).prop(self, "showUninstallInfo", text = "How to Uninstall?",
            toggle = True, icon = "INFO")
        if self.showUninstallInfo:
            col.label(text = "1. Disable wiredworks_winches and save the user settings.")
            col.label(text = "2. Restart Blender and remove the addon (without enabling it first).")

def getPreferences():
    return bpy.context.preferences.addons[addonName].preferences

def debuggingIsEnabled():
    return getPreferences().developer.debug

def testsAreEnabled():
    return getPreferences().developer.runTests

def getBlenderVersion():
    return bpy.app.version

def getACT_Version():
    return sys.modules[addonName].bl_info["version"]
