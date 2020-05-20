# ATE/eaquipment

An `equipment` is defined in the first place as the `Test Cell Controller` (TCC), which implementation you find in this directory.
All the elements in a `Test Cell` are covered by the entries:
* [Actuators](./../actuators)
* Instruments
The Abstract Base Classes can be found for those can be found in those directories.
What we still miss however is the Abstract Base Classes for:
* [Handler](handler.py)s
* [Prober](prober.py)s
Those two Abstract Base Classes can be found here in the equally named python files. (for the lack of a better location)
