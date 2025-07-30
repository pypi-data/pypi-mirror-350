import os
import importlib.metadata

# DO NOT EDIT
__pkg_version__ = importlib.metadata.version("weco")
__api_version__ = "v1"

__base_url__ = f"https://api.weco.ai/{__api_version__}"
# If user specifies a custom base URL, use that instead
if os.environ.get("WECO_BASE_URL"):
    __base_url__ = os.environ.get("WECO_BASE_URL")

__dashboard_url__ = "https://dashboard.weco.ai"
if os.environ.get("WECO_DASHBOARD_URL"):
    __dashboard_url__ = os.environ.get("WECO_DASHBOARD_URL")
