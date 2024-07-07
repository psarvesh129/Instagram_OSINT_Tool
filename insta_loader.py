import instaloader
from helpers import get_random_user_agent

class InstaLoaderWrapper:
    def __init__(self):
        self.loader = instaloader.Instaloader()

    def login(self, username, password):
        self.loader.context._session.headers.update({'User-Agent': get_random_user_agent()})
        try:
            self.loader.load_session_from_file(username)
            return "Logged in successfully using existing session."
        except FileNotFoundError:
            try:
                self.loader.login(username, password)
                self.loader.save_session_to_file()
                return "Logged in successfully."
            except instaloader.exceptions.BadCredentialsException:
                raise ValueError("Incorrect username or password.")
            except instaloader.exceptions.ConnectionException:
                raise ConnectionError("Connection error occurred.")
            except Exception as e:
                raise e

    def get_profile(self, username):
        try:
            profile = instaloader.Profile.from_username(self.loader.context, username)
            return profile
        except instaloader.exceptions.ProfileNotExistsException:
            raise ValueError("Profile does not exist.")
        except instaloader.exceptions.ConnectionException:
            raise ConnectionError("Connection error occurred.")
        except Exception as e:
            raise e
# GPCSSI2024CW407