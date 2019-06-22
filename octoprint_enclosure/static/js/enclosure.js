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

		self.pluginName = "enclosure";

		self.temperature = ko.observable();
		self.ledState = ko.observable();
		self.ledBtnText = ko.observable();

		//This function is executed when the backend sends a message
		self.onDataUpdaterPluginMessage = function(plugin, data){
			if(plugin == self.pluginName){
				self.temperature(data.temperature);
				if(data.ledState){
					self.ledState("On");
					self.ledBtnText("Turn led off");
				}else{
					self.ledState("Off");
					self.ledBtnText("Turn led on");
				}
			}
		}
		
		self.toggleLedState = function(){
			$.ajax({
				url: self.buildPluginUrl("/toggleLedState"),
				type: "GET",
				dataType: "json"
                    	});
		}

		self.buildPluginUrl = function(path){
			return window.PLUGIN_BASEURL + self.pluginName + path;
		}

	}

	OCTOPRINT_VIEWMODELS.push({
		construct: EnclosureViewModel,
		dependencies: ["settingsViewModel"],
		elements: ["#settings_plugin_enclosure", "#navbar_plugin_enclosure", "#sidebar_plugin_enclosure"]
	});
});
