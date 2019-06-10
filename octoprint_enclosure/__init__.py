# coding=utf-8
from __future__ import absolute_import
from octoprint.util import RepeatedTimer
from random import randint
from .hardware import Hardware

import octoprint.plugin

class EnclosurePlugin(octoprint.plugin.SettingsPlugin,
                      octoprint.plugin.AssetPlugin,
                      octoprint.plugin.TemplatePlugin,
                      octoprint.plugin.StartupPlugin):

        def __init__(self):
            self._sensorUpdateTimer = None
            self._hardware = None
        
        def updateSensorValues(self):
            hum, temp = self._hardware.getSensorValues()
            self._plugin_manager.send_plugin_message(self._identifier, 
                dict(
                    temperature=temp,
                    humidity=hum
                )
            )
            self._hardware.setLedState(~self._hardware.getLedState())
            
        def startTimer(self, interval):
            self._sensorUpdateTimer = RepeatedTimer(interval, self.updateSensorValues, None, None, True)
            self._sensorUpdateTimer.start()

        def on_after_startup(self):
            self._hardware = Hardware(
                int(self._settings.get(['sensorPin'])),
                int(self._settings.get(['ledPin']))
            )

            self.startTimer(int(self._settings.get(['sensorUpdateInterval'])))
            self._logger.info("Enclosure plugin started!")

	def get_settings_defaults(self):
		return dict(
                        sensorUpdateInterval=5,
                        sensorPin=23,
                        ledPin=24
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
		# Define the configuration for your plugin to use with the Software Update
		# Plugin here. See https://github.com/foosel/OctoPrint/wiki/Plugin:-Software-Update
		# for details.
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


# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "Enclosure Plugin"

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = EnclosurePlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}

