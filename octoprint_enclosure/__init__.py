# coding=utf-8

from __future__ import absolute_import
from octoprint.util import RepeatedTimer
from .hardwareinterface import HardwareInterface

import octoprint.plugin

class EnclosurePlugin(octoprint.plugin.SettingsPlugin,
                      octoprint.plugin.AssetPlugin,
                      octoprint.plugin.TemplatePlugin,
                      octoprint.plugin.StartupPlugin,
                      octoprint.plugin.ShutdownPlugin,
                      octoprint.plugin.BlueprintPlugin,
                      octoprint.plugin.EventHandlerPlugin):

        def __init__(self):
            self._frontendUpdateTimer = None
            self._hardwareUpdateTimer = None
        
        def updateFrontend(self):
            #Receive the temperature
            temp = self._hardwareInterface.getTemperature()

            #Receive the ledstate
            led = self._hardwareInterface.getLedState()

            #Send data to the frontend
            self._plugin_manager.send_plugin_message(self._identifier, 
                dict(
                    temperature=temp,
                    ledState=led
                )
            )

        @octoprint.plugin.BlueprintPlugin.route("/toggleLedState", methods=["GET"])
        def toggleLedState(self):
            #Toggle the led state
            self._hardwareInterface.setLedState(~self._hardwareInterface.getLedState())
            
            #Update the frontend
            self.updateFrontend()
            return ""
            
        def startTimers(self):
            frontendInterval = self._settings.get(['frontendUpdateInterval'])
            hardwareInterval = self._settings.get(['sensorUpdateInterval'])

            #Create and start the timers
            self._frontendUpdateTimer = RepeatedTimer(frontendInterval, self.updateFrontend)
            self._frontendUpdateTimer.start()

            self._hardwareUpdateTimer = RepeatedTimer(hardwareInterval, self._hardwareInterface.update)
            self._hardwareUpdateTimer.start()

        def on_after_startup(self):
            #Create the Hardware thread
            self._hardwareInterface = HardwareInterface(
                self,
                int(self._settings.get(['ledPin'])),
                int(self._settings.get(['buttonPin']))
            )
            #Turn on or off the leds, depending on the value in the settings
            self._hardwareInterface.setLedState(self._settings.get(['ledsOnAtStartup']))

            #Start the timers
            self.startTimers()


            # Update the frontend
            self._hardwareInterface.update()
            self.updateFrontend()

        def shutdown(self):
            self._frontendUpdateTimer.cancel()
            self._hardwareUpdateTimer.cancel()

        def on_event(self, event, payload):
            #if a client connected
            if(event == "ClientOpened"):
                #Update the sensor values on the client side
                self.updateFrontend()
            
            #If the print is started and the leds have to be turned on
            elif((event == "PrintStarted") and self._settings.get(['ledsOnAtPrintStart'])):
                self._hardwareInterface.setLedState(True)
            
            #If the timelapse has started and the leds have to be turned on
            elif((event == "CaptureStart") and self._settings.get(['ledsOnAtTimelapseStart'])):
                self._hardwareInterface.setLedState(True)

            #If the print has ended (failed or just done) and the leds have to be turned off
            elif(((event == "PrintFailed") or (event == "PrintDone")) and self._settings.get(['ledsOffAtPrintEnd'])):
                self._hardwareInterface.setLedState(False)
            
	def get_settings_defaults(self):
		return dict(
                        sensorUpdateInterval=30,
                        frontendUpdateInterval=5,
                        sensorName='',
                        ledPin=24,
                        buttonPin=25,
                        ledsOnAtStartup=False,
                        ledsOnAtTimelapseStart=True,
                        ledsOnAtPrintStart=False,
                        ledsOffAtPrintEnd=True,
		)
        
	def get_assets(self):
		return dict(
			js=["js/enclosure.js"],
			css=["css/enclosure.css"],
			less=["less/enclosure.less"]
		)

        def get_template_configs(self):
            return [
                dict(type="navbar", custom_bindings=False),
                dict(type="sidebar", custom_bindings=False),
                dict(type="settings", custom_bindings=False)
            ]

	def get_update_information(self):
            return dict(
                enclosure=dict(
                    displayName="Enclosure Plugin",
                    displayVersion=self._plugin_version,

                    # version check: github repository
                    type="github_release",
                    user="wouterbruggeman",
                    repo="EnclosurePlugin",
                    current=self._plugin_version,

                    # update method: pip
                    pip="https://github.com/wouterbruggeman/EnclosurePlugin/archive/{target_version}.zip"
                )
            )


__plugin_name__ = "Enclosure Plugin"

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = EnclosurePlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}

