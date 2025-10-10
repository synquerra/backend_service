from dotenv import dotenv_values


class APAARClientsAuth:
    """
    mapping *_CLIENT_ID to *_CLIENT_SECRET values.
    """

    @classmethod
    def _load_dynamic_client_keys(cls) -> dict:
        """
        Extracts all client_id and client_secret pairs from environment variables.

        Returns:
            dict: A mapping of client_id to client_secret.
        """
        env_vars = dotenv_values(".env.auth.credentials")
        client_map = {}
        temp_map = {}

        for key, value in env_vars.items():
            if key.endswith("_CLIENT_ID"):
                temp_map["id"] = value
            elif key.endswith("_CLIENT_SECRET"):
                temp_map["secret"] = value

            # When both id and secret are available, store and reset
            if "id" in temp_map and "secret" in temp_map:
                client_map[temp_map["id"]] = temp_map["secret"]
                temp_map.clear()

        return client_map

    @classmethod
    def get_all(cls) -> dict:
        """
        Returns all client credentials as a dictionary {client_id: client_secret}.
        """
        return cls._load_dynamic_client_keys()

    @classmethod
    def get_secret_by_client_id(cls, client_id: str) -> str | None:
        """
        Fetches the client secret for a given client ID.

        Args:
            client_id (str): The client ID.

        Returns:
            str | None: The corresponding client secret, or None if not found.
        """
        return cls.get_all().get(client_id)
