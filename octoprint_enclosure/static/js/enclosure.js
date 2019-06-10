/*
 * View model for OctoPrint-Enclosure
 *
 * Author: Wouter Bruggeman
 * License: AGPLv3
 */
$(function() {
	function EnclosureViewModel(parameters) {
		var self = this;
	
		self.settings = parameters[0];

		self.temperature = ko.observable();
		self.humidity = ko.observable();
		

		//This function is executed when the backend sends a message
		self.onDataUpdaterPluginMessage = function(plugin, data){
			if(plugin == "enclosure"){
				self.temperature(data.temp);
				self.humidity(data.humidity);
			}
		}

	}

	OCTOPRINT_VIEWMODELS.push({
		construct: EnclosureViewModel,
		dependencies: ["settingsViewModel"],
		elements: ["#settings_plugin_enclosure", "#navbar_plugin_enclosure"]
	});
});
