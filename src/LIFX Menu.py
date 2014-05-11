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
		self.status_item.setMenu_(menu)

		self.lights = lifx.get_lights()
		self.toggle_item.setState_(self.lights[0].power)

		submenu =  NSMenu.alloc().init()
		item =  NSMenuItem.alloc().initWithTitle_action_keyEquivalent_( 'Colours', '', '')
		item.setSubmenu_( submenu )
		menu.addItem_( item )
		subitem =  NSMenuItem.alloc().initWithTitle_action_keyEquivalent_( 'White', 'setColour:', '')
		subitem.setRepresentedObject_( 'White' )
		submenu.addItem_( subitem )
		subitem =  NSMenuItem.alloc().initWithTitle_action_keyEquivalent_( 'Red', 'setColour:', '')
		subitem.setRepresentedObject_( 'Red' )
		submenu.addItem_( subitem )
		subitem =  NSMenuItem.alloc().initWithTitle_action_keyEquivalent_( 'Green', 'setColour:', '')
		subitem.setRepresentedObject_( 'Green' )
		submenu.addItem_( subitem )
		subitem =  NSMenuItem.alloc().initWithTitle_action_keyEquivalent_( 'Blue', 'setColour:', '')
		subitem.setRepresentedObject_( 'Blue' )
		submenu.addItem_( subitem )


		for bulb in self.lights:
			submenu =  NSMenu.alloc().init()
			item =  NSMenuItem.alloc().initWithTitle_action_keyEquivalent_( bulb.get_addr(), '', '')
			item.setSubmenu_( submenu )
			menu.addItem_( item )
			subitem =  NSMenuItem.alloc().initWithTitle_action_keyEquivalent_( 'Toggle light', 'toggleBulb:', '')
			subitem.setRepresentedObject_( bulb )
			subitem.setState_(bulb.power)
			submenu.addItem_( subitem )

			
		quit_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('Quit', 'terminate:', '')
		menu.addItem_(quit_item)



	def toggle_(self, notification):
		state = not self.lights[0].power
		for bulb in self.lights:
			bulb.set_power(state)
		self.toggle_item.setState_(self.lights[0].power)

	def toggleBulb_(self, notification):
		bulb = notification._.representedObject
		state = not bulb.power
		bulb.set_power(state)
		notification.setState_(bulb.power)

	def setColour_(self, notification):
		hue = 0;
		saturation = 65535
		colour = notification._.representedObject
		if colour == 'White' :
			hue = 9802
			saturation = 10023
		if colour == 'Red' :
			hue = 0
			saturation = 65535
		if( colour == 'Green' ):
			hue = 65535/360*120
			saturation = 65535
		if( colour == 'Blue' ):
			hue = 65535/360*240
			saturation = 65535
		for bulb in self.lights:
			bulb.set_color( hue, saturation, 65535, 3500, 1000)


if __name__ == "__main__":
    app = NSApplication.sharedApplication()
    delegate = LifxMenu.alloc().init()
    app.setDelegate_(delegate)
    AppHelper.runEventLoop()
