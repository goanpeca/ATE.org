# Test Program Name Definition

Project_Hardware_Base_Target_Flow_Designator.py

`Project`

`Hardware`

`Base`

`Target`

`FLOW` ➜ MIR/MODE_COD
  - 'C' = Checker ➜ holds the load-board/probe-card checker/calibration program(s)
    
  - 'M' = Maintenance ➜ holds the program(s) the Maintenance Engineers use, thus the **MAINTENANCE department**.

  - 'P' = Production ➜ holds the programs for production mode, thus the **PRODUCTION department**.
    
  - 'E' = Engineering ➜ holds the programs for the Test- and Product Engineers, thus the **TEST Department**
  
  - 'V' = Validation ➜ hods the programs for the Design Engineers, thus the **R&D department**.
  
  - 'C' = Characterisation ➜ holds the programs for the Quality Engineers, thus the **QUALITY department**.
  
  - 'Q' = Qualification ➜ holds the programs for the Qualification Engineers, thus the **QUALIFICATION department**.
  
`Designator` ➜ MIR/FLOW_ID, depends on the `Flow`

  | Flow | Designator       | Examples  | `USER_TXT` |
  |:-----|:-----------------|:------------|:---------|
  | C    | 1, 2, 3, ...     | CTCA_HW1_FT_XYZ_C_1 ➜ Final Test, first checker program | set manually |
  | M    | 1, 2, 3, ...     | CTCA_HW1_FT_XYZ_M_1 ➜ Final Test, first maintenance program | set manually |
  | P    | 1, 2, 3, ... [QC]| CTCA_HW1_FT_XYZ_P_1 ➜ Final Test, production, first program<br> CTCA_HW1_FT_XYZ_P_QC ➜ Final Test, Production, Quality Check | leave auto<br> leave auto |
  | E    | 1, 2, 3, ...     | CTCA_HW1_FT_XYZ_E_7 ➜ Final Test, engineering program #7 | set manually |
  | V    | 1, 2, 3, ...     | CTCA_HW1_FT_XYZ_V_3 ➜ Final Test, validation program #3 | set manually |
  | C    | 1, 2, 3, ...     | CTCA_HW1_FT_XYZ_C_1 ➜ 
