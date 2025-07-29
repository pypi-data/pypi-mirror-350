#!python

import sys
import os
import wx

# Try importing SDWire from pytelmbot, adjust sys.path if running as example
try:
    from pytelmbot import SDWire
except ImportError:
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from pytelmbot import SDWire

        
class SDWireController:
    SDWIRE_NAME = 'sd-wire_11' # Replace with your SDWire device name
    
    def __init__(self, wx_parent):
        """
        Initialize the SDWireController with a wx parent for dialogs.
        """
        self.wx_parent = wx_parent
        self.sdwire = SDWire(self.SDWIRE_NAME)
        self.ts_selected = False  # Track if test server is selected
        
    def drive_busy_prompt(self):        
        """
        Show a dialog when the drive is busy and cannot be ejected.
        Returns the user's choice.
        """
        dialog = wx.MessageDialog(
            parent=self.wx_parent,
            message="Could not eject the drive. Retry?",
            caption="Drive Busy",
            style=wx.ICON_HAND | wx.YES_NO
        )

        result = dialog.ShowModal()

        if result == wx.ID_YES:
            print("User chose to retry.")
            
        elif result == wx.ID_NO:
            print("User cancelled the operation.")

        dialog.Destroy()
        return result
    
    def force_switch_prompt(self):        
        """
        Show a dialog asking if the user wants to force the device switch.
        Returns the user's choice.
        """
        dialog = wx.MessageDialog(
            parent=self.wx_parent,
            message="Do you want to force the switch?",
            caption="Force device switch",
            style=wx.ICON_EXCLAMATION | wx.YES_NO
        )

        result = dialog.ShowModal()

        if result == wx.ID_YES:
            print("User chose to force.")
            
        elif result == wx.ID_NO:
            print("User chose not to force.")

        dialog.Destroy()
        return result

    def select_ts(self, evt=None):
        """
        Select the test server if not already selected.
        Optionally handle a wx event.
        """
        if not self.ts_selected:                
            self.sdwire.select_ts()
            self.ts_selected = True
            print("Test server selected")
            
        if evt:
            evt.Skip()
        
    def select_dut(self, evt=None):
        """
        Select the DUT (Device Under Test).
        Handles drive busy and force switch prompts as needed.
        Optionally handle a wx event.
        """
        force = False
        while self.ts_selected:
            if self.sdwire.select_dut(force):
                self.ts_selected = False
                print("DUT Selected")
            elif self.drive_busy_prompt() == wx.ID_YES:
                continue
            elif self.force_switch_prompt() == wx.ID_YES:
                force = True
            else:
                break
            
        if evt:
            evt.Skip()


class MyFrame(wx.Frame):
    def __init__(self):
        """
        Main application window with buttons to control SDWire.
        """
        super().__init__(parent=None, title='Telmbot Control', size=(300, 150))
        
        self.sdwire_controller = SDWireController(self)
        
        panel = wx.Panel(self)

        # Create buttons
        test_server_btn = wx.Button(panel, label='Test Server')
        test_server_btn.Bind(wx.EVT_BUTTON, self.sdwire_controller.select_ts)
        
        dut_btn = wx.Button(panel, label='DUT')
        dut_btn.Bind(wx.EVT_BUTTON, self.sdwire_controller.select_dut)

        # Layout using a box sizer
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(test_server_btn, 0, wx.ALL | wx.CENTER, 10)
        sizer.Add(dut_btn, 0, wx.ALL | wx.CENTER, 10)

        panel.SetSizer(sizer)

        self.Centre()
        self.Show()
        


if __name__ == '__main__':
    # List available SDWire devices and start the wx application
    SDWire.list_devices()   
    
    app = wx.App(False)
    frame = MyFrame()
    app.MainLoop()
