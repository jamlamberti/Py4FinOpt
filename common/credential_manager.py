"""Holds creds for the database"""
import os


class CredentialManager(object):

    """Creds for a database connection"""
    # TODO: Switched to a named tuple
    # pylint: disable=too-many-arguments, too-few-public-methods

    def __init__(
            self,
            host=None,
            user=None,
            passwd=None,
            name='example.db',
            port=3306):

        self.db_host = host
        self.db_user = user
        self.db_pass = passwd

        if host is None:
            self.db_name = os.path.abspath(name)
        else:
            self.db_name = name

        self.port = port
