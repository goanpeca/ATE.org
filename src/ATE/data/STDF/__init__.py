import sys

python_version = sys.verion_info
if python_version.major < 3:
    raise Exception("The STDF library is made for Python 3")
elif python_version.minor < 6:
    raise Exception("The STDF library is made for Python >= 3.6")

