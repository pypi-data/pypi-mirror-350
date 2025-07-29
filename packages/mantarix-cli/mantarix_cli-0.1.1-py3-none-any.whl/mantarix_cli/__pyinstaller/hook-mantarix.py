import os

import mantarix_cli.__pyinstaller.config as hook_config
from mantarix_cli.__pyinstaller.utils import get_mantarix_bin_path

bin_path = hook_config.temp_bin_dir
if not bin_path:
    bin_path = get_mantarix_bin_path()

if bin_path:
    # package "bin/mantarixd" only
    if os.getenv("PACKAGE_MANTARIXD_ONLY"):
        bin_path = os.path.join(bin_path, "mantarixd*")

    datas = [(bin_path, "mantarix/bin")]
