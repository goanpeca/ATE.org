This is a placeholder for ATE testers.
In principle ATE testers are 'Instruments', but they are so BIG that it makes
no sense to dump them under 'Instruments'.

Also, the ATE package is tester agnostic !

It must be possible to use the ATE.org system without a tester too!

The libraries for any tester are usualy 3-th party, so they can not be
maintained in the ATE.org project.

As a consequence, they need to be installed separately (with conda please)
using the python pluggy module:
     https://pypi.org/project/pluggy/
     https://github.com/pytest-dev/pluggy
     https://pluggy.readthedocs.io/en/latest/
     
so the ATE.org module can pick up on it :-)