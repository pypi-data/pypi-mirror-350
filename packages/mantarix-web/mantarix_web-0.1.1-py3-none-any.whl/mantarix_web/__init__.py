import os
from pathlib import Path

from mantarix_web.patch_index import patch_index_html, patch_manifest_json


def get_package_web_dir():
    web_root_dir = os.environ.get("MANTARIX_WEB_PATH")
    return web_root_dir or str(Path(__file__).parent.joinpath("web"))
