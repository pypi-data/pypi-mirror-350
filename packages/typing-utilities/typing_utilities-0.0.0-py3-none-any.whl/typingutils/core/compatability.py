# pragma: no cover
from sys import version_info

PYTHON_310 = version_info.major == 3 and version_info.minor == 10
PYTHON_LT_310 = version_info.major == 3 and version_info.minor < 10
PYTHON_GTE_310 = version_info.major == 3 and version_info.minor >= 10
PYTHON_311 = version_info.major == 3 and version_info.minor == 11
PYTHON_GTE_311 = version_info.major == 3 and version_info.minor >= 11
PYTHON_312 = version_info.major == 3 and version_info.minor == 12
PYTHON_GTE_312 = version_info.major == 3 and version_info.minor >= 12
PYTHON_313 = version_info.major == 3 and version_info.minor == 13
PYTHON_GTE_313 = version_info.major == 3 and version_info.minor >= 13
PYTHON_GTE_314 = version_info.major == 3 and version_info.minor >= 14
PYTHON_SUPPORTED = PYTHON_GTE_310