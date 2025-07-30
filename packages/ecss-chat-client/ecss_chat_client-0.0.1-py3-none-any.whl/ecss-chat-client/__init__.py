"""
ECSS Chat Client - Python клиент для ECSS Chat
"""

from .auth import Auth
from .avatar import Avatar
from .chat import Chat
from .config import Settings
from .different import Different
from .dm_im import DmIm
from .folders import Folders
from .groups import Groups
from .polls import Polls
from .rooms import Rooms
from .supergroups import SuperGroups
from .testing import Testing
from .threds import Thread
from .users import Users


class Client:
    def __init__(self, server, username, password):
        self.username = username
        self.password = password
        self.base_url = f'https://{server}:3443/api/v1'
        self.short_url = f'https://{server}:3443/api'

        self.settings = Settings(
            server, config_file='settings.ini',
        )

        self.session = Auth.session(self, username, password)
        self.avatar = Avatar(self)
        self.dm_im = DmIm(self)
        self.groups = Groups(self)
        self.polls = Polls(self)
        self.rooms = Rooms(self)
        self.supergroups = SuperGroups(self)
        self.folders = Folders(self)
        self.users = Users(self)
        self.different = Different(self)
        self.chat = Chat(self)
        self.threds = Thread(self)
        self.testing = Testing(self)


__all__ = ['Client']
__version__ = '0.1.0'
__author__ = 'Eltex SC VoIP - maxstolpovskikh'
__description__ = 'ElphChat API Client Library'
