from Cocoa import *
from Foundation import NSObject
from AppKit import NSStatusBar
from PyObjCTools import AppHelper

import lifx

class LifxMenu(NSObject):

	def applicationDidFinishLaunching_(self, notification):

		icon = NSImage.alloc().initByReferencingFile_('images/lifx-icon@2x.png')
		icon.setScalesWhenResized_(True)
		icon.setSize_((20, 20))

		self.status_item = NSStatusBar.systemStatusBar().statusItemWithLength_(NSVariableStatusItemLength)
		self.status_item.setImage_(icon)
		self.status_item.setHighlightMode_(True)

		menu = NSMenu.alloc().init()
		self.toggle_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('Toggle lights', 'toggle:', '')
		menu.addItem_(self.toggle_item)
		quit_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('Quit', 'terminate:', '')
		menu.addItem_(quit_item)
		self.status_item.setMenu_(menu)

		self.lights = lifx.get_lights()
		self.toggle_item.setState_(self.lights[0].power)

	def toggle_(self, notification):
		state = not self.lights[0].power
		for bulb in self.lights:
			bulb.set_power(state)
		self.toggle_item.setState_(self.lights[0].power)

if __name__ == "__main__":
    app = NSApplication.sharedApplication()
    delegate = LifxMenu.alloc().init()
    app.setDelegate_(delegate)
    AppHelper.runEventLoop()
