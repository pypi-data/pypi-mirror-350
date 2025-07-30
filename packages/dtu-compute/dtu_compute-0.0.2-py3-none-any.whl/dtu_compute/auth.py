import keyring
import typer


class AuthManager:
    """Class to manage authentication for DTU Compute.

    Args:
        auth_method (str): The authentication method to use. Supported methods are 'password' and 'keyring'.

    """

    def __init__(self, auth_method: str) -> None:
        if auth_method not in ["password", "keyring"]:
            raise ValueError(
                f"Invalid authentication method: {auth_method}. Supported methods are 'password' and 'keyring'."
            )
        self.auth_method = auth_method

    def setup_auth(self, username: str, password: str) -> None:
        """Set up authentication data and save it to the auth file.

        Args:
            username: DTU Compute username
            password: DTU Compute password

        """
        if self.auth_method == "keyring":
            keyring.set_password("dtu_compute", username, password)
        elif self.auth_method == "password":
            # No action needed for password method
            pass

    def get_auth(self, username: str) -> str | None:
        """Retrieve the password for the given username.

        Args:
            username: DTU Compute username

        Returns:
            The password for the given username.

        """
        if self.auth_method == "keyring":
            return keyring.get_password("dtu_compute", username)
        return typer.prompt("Enter your DTU Compute password", type=str, hide_input=True)

    def delete_auth(self, username: str) -> None:
        """Delete the authentication data for the given username.

        Args:
            username: DTU Compute username

        """
        if self.auth_method == "keyring":
            keyring.delete_password("dtu_compute", username)
        elif self.auth_method == "password":
            # No action needed for password method
            pass
