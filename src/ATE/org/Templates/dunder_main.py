'''
Created on %DT%
Platform : %PLATFORM%

This is the main entry point for the %PROJECT% (zip) project

@author: %USER%
'''

import argparse

parser = argparse.ArgumentParser(description="Entry point selector for all %PROJECT% test programs")
parser.add_argument("--info", action="store_true", help="prints out information of this project package")

args = parser.parse_args()
'''
HACB.zip --program HAL1002UT-A_P_LFP25C --lot 123456 --station 

{TARGET}_P_LF_P25C
	-die
	-product                                  P = + 25C
                           LF = Lead Frame	  N = - 40C
		P = Production     SD = Singulated Die     P170C
		E = Engineering
		Q = Qualifiaction
			-ESD
			-HALT
			...
		...
'''
if args.info:
    print("info")
