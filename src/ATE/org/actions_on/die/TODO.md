# context menus on tree-view

## context menus on dies

    - Add

## context menus on die

    - View
    - Edit
    - Trace
    - <sep>
    - Delete (no 'make obsolete here')


# logic on 'DieWizard'

When a Maskset is selected, the wizard needs to collect all A grade DIES for 
that maskset.
    - if there is none, then the grade dropdown box needs to gray out
      everything (except 'A') so no aleternative grade can be selected.
      
    - if there is A grades available, then (when something else as A grade
      is selected in grade), these 'A' grade DIES are displayed in the 
      'reference Grade' pulldown box.
      
If a Maskset is selected, the wizard needs to see if the selected mask set
is an ASIC or and ASSP. 

    - ASSP : the 'customer' IS an empty string
    - ASIC : the 'customer' is NOT an empty string

if the selected maskset is an ASIC, then the new die is by default 
also an ASIC, so the Type is filled in as 'ASIC', and in the customer field
the customer is filled in and both the pulldown box and the lineEdit are
disabled.

So only if the Maskset is an ASSP, we have both options available.

Note: work with 'set' of 
        - get_dies_for_hardware
        - get_dies_for_maskset
        - get_dies_for_grade
        - get_dies_for_customer
      for the above logic instead of custom functions in navigator.