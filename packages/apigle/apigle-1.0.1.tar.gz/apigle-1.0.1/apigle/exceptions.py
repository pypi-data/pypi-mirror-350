class MissingAPIKeyError(Exception):
    def __init__(self):
        super().__init__(
            "API key is missing. Set it using ApigleClient.set_api_key().\n"
            "Visit https://apigle.com to get your API key."
        )
