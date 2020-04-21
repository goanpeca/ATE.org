This is a place holder directory where we will copy in all the stuff the
guys from the LAB and guys like Jonathan and the stuff from InvenSense I
got is placed.

basicaly these are primitive API's to some instrumentation

We will organize things hereunder in the following way:

    - Manufacturer
        - Equipment
            - Implementer
            
so that for example one can write in a test (or better, the common.py file) :

    from ATE.instruments.Keithley.K2000.Micornas import K2000 
    
this 'Implementer' level is needed to let different implementations live
side by side. The idea is that if a common implementation is used/selected, 
it will live one level up, so we can also do :

    from ATE.instruments.Keithley import K2000 
    
if one wants the "unified" implementation and still the shit from other 
implementers is available :-)

Also note that in the case of a 'plugin' the above could become:

    from foo.bar.jefke import K2000

and still the ATE.org system can past this in ! :tada:

now ... the point is that we can't maintain all implementations of everybody
in the TDK group ... so we will need to work with plug-in's (as we do anyway
for the 'import' stuff) OK, but when for example IC-Sense makes a test program
(for Verification to name something), and they use their 'libraries', then 
Micronas will have a problem running this program as they don't have the
referenced libraries installed ... we need thus to foresee a 'copy-in' from 
the libraries to the project !

This way we can define the Equipment level, and the 'Implementer' level is 
de-coupled, but not disfunctional :-)