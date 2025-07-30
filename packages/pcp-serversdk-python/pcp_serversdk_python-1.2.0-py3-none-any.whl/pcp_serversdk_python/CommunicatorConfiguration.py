class CommunicatorConfiguration:
    def __init__(self, api_key: str, api_secret: str, host: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.host = host

    def get_api_key(self) -> str:
        return self.api_key

    def get_api_secret(self) -> str:
        return self.api_secret

    def get_host(self) -> str:
        return self.host
