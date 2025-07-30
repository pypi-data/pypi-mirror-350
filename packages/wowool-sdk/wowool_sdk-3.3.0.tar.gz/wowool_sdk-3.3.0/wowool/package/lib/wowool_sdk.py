from pathlib import Path
import os
import sys


if "WOWOOL_ROOT" in os.environ:
    WOWOOL_ROOT = os.environ["WOWOOL_ROOT"]
    expanded_eot_root = Path(WOWOOL_ROOT).expanduser().resolve()
    import platform

    if platform.system() == "Windows":
        WOWOOL_LIB = expanded_eot_root / "bin"
        if str(WOWOOL_LIB) not in sys.path:
            sys.path.append(str(WOWOOL_LIB))
    WOWOOL_LIB = expanded_eot_root / "lib"
else:
    WOWOOL_LIB = Path(__file__).resolve().parent
    os.environ["WOWOOL_ROOT"] = str(WOWOOL_LIB.parent)

if str(WOWOOL_LIB) not in sys.path:
    sys.path.append(str(WOWOOL_LIB))

if "WOWOOL_LICENSE_FILE" not in os.environ:
    lic_fn = WOWOOL_LIB.parent / "lxware" / "lic.dat"
    if lic_fn.exists():
        os.environ["WOWOOL_LICENSE_FILE"] = str(lic_fn)

from _wowool_sdk import *  # noqa
