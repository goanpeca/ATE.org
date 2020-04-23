# Toolbar



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

The `flows` section is **ONLY** enabled for the context menu **IF** a Base is defined (PR or FT)
In other workds, if `Base` is the **empty** string, then `flows` is disabled for the context menu.

If in the toolbar, no Base is selected, the Target will list **ALL** targets for PR and FT, in
other words :**all** dies and **all** products. 

If one selects a Target, the `Base` of the selected `Target` is updated.

If one selects another `Base`, the corresponging `Targets` are updated. If the previously
selected `Target` is in the new `Target` list, that one is selected. If the previously
selected `target` is no longer in the new `Target` list, then the **empty** string (=first item)
is enabled.

On any change in the toolbar, the tree is updated.

### flows case Nr1: `Base` = ''

### flows case Nr2: `Base` = FT

### flows case Nr3: `Base` = FT and 





## tests
