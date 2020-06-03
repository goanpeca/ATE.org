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
  
  - 'Q' = Quality ➜ holds the programs for the Quality Engineers, thus the **QUALITY department**.
  
  - 'q' = Qualification ➜ holds the programs for the Qualification Engineers, thus the **QUALIFICATION department**.
  
`Designator` ➜ MIR/FLOW_ID, depends on the `Flow`

  | Flow | Designator       | Examples  |
  |:-----|:-----------------|:------------|
  | C    | 1, 2, 3, ...     | CTCA_HW1_FT_XYZ_C_1 ➜ Final Test, first checker program |
  | M    | 1, 2, 3, ...     | CTCA_HW1_FT_XYZ_M_1 ➜ Final Test, first maintenance program |
  | P    | 1, 2, 3, ... [QC]| CTCA_HW1_FT_XYZ_P_1 ➜ Final Test, production, first program<br> CTCA_HW1_FT_XYZ_P_QC ➜ Final Test, Production, Quality Check |
  | E    | 1, 2, 3, ...     | CTCA_HW1_FT_XYZ_E_7 ➜ Final Test, engineering program #7 |
  | V    | 1, 2, 3, ...     | CTCA_HW1_FT_XYZ_V_3 ➜ Final Test, validation program #3 |
  | Q    | 1, 2, 3, ...     | CTCA_HW1_FT_XYZ_Q_2 ➜ Final Test, quality program #2 |
  | q    | **see below**    |                                                        |



# TODO

  [  ] Add a 'checker' flow for PR
  [  ] Add a 'checker' flow for FT
  [  ] add a 'maintenance' flow for PR
  [  ] add a 'maintenance' flow for FT
  [  ] rename 'characterisation' to 'quality' for PR
  [  ] rename 'characterisation' to 'quality' for FT

# Notes

## USER_TXT

  | Flow | Default user text |
  |:-----|:------------------|
  | C    | f"Checker program for {Target} in {Base} at {Temperature}" |
  | M    | f"Maintenance program for {Target} in {Base} at {Temperature}" |
  | P    | f"Production program #{Designator} for {Target} in {Base} at {Temperature}" |
  | E    | f"Engineering program #{Designator} for {Target} in {Base} at {Temperature}" |
  | V    | f"Validation program #{Designator} for {Target} in {Base} at {Temperature}" |
  | Q    | f"Quality program #{Designator} for {Target} in {Base} at {Temperature}" |
  | q    | f"Quality program #{Designator} for {Target} in {Base} at {Temperature}" |
  
