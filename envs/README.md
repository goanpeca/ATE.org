# ATE.org/envs

This directory holds some yaml files to create environments.

Create the environment fro the yaml file like this : `conda env create -f environment.yml`

Boot into spyder from outside conda: `/usr/bin/env conda run -n __spyder__ spyder`

Boot into spyder from inside conda: `conda run -n __spyder__ spyder`

... don't understand why the command doesn't return after closing spyder ...