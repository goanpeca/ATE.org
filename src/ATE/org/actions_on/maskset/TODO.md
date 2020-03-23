# Context menus
The table needs to have context menus ;

## Context menu on the 'Direction' column 
    - input --> I
    - output --> O
    - bidirectional --> IO
    
## Context menu on the 'Type' column
    - Digital --> D
    - Analog --> A
    - Mixed --> M
    - Power --> P
    
## Context menu on the 'Name' column = convenience
    - Digital
    - Analog
    - Mixed
    - Power
    <separator>
    - input
    - output
    - bidirectional
    
Note: if multiple rows (or parts of rows) are selected, the action should
apply to all selected rows !

# Validator on 'PosX', 'PosY', 'SizeX' and 'SizeY'

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
