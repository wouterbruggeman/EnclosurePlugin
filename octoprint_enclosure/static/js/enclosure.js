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
		self.humidity = ko.observable();
		self.ledState = ko.observable();

		//This function is executed when the backend sends a message
		self.onDataUpdaterPluginMessage = function(plugin, data){
			if(plugin == self.pluginName){
				self.temperature(data.temperature);
				self.humidity(data.humidity);
				if(data.ledState){
					self.ledState("On");
				}else{
					self.ledState("Off");
				}
			}
		}
		
		self.toggleLedState = function(){
			$.ajax({
				url: self.buildPluginUrl("/toggleLedState"),
				type: "GET",
				dataType: "json",
				success: function(result){
					$("#ledState").html(result);
				};
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
