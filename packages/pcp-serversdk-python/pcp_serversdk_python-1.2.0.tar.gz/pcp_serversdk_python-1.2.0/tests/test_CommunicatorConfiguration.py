from pcp_serversdk_python.CommunicatorConfiguration import (
    CommunicatorConfiguration,
)  # Update import as needed


def test_communicator_configuration_initialization():
    api_key = "testApiKey"
    api_secret = "testApiSecret"
    host = "https://example.com"

    config = CommunicatorConfiguration(
        api_key=api_key, api_secret=api_secret, host=host
    )

    # Check initialization
    assert config.api_key == api_key
    assert config.api_secret == api_secret
    assert config.host == host


def test_get_api_key():
    api_key = "testApiKey"
    config = CommunicatorConfiguration(
        api_key=api_key, api_secret="testApiSecret", host="https://example.com"
    )

    # Check get_api_key method
    assert config.get_api_key() == api_key


def test_get_api_secret():
    api_secret = "testApiSecret"
    config = CommunicatorConfiguration(
        api_key="testApiKey", api_secret=api_secret, host="https://example.com"
    )

    # Check get_api_secret method
    assert config.get_api_secret() == api_secret


def test_get_host():
    host = "https://example.com"
    config = CommunicatorConfiguration(
        api_key="testApiKey", api_secret="testApiSecret", host=host
    )

    # Check get_host method
    assert config.get_host() == host
