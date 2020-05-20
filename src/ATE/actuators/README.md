## ATE/actuators

When creating an ATE test (or an ATE test program for that matter), we might have an idea about what handler/prober the test,
test program or hell the whole test project might be running on initially, but we don't have a crystal ball, so we don't 
REALLY know on what probers/handlers the tests/programs/project will be running on in it's life time.

Therefore, we make 100% abstraction of the handler/prober. Instead, we define the `actuators` that we want to use.

An actuator is something that generates a non-electrical stimulus to our DUT, for example:
  * Temperature
  * Magnetic field
  * Light
  * Acceleration
  * Position 
  * Pressure 
  * ...
  
At **RUNTIME** these actuators are mapped to a `Test Cell`.

A `Test Cell` is a handler/prober, ofcourse the chosen ATE **AND** possibly (extension) actuators.

For example, most handlers/probers can generate `Temperature`, but very few can also do `Magnetic field`. Most commonly one
does buys a commercial handler and one adds a `module` that generates for example a `Magnetic field`. Now, of course the 
handler doesn't control the magnetic field (for a varity of reasons, closed source being one of them). The controlling unit
should be anything, as long as it is **NOT** the ATE! Because if we do so, we create non-portable setups, meaning that in 
the test code of the ATE we 'control' the actuator but then we can't use the same ATE software anymore to go from one setup 
(maybe the development environment) to another setup (LAB, Quality, production FT/PR, QC, Qualification) because also the 
handler type will most likely change. This leads to 'touching the code' ... but this is a huge **no-go** in Automotive, 
as this means you need to re-qualify **AND** inform your customers! This is a costly (in time as well as money) action 
that can simply be avoided by abstracting the actuator(s) in the ATE code, and map it at run-time to you test cell. 
