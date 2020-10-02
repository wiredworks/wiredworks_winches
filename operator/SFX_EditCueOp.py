import bpy
import time
import math
from scipy.integrate import quad
import wx

class SFX_simpleCueOp(bpy.types.Operator):
    """ simple Cue op"""
    bl_idname = "sfx.editsimplecueop"
    bl_label = "Simple Cue Operator"

    def modal(self, context, event):
        if event.type == 'TIMER':
            if self.MotherNode.operator_edit:
                self.MotherNode.operator_editing = True
                # Trigger Node Update
                self.MotherNode.TickTime1_prop = (time.time_ns() - self.old_time)/1000000.0                
                pass
                self.old_time = time.time_ns()
                return {'PASS_THROUGH'}
            self.MotherNode.operator_running_modal = False
            return{'CANCELLED'}
        return {'PASS_THROUGH'}
    def execute(self, context):
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def invoke(self, context, event):        
        #if not(context.active_node.operator_started_bit1):
        self.old_time = time.time_ns()
        self.MotherNode = context.active_node
        self.MotherNode.operator_edit = True
        #self.initGraph()
        #self.f = 0.0
        gApp = wxBlenderApp(redirect=False,
                        filename=None,
                        useBestVisual=False,
                        clearSigInt=True)
        gApp.MainLoop()
        return{'FINISHED'}

            #return self.execute(context)

    def draw(self,context):
        pass

    def initGraph(self):
        pass

class wxBlenderApp(wx.App):
    def OnInit(self):
        self.SetClassName('wxBlenderApp')
        self.SetAppName('wxBlenderApp')
        gMainWin = wxBlenderFrame(None)
        gMainWin.SetTitle('wxBlenderApp')
        self.SetTopWindow(gMainWin)
        gMainWin.Show()
        return True

class wxBlenderFrame(wx.Frame):

    def __init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString,
                 pos=wx.DefaultPosition, size=wx.DefaultSize,
                 # Use these styleBits for a standard frame...
                 style=wx.DEFAULT_FRAME_STYLE |
                        wx.STAY_ON_TOP
                 # ...Or use these styleBits for a borderless/taskbarless frame.(WinXP)
                 #style=wx.STAY_ON_TOP |
                  #     wx.FRAME_NO_TASKBAR |
                   #    wx.RESIZE_BORDER
                       , name='frame'):

        wx.Frame.__init__(self, parent, id, title, pos, size, style, name)

        panel = wx.Panel(self,-1)
        panel.Bind(wx.EVT_MOTION, self.OnMove)
        self.PosCtrl = wx.TextCtrl(panel,-1,'',pos =(40,10))

        self.Centre()
        self.SetFocus()

    def OnMove(self,evt):
        pos = evt.GetPosition()
        self.PosCtrl.SetValue("%s %s"%(pos.x,pos.y))


        # Lose focus destroy workaround.
        wx.CallAfter(self.Bind, wx.EVT_ACTIVATE, self.OnActivate)

    def OnActivate(self, event):
        """
        Destroy when frame loses focus to workaround Blender GUI lockup
        issue when wxapp is active.
        Ex: User has clicked back to the Blender GUI or another application.
        """
        try:
            self.Close()
        except RuntimeError:
            ###############
            ## Traceback (most recent call last):
            ##   File "....Blender\2.69\scripts\addons\wx_blender\wxblender.py", line ###, in OnActivate
            ##     self.Close()
            ## RuntimeError: wrapped C/C++ object of type wxBlenderAddMeshesFrame has been deleted
            ###############
            pass
        except Exception as exc:
            wx.Bell()
            import traceback
            tb = traceback.format_exc()
            f = open(gFileDir + os.sep + 'traceback.log', 'w')
            f.write('%s' %tb)
            f.close()

    def OnDestroy(self, event):
        self.Destroy()

