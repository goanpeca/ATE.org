ATE.org is itself a plug-in (pluggy based) for Spyder.

ATE.org is a tester agnostic system to write (ASIC) test programs, however
all things have their order and place, so that:

1. One needs to write as little as possible code.
2. Developers can develop next to eachother and merge their work without problems.
3. Only test need writing, all the rest is 'configuring'.
4. A test can be developed and debugged as a unit. 
5. Support is available for Shmooing, reporting, ...

This is accomplished through a series of wizards that guides us through the process
and prevents us of making costly mistakes.

The ATE.org system is setup as a base system, and it accepts itself other plugins, 
from different sources. Each such plugin can provide ATE.org with one or more of 
the following (but at least **ONE**) :

1. Importers

The ATE.org system has some import hooks (most notably in some wizards).
For each of these hooks, a plugin can supply a 'stub'.

>Use case:
>   In the 'Maskset Wizard', some data needs to be filled in. 
>   Ofcourse this is an error-prune operation, what is more is that the data
>   that is asked will live somewhere on the 'company network'.
>   That is why there is an 'inport hook' present, so that (when implemented)
>   the stub will access (in whatever way) this data and siphones it to the
>   wizard, so that we have a quick, easy and error free modus-operandus.  

TODO: make a list of all import hooks

2. Exporters

The ATE.org system has some standard export hooks (most notably in the project tree).
For each of these hooks, a plugin can supply a 'stub'.

>Use case:
>   Say there is an export hook to generate a changelog of the project with 
>   respect to the previous version.
>   It is not un-thinkable that a specific company wants to have this in a 
>   company tailored format or even content.
>   An exporter hook can thus be provided to do so.

3. Documentation

Whenever a new project is created in ATE.org, the project automatically gets
a 'documentation' folder, that is filled in to the best of ATE.org's knowledge.
Given the fact that ATE.org is grown out of **automotive sensors**, the documentation
folder is filled with documents like the AEC documents, STDF documentation and so on.

>Use case:
>   Say a company is 'Medical' electronics, then a bunch of extra documentation
>   (of which ATE.org is ignorant about) could be needed to be inserted in the
>   documentation folder upon project creation.
>   A specific plugin could be made to extend the knowledge of ATE.org as the 
>   creator deams necessary.

4. Actuators

ATE.org is grown out of **automotive sensor** industry, and specificly for 
**sensors**, there is a 3th party in the mix ... the actuator. 
Examples of actuators are : magnetic field, light, acceleration, positionning, ... 
*ONE* type of actuator is usually build-in to a handler : **temperature**, but
more about that later. The point is that -we-can- but -we-will-not- control the
actuator from the test program. One is quickly seduced to do so, but the result is
that we get a test-program that is no longer portable from one setup to another, 
what is more is that (usually when shit hits the fan) we realize that also tha
actuator needs calibration, maintenance, exchanging, upgrading, and each time we
need to change the test-program ... in the automotive business, this is an
absolute **no-go** (eventhoug plenty of these companies do it this way!)
The solution is thus that the control of the actuator is out-sourced, if not
to the handler (because maybe a closed source commercial handler), then to the
Test Cell Controller (TCC, more about that later).
However, when we 'configure' a test program, we need to make up our mind what
kinds of actuators we are going to use (regardless of who controls them).
ATE.org provides some actuators, but it has no 'crystal ball', so any plugin
can add acctuators to ATE.org. (actually on the long run Actuators should be
pushed-out of ATE.org)

5. Equipment

With 'Equipment' we basically mean Handlers and Probers. In any setup we need
this. ATE.org has some widely used handlers and probers, however it should not
be the task of the ATE.org maintainers to maintain these implementations.
A hook allows us to push out (in a later stage) the Equipment to 3th parties
(maybe the manufacturers of these things?!?) and it allows for example a specific
company to handle their equipment themselves.

6. Instruments

Instruments are basically electronical measurement devices (like you find in 
any electronic lab). For now ATE.org holds some such instruments to get started, 
but similarly to Equipment we want to push this out on the long run, on the other 
hand, ATE.org is tester/instrument agnostic system, meaning that we do need to 
tell ATE.org sooner or later what 'insturments' are used, thus : plugin!

7. Testers

Testers (aka: ATE or Automatic Test Equipment), is basically a super instrument,
if you want, but the associated libraries are HUGE, and one uses only one
tester at a time (while we might use multiple instruments combined) that is 
why Testers are pulled out of 'Instruments'.
