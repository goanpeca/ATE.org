# ATE/instruments

`ATE.org` is a tester (aka ATE) and `instrument` agnostic framework for ATE ASIC testing projects.

We need however to foresee that a project (might) need, besides a specific tester also one or more `instruments`.
The the definition, implementation and maintainence of an `instrument` library is **not** the task of ATE.org, however 
`ATE.org` needs to 'know about it' ...
We implement this through a plugin mechanism (based on the `pluggy` python package), in which a plugin can provide (amongst other things) one or more `instruments`.

We define here how the `instrument` part of the plugin should look like.

From the point of view of the `hardware_wizard` things look like this:

 ![hardware_wizard_instruments_tab](hardware_wizard.png)

Some preliminary thoughts:

