import keyring
import getpass


PROG = "marmoset"


class DuplicateUserException(Exception):
    pass


class NoUserException(Exception):
    pass


def user_exists(username):
    """
    Determines if the specified user exists in the keyring for Marmoset.

    @param username: user's name, a string.
    @return: boolean
    """
    current = getpass.getuser()
    users = keyring.get_password(PROG, current)
    # Note: this uses the fact that certain characters are not allowed in Quest usernames
    # if this changes, this code should be rewritten to accomodate that
    if not users:
        keyring.set_password(PROG, current, "")
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
    keyring.set_password(PROG, username, password)
    current = getpass.getuser()
    # Add user to the list of Marmoset users for the current user
    users = keyring.get_password(PROG, current)
    users += "%s," % username
    keyring.set_password(PROG, current, users)


def get_user_info(username=None):
    """
    Gets the username/password for the specified user, otherwise the currently
    logged in user.

    @param username: optional username
    @return: tuple
    """
    users = keyring.get_password(PROG, getpass.getuser())
    if not users:
        keyring.set_password(PROG, getpass.getuser(), "")
        return (username, None)

    users = users.split(",")
    if username and username in users:
        return (username, keyring.get_password(PROG, username))
    elif not username and len(users) > 0:
        return (users[0], keyring.get_password(PROG, users[0]))
    return (username, None)


def change_default_user(username):
    """
    Changes the default user for the app keyring.

    @param username: user's name, a string.
    @return: None
    """
    if not username:
        raise NoUserException("Error: expected a username, given None.")
    if not user_exists(username):
        raise NoUserException("Error: %s is not a valid user."% username)

    # Get the current user list and rearrange
    current = getpass.getuser()
    users = keyring.get_password(PROG, current)
    users = users.split(",")
    users = [username] + users.remove(username)
    keyring.set_password(PROG, current, users)
