# coding=utf-8

from __future__ import absolute_import
from octoprint.util import RepeatedTimer
from .hardwareThread import HardwareThread
import threading

import octoprint.plugin

class EnclosurePlugin(octoprint.plugin.SettingsPlugin,
                      octoprint.plugin.AssetPlugin,
                      octoprint.plugin.TemplatePlugin,
                      octoprint.plugin.StartupPlugin,
                      octoprint.plugin.BlueprintPlugin,
                      octoprint.plugin.ShutdownPlugin,
                      octoprint.plugin.EventHandlerPlugin):

        def __init__(self):
            self._frontendUpdater = None
            self._hardwareThreadThread = None
        
        def updateFrontend(self):
            #Receive the sensor values
            hum, temp = self._hardwareThread.getSensorValues()

            #Receive the ledstate
            led = self._hardwareThread.getLedState()

            #Send data to the frontend
            self._plugin_manager.send_plugin_message(self._identifier, 
                dict(
                    temperature=temp,
                    humidity=hum,
                    ledState=led
                )
            )

        @octoprint.plugin.BlueprintPlugin.route("/toggleLedState", methods=["GET"])
        def toggleLedState(self):
            #Toggle the led state
            self._hardwareThread.setLedState(~self._hardwareThread.getLedState())
            
            #Update the frontend
            self.updateFrontend()
            return ""
            
        def startTimer(self, interval):
            #Create and start the timer
            self._frontendUpdater = RepeatedTimer(interval, self.updateFrontend, None, None, True)
            self._frontendUpdater.start()

        def on_after_startup(self):
            #Create the HardwareThread
            self._hardwareThread = HardwareThread(
                self,
                int(self._settings.get(['sensorPin'])),
                int(self._settings.get(['ledPin'])),
                int(self._settings.get(['buttonPin'])),
                int(self._settings.get(['sensorUpdateInterval']))
            )
            self._hardwareThread.deamon = True
            self._hardwareThread.start()

            #Turn on or off the leds, depending on the value in the settings
            self._hardwareThread.setLedState(self._settings.get(['ledsOnAtStartup']))

            #Start the sensor timer
            self.startTimer(int(self._settings.get(['sensorUpdateInterval'])))

        def shutdown(self):
            self._hardwareThread.stop()
            self._hardwareThread = None

        def on_event(self, event, payload):
            #if a client connected
            if(event == "ClientOpened"):
                #Update the sensor values on the client side
                self.updateFrontend()
            
            #If the print is started and the leds have to be turned on
            elif((event == "PrintStarted") and self._settings.get(['ledsOnAtPrintStart'])):
                self._hardwareThread.setLedState(True)
            
            #If the timelapse has started and the leds have to be turned on
            elif((event == "CaptureStart") and self._settings.get(['ledsOnAtTimelapseStart'])):
                self._hardwareThread.setLedState(True)

            #If the print has ended (failed or just done) and the leds have to be turned off
            elif(((event == "PrintFailed") or (event == "PrintDone")) and self._settings.get(['ledsOffAtPrintEnd'])):
                self._hardwareThread.setLedState(False)
            
	def get_settings_defaults(self):
		return dict(
                        sensorUpdateInterval=5,
                        sensorPin=23,
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

