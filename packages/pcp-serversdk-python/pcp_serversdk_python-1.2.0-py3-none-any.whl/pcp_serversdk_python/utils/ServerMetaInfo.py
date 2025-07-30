import platform


class ServerMetaInfo:
    def __init__(self, integrator: str = ""):
        self.platformIdentifier = (
            f"{platform.system()}, Python version is: {platform.python_version()}"
        )
        self.sdkIdentifier = "PythonServerSDK/v1.2.0"  # Update version as needed
        self.sdkCreator = "PAYONE GmbH"
        self.integrator = integrator
