import keyring
import getpass


class DuplicateUserException(Exception):
    pass


def user_exists(username):
    """
    Determines if the specified user exists in the keyring for Marmoset.

    @param username: user's name, a string.
    @return: boolean
    """
    current = getpass.getuser()
    users = keyring.get_password("marmoset", current)
    # Note: this uses the fact that certain characters are not allowed in Quest usernames
    # if this changes, this code should be rewritten to accomodate that
    if not users:
        keyring.set_password("marmoset", current, "")
        return False
    users = users.split(",")
    return (username in  users)


def store_user_info(username, password):
    """
    Uses keyring to store the user's username and password for their marmoset
    instance provided this is a new user and they want to store this information.

    @param username: user's name, a string.
    @param password: user's password, a string.
    @return: None
    """
    # Store the user's information
    # Important: We don't check to ensure the user isn't overwriting
    keyring.set_password("marmoset", username, password)
    current = getpass.getuser()
    # Add user to the list of Marmoset users for the current user
    users = keyring.get_password("marmoset", current)
    users += "%s," % username
    keyring.set_password("marmoset", current, users)


def get_user_info(username=None):
    """
    Gets the username/password for the specified user, otherwise the currently
    logged in user.

    @param username: optional username
    @return: tuple
    """
    users = keyring.get_password("marmoset", getpass.getuser())
    if not users:
        return (username, None)

    users = users.split(",")
    if username and username in users:
        return (username, keyring.get_password("marmoset", username))
    elif not username:
        return (users[0], keyring.get_password("marmoset", users[0]))
    return (username, None)

