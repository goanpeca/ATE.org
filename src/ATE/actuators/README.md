## ATE/actuators

When creating an ATE tests for [sensors](https://en.wikipedia.org/wiki/Sensor), we might have an idea about what Test-Cell(s) these tests will run on initially, but we don't have a crystal ball, so we don't REALLY know how on what Test-Cells the ATE
test suit will be running during it's life time.

Therefore, we make abstraction of the Test-Cell by introducing `actuators` that we want to use from the tests.

An `actuator` is something that generates a <ins>**non-electrical stimulus**</ins> to our DUT, for example:
  * Temperature
  * Magnetic field
  * Light
  * Acceleration
  * Position 
  * Pressure 
  * ...

Now, I know that it is **exctreamly tempting** to use the ATE to control the `actuator`! After all measuring a signal and
generate another one that relates to that is the bread and butter of an ATE, however in doing so you make a very costly
(boath in time and money) mistake! 

I explain with an example using two actuators : `Temperature` and `Magnetic field`:

* <ins>In our development environment</ins>, we might change the DUT's ourselves by hand, the `temperature` comes from 
a [heatgun](https://www.google.com/search?sa=X&source=univ&tbm=isch&q=heat+gun&ved=2ahUKEwj4jKDKusHpAhWEUBUIHc7iALUQsAR6BAgJEAE&biw=2560&bih=1287)/[cold-spray](https://www.google.com/search?q=cold+spary&tbm=isch&ved=2ahUKEwiMyNbMusHpAhXoMewKHbEZDQ8Q2-cCegQIABAA&oq=cold+spary&gs_lcp=CgNpbWcQAzIGCAAQChAYOgIIKToECAAQQzoCCABQhowCWOWfAmCUpAJoAHAAeACAAUiIAZ4FkgECMTCYAQCgAQGqAQtnd3Mtd2l6LWltZw&sclient=img&ei=X57EXsycIujjsAexs7R4&bih=1287&biw=2560) and the `magnetic field` from a [self-wound coil](./../../../docs/pictures/coil.jpg) with a power supply (read: a current limited voltage source) as coil-driver. 

* <ins>In production Quality Control</ins> we might have a nice magnetic field generator based on a [Helmholz coil](https://en.wikipedia.org/wiki/Helmholtz_coil) driven by a real current source, the `temperature` might come from a 
[thermo-stream](https://www.youtube.com/watch?v=W2OYzQhiLNE), and we change the DUT's by hand.

* <ins>In production Probing</ins> (aka Wafer Sort) we use a so called [prober](https://www.google.com/search?q=wafer+prober&tbm=isch&ved=2ahUKEwiOlvWcrMHpAhUKShoKHZhxBJEQ2-cCegQIABAA&oq=wafer+prober&gs_lcp=CgNpbWcQAzIECAAQQzICCAAyAggAMgQIABAYMgQIABAYUOniDFik9Axg3PUMaABwAHgAgAFKiAG8BpIBAjEymAEAoAEBqgELZ3dzLXdpei1pbWc&sclient=img&ei=TY_EXs67EoqUaZjjkYgJ&bih=1287&biw=2560) to change the DUT's. Most likely the prober 
can apply a `Temperature` to the DUT (hell, to the whole wafer through the [Chuck](https://www.google.com/search?source=univ&tbm=isch&q=prober+chuck&sa=X&ved=2ahUKEwjVvNiarMHpAhVLy6QKHU71CMIQsAR6BAgJEAE&biw=2560&bih=1287)) and we of course don't have a Helmholz coil to generate the `magnetic field` (because the construct of the chuck), but (yet another) coil and probably yet another real current source (adapted to the coil).

* <ins>In Final Test production</ins> we might have a commercial handler like a [Cohu/Rasco SO1000](https://www.cohu.com/so1000) to switch DUT's. This handler can apply `Temperature` himself, but an adaptation needs to be made to generate the `Magnetic field`. This will
be yet another coil (Helmhotz will not work here because of the `plungers`) and probably yet an current/voltage source.

* <ins>In Quality</ins>, they might have a [super-duper 3D magnetic field generator](./../../../docs/pictures/qc6d.png) with special designed coil drivers to generate the `magnetic field`, the `Temperature` comes from a thermo-stream, and the DUT's are changed by hand.

* <ins>In the LAB</ins>, we might want to [Shmoo](https://en.wikipedia.org/wiki/Shmoo_plot) the tests we developed in
our `design environment` over `Temperatrue` (goes to '[reliability](https://en.wikipedia.org/wiki/Reliability_(statistics))', '[reproducability](https://en.wikipedia.org/wiki/Reproducibility)' and '[stability](https://en.wikipedia.org/wiki/Numerical_stability)' ... could extend to qualification, aka [ACQ100](http://www.aecouncil.com/AECDocuments.html), too ...) changing DUT's
will likely be by hand, `Temperature` comes from a thermo-stream (maybe even another brand/type as in orther departmenst!) and you can bet you ass on it that there will be yet another coil system to generate the `magnetic field`.

Maybe down the line for <ins>Final Test productin</ins> the Cuhu/Rasco SO1000 (this is a so called batch/singulated 
handler) needs to be replaced by an [In-Line Lead-Frame-handler](https://www.geringer.de/en/products/special-machine-building) ... do we want to touch the code that tests the DUT at such a point? No! We want to use the code developed
in the development environment and apply it to all above, and other use-cases!








At **RUNTIME** these actuators are mapped to the used `Test-Cell`.

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


