from zenetics.api.zenetics_api_client import ZeneticsAPIClient


class SetupChecker:
    """
    This class is responsible for checking the connection to all required services.
    """

    def __init__(self, zenetics_api_client: ZeneticsAPIClient) -> None:
        self.zenetics_api_client = zenetics_api_client

    def check_zenetics_api_connection(self) -> bool:
        """
        Check the connection to the Zenetics API.
        """
        return self.zenetics_api_client.check_connection()
