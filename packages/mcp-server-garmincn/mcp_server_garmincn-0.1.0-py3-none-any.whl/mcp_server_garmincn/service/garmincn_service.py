from garminconnect import *
from garth.exc import GarthHTTPError
from requests import HTTPError

import os


class GarminService:

    def __init__(self):
        self.email: str | None = os.getenv("EMAIL") or None
        self.password: str = os.getenv("PASSWORD") or None
        self.tokenstore: str = os.getenv("GARMINTOKENS") or "~/.garminconnect"
        self.tokenstore_base64: str  = os.getenv("GARMINTOKENS_BASE64") or "~/.garminconnect_base64"

    def get_mfa(self):
        """Get MFA."""

        return input("MFA one-time code: ")

    def init_api(self):

        try:
            self.garmin = Garmin()
            self.garmin.login(self.tokenstore)
        except (FileNotFoundError, GarthHTTPError, GarminConnectAuthenticationError):
            try:
                self.garmin = Garmin(email=self.email, password=self.password, is_cn=True, return_on_mfa=True)
                result1, result2 = self.garmin.login()
                if result1 == "needs_mfa":  # MFA is required
                    mfa_code = self.get_mfa()
                    self.garmin.resume_login(result2, mfa_code)

                # Save Oauth1 and Oauth2 token files to directory for next login
                self.garmin.garth.dump(self.tokenstore)
                print(
                    f"Oauth tokens stored in '{self.tokenstore}' directory for future use. (first method)\n"
                )

                # Encode Oauth1 and Oauth2 tokens to base64 string and safe to file for next login (alternative way)
                token_base64 = self.garmin.garth.dumps()
                dir_path = os.path.expanduser(self.tokenstore_base64)
                with open(dir_path, "w") as token_file:
                    token_file.write(token_base64)
                print(
                    f"Oauth tokens encoded as base64 string and saved to '{dir_path}' file for future use. (second method)\n"
                )

                # Re-login Garmin API with tokens
                self.garmin.login(self.tokenstore)
                return True
            except (
                FileNotFoundError,
                GarthHTTPError,
                GarminConnectAuthenticationError,
                HTTPError,
            ) as err:
                logger.error(err)
                return None

        return True

    @property
    def garminapi(self):
        return self.garmin
