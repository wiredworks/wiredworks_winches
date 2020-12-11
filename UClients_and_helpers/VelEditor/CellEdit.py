# cl
import wx, wx.xrc
import wx.lib.mixins.listctrl as listmix

class listKeyPoints(wx.ListCtrl,listmix.TextEditMixin):
    _firstEventType = wx.EVT_SIZE
    #_firstEventType = wx.EVT_WINDOW_CREATE

    def __init__(self):
        
        wx.ListCtrl.__init__
        # p = wx.PreListCtrl()
        # # the Create step is done by XRC.
        # self.PostCreate(p)
        # # Apparently the official way to do this is:
        # #self.Bind(wx.EVT_WINDOW_CREATE, self.OnCreate)
        # # But this seems to be the actually working way, cf:
        # # http://aspn.activestate.com/ASPN/Mail/Message/wxPython-users/2169189
        self.Bind(self._firstEventType, self.OnCreate)

    def _PostInit(self):
        listmix.TextEditMixin.__init__(self)
        self.DeleteAllColumns()
        self.InsertColumn(0,'Description',format= wx.LIST_FORMAT_LEFT,width = 80)
        self.InsertColumn(1,'Number',format= wx.LIST_FORMAT_CENTER,width = 55)
        self.InsertColumn(2,'X-Coord',format= wx.LIST_FORMAT_CENTER,width = 60)
        self.InsertColumn(3,'Y-Coord',format= wx.LIST_FORMAT_CENTER,width = 60)
        self.InsertColumn(4,'Z-Coord',format= wx.LIST_FORMAT_CENTER,width = 60)
        self.InsertColumn(5,'Time',format= wx.LIST_FORMAT_CENTER,width = 60)
        self.InsertColumn(6,'Vx',format= wx.LIST_FORMAT_CENTER,width = 60)
        self.InsertColumn(7,'Vy',format= wx.LIST_FORMAT_CENTER,width = 60)
        self.InsertColumn(8,'Vz',format= wx.LIST_FORMAT_CENTER,width = 60)
        self.InsertColumn(9,'VAbs',format= wx.LIST_FORMAT_CENTER,width = 60)

    def OnCreate(self, evt):
        self.Unbind(self._firstEventType)
        # Called at window creation time
        self._PostInit()
        self.Refresh()
        
class listBigKeyPoints(wx.ListCtrl,listmix.TextEditMixin):
    _firstEventType = wx.EVT_SIZE
    #_firstEventType = wx.EVT_WINDOW_CREATE

    def __init__(self):
        wx.ListCtrl.__init__
        # p = wx.PreListCtrl()
        # # the Create step is done by XRC.
        # self.PostCreate(p)
        # # Apparently the official way to do this is:
        # #self.Bind(wx.EVT_WINDOW_CREATE, self.OnCreate)
        # # But this seems to be the actually working way, cf:
        # # http://aspn.activestate.com/ASPN/Mail/Message/wxPython-users/2169189
        self.Bind(self._firstEventType, self.OnCreate)

    def _PostInit(self):
        listmix.TextEditMixin.__init__(self)

    def OnCreate(self, evt):
        self.Unbind(self._firstEventType)
        # Called at window creation time
        self._PostInit()
        self.Refresh()
        
class listKeyPointWindow(wx.ListCtrl,listmix.TextEditMixin):
    # Liste im Fenster zum KeyPoint editing
    #_firstEventType = wx.EVT_SIZE
    _firstEventType = wx.EVT_WINDOW_CREATE

    def __init__(self):
        wx.ListCtrl.__init__
        # p = wx.PreListCtrl()
        # # the Create step is done by XRC.
        # self.PostCreate(p)
        # # Apparently the official way to do this is:
        # #self.Bind(wx.EVT_WINDOW_CREATE, self.OnCreate)
        # # But this seems to be the actually working way, cf:
        # # http://aspn.activestate.com/ASPN/Mail/Message/wxPython-users/2169189
        self.Bind(self._firstEventType, self.OnCreate)
        
    def _PostInit(self):
        listmix.TextEditMixin.__init__(self)
        
    def OnCreate(self, evt):
        self.Unbind(self._firstEventType)
        # Called at window creation time
        self._PostInit()
        self.Refresh()
        
class listPathEditWindow(wx.ListCtrl,listmix.TextEditMixin):
    # Liste im Fenster zum KeyPoint editing
    #_firstEventType = wx.EVT_SIZE
    _firstEventType = wx.EVT_WINDOW_CREATE

    def __init__(self):
        wx.ListCtrl.__init__
        # p = wx.PreListCtrl()
        # # the Create step is done by XRC.
        # self.PostCreate(p)
        # # Apparently the official way to do this is:
        # #self.Bind(wx.EVT_WINDOW_CREATE, self.OnCreate)
        # # But this seems to be the actually working way, cf:
        # # http://aspn.activestate.com/ASPN/Mail/Message/wxPython-users/2169189
        self.Bind(self._firstEventType, self.OnCreate)
        
    def _PostInit(self):
        listmix.TextEditMixin.__init__(self)
        
    def OnCreate(self, evt):
        self.Unbind(self._firstEventType)
        # Called at window creation time
        self._PostInit()
        self.Refresh()