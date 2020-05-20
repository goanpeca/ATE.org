# ATE.org

`ATE.org` is a tester/instrument <ins>agnostic</ins> framework for ATE ASIC testing projects.

`ATE.org` support the following 'electronic grades':
* consumer
* industrial
* [automotive](https://en.wikipedia.org/wiki/Automotive_electronics)
* medical
* military

It also has **full** support for `sensor` testing !

It is implemented as a set of libraries **AND** a plug-in system to the [Spyder](https://github.com/spyder-ide/spyder)-IDE (starting from V5).

It adds the **ATE project type** to Spyder, with which one can organize ATE tests, test-programs, test-flows ... in a structured way. 

# Description

`ATE.org` is a tester/instrument **agnostic** framework. This means that the system is **not** build around a
a specific instrument (let's consider an ATE tester for a moment as a super instrument😋), it rather focuses on 
organizing (hence the project name: ATE.org) semiconductor testing in such a way that all special corner cases have
their well known place. This enables the users to focus on the **REAL** work : <ins>writing test</ins> rather than 
struggling to implement corner cases manually


# Note

This project has been set up using PyScaffold 3.2.2. For details and usage
information on PyScaffold see https://pyscaffold.org/.
