from ..constance import Params
from .avatar import AvatarAPI
from .different import DifferentAPI
from .dm_im import DmImAPI
from .folders import FoldersAPI
from .groups import GroupsAPI
from .polls import PollsAPI
from .rooms import RoomsAPI
from .supergroups import SuperGroupsAPI
from .testing import TestingAPI # noqa
from .users import UsersAPI
from .chat import ChatAPI
from .threads import ThreadAPI
from .config import Settings


class ClientAPI():
    def __init__(self, session):
        self.session = session
        self.base_url = Params.REMOTE_URL
        self.settings = Settings(config_file='settings.ini')
        self.avatar = AvatarAPI(self)
        self.dm_im = DmImAPI(self)
        self.groups = GroupsAPI(self)
        self.polls = PollsAPI(self)
        self.rooms = RoomsAPI(self)
        self.supergroups = SuperGroupsAPI(self)
        self.folders = FoldersAPI(self)
        self.users = UsersAPI(self)
        self.different = DifferentAPI(self)
        self.chat = ChatAPI(self)
        self.threds = ThreadAPI(self)
