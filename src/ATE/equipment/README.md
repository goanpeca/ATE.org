# ATE/Equipment

This package contains EQUIPMENT, so anything that is *NOT* an INSTRUMENT.
Things that belong here :
    - prober (or better the Abstract Base Class for all `Prober` implementations)
    - handler (or better, the Abstract Base Class for all `handler` implementations)
    - TCC (Test Cell Controller)

Note:
  - Any plug-in for ATE.org that provedes one or more handler(s)/prober(s) should derive from handlerABC/proberABC.