# simplyprint-hass-poc
This is a proof of concept to show the developers of the SimplyPrint app what 1 part of the Home Assistant Integration should look like. The Add-On/APP is a different type of home assistant component that lets you run the server on your local HASS system. 

This integration pulls sensor data from all of your SimplyPrint Printers, so you can monitor the status via home assistant. The current sensors being pulled as of v1.0 are:
- Status (Printing, Paused, Idle, Error)
- Nozzle temp
- Bed temp
- Percentage (of the print so far)
  
