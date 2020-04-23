# Toolbar

If in the toolbar, no Base is selected, the Target will list **ALL** targets for PR and FT, in
other words :**all** dies and **all** products. 

If one selects a Target, the `Base` of the selected `Target` is updated.

If one selects another `Base`, the corresponging `Targets` are updated. If the previously
selected `Target` is in the new `Target` list, that one is selected. If the previously
selected `target` is no longer in the new `Target` list, then the **empty** string (=first item)
is enabled.


On any change in the toolbar, the tree is updated.


# project tree view

## documentation (skip the 's' at the end !)

The tree view under `documentation` follows the structure under <project>\documentation.

If on spyder|project|open we see that the project has no `documentation` subdirectory,
we call the function `ATE.org.templates.documentation_templating(project_dir)`, 
this function is part of the spyder|new|project suit of functions that create a new project.
In our usecase this function is 'touching up' a project that lost his documentation directory.

## definitions

The `definitions` section in the project tree structure **ONLY** looks at
the `hardware` of the toolbar !

`hardwaresetups` is **ALWAYS** enabled for the context menu 
`masksets` is **ALWAYS** enabled for the context menu
`dies` is **ONLY** available for the context menu if (for the selected hardware in the toolbar) 
there is at least one `maskset` defined.
`packages` is **ALWAYS** available for the context menu
`devices` is **ONLY** available for the context menu if (for the selected hardware in the toolbar)
there is at least **ONE** 'die' defined under `dies`.
`products` is **ONLY** available for the conext menu if (for the selected hardware in the toolbar)
there is at least **ONE** 'device' defined under `devices`

## flows

The `flows` section is **directly** related to a `Target`.
As long as no `Target` is selected, the `flows` will be disabled for the context menu.

- `flows` in case `Target` = '' 

    `flows` is not enabled for the context menu

- `flows` in case `Target` is selected and `Base` is 'PR'

    `flows` is enabled for the context menu, but there is **NO** `qualification` section !
    Ah, yes, we do `qualification` only on what we sell, and we only sell `products` !
    We do however have the `production`, `engineering`, `validation`, and `characterisation` flows !
    
- `flows` in case `Target` is selected and `Base` is 'FT'

    `flows` is enabled for the context menu **AND** the `qualification` section is available, however
    based on the `package` that is associated to the `Target` (over `device`) we have a slightly 
    different outline of the `qualification` section:

1. The `device` of the selected `Target` is associated with the 'naked die' `package`

So, the package is 'virtual', this is the way we implement if we sell 'naked die' products.
It also means that some sections in the full `qualification` section are not applicable,
Notably everything to do with ... the package :wink:

2. The `device` of the selected `Target` is **not** associated with the 'naked die' `package`

So, we have a real package, and thus the full `qualification` section is available.     

## tests

Similar as `flows`, the `tests` section is **directly** related to a `Target`,
so again as long as no `Target` is selected the `tests` will be disabled for the context menu.

- `tests` in case `Target` == ''

    `tests` is not enabled for the context menu

- `tests` in case a `Target` is selected and `Base` is 'FT'


- `tests` in case a `Target` is selected and `Base` is 'PR'



