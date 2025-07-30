from importlib.metadata import version

SERVER_TPL = "https://{}.e2.earnix.com"

PACKAGE_VERSION = version("earnix_elevate")

USER_AGENT = f"Earnix-Elevate-SDK-Python/{PACKAGE_VERSION}"
