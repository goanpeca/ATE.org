# Context menus on tree-view

## masksets

    - Add

## maskset

    - View
    - Edit
    - Trace
    - Make obsolete <--- instead of delete ;-)

# context menus on 'MasksetWizard'
The table needs to have context menus ;

## Context menu on the 'Direction' column 
    - Input --> I
    - Output --> O
    - Bidirectional --> IO
    
## Context menu on the 'Type' column
    - Digital --> D
    - Analog --> A
    - Mixed --> M
    - Power --> P
    
## Context menu on the 'Name' column = convenience
    - Digital --> makes all selected rows 'Digital' in the Type column
    - Analog --> makes all selected rows 'Analog' in the Type column
    - Mixed --> makes all selcted rows 'Mixed' in the Type column
    - Power --> makes all selected rows 'Power' in the Type column
    <separator>
    - input --> makes all selected rows 'Input' in the Direction column
    - output --> makes all selected rows 'Output' in the Direction column
    - bidirectional --> makes all selected rows 'Bidirectional' in the Direction column
    
Note: if multiple rows (or parts of rows) are selected, the action should
apply to all selected rows !

# Validator on 'PosX', 'PosY', 'SizeX' and 'SizeY'

TBD

## Validator type
The 4 above mentioned columns can only hold POSETIVE integers to start off with.
Also an empty value (= default) is not allowed!
Then, per column the following validations need to be satified:

### PosX
PosX can not be bigger than 'Die Size X'
PosX + (SizeX/2) can not be bigger than 'Die Size X'

### PosY
PosY can not be bigger thant 'Die Size Y'
PosY + (SizeY/2) cna not be bigger than 'Die Size Y'

### SizeX
SizeX can not be bigger than 'Die Size X'

### SizeY
SizeY can not be bigger than 'Die Size Y'


### bondpadTable
In the table, each element of the column 'Name' *MUST* be filled in !
In the table, each element of the columns 'PosX', 'PosY', 'SizeX' and 'SizeY' *MUST* be filled in !
In the table, each element of the column 'Type' *MUST* be filled in !
In the table, each element of the column 'Direction' *MUST* be filled in !
