Basically our plugin for Spyder (for now called SpyderMockUp) lives under
this directory.

We thus should pull-in the 'SpyderMockUp' directory to here!

Spyder itself recognizes (or will recognize from V5 onward) plugins for 
Spyder by means of the 'pluggy' library : https://pypi.org/project/pluggy/

Our plugin will itself have plug-in's (per company imports/exports),
so we will ourselves also use 'pluggy' to recognize (find) our plugins :-)