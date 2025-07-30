import uuid
from typing import List

from .lib import Base


class Chat(Base):
    def send_message(self, text: str, room_id: str):
        _uuid = str(uuid.uuid4())
        return self._make_request(
            'chat.sendMessage', payload={
                'message': {
                    'rid': room_id,
                    'msg': text,
                    '_id': _uuid,
                }
            }
        ), _uuid

    def message_reply(self, text: str, room_id: str, message_id: str):
        return self._make_request(
            'chat.sendMessage', payload={
                'message': {
                    'rid': room_id,
                    'msg': text,
                    'toReplyId': message_id,
                }
            }
        )

    def forward_message(
            self,
            room_id: str,
            to_room_id: str,
            message_ids: List[str],
            updated_ids: List[str],
    ):
        return self._make_request(
            'chat.forwardMessages', payload={
                'roomId': room_id,
                'toForwardRoomId': to_room_id,
                'toForwardIds': message_ids,
                'forwardedIds': updated_ids,
            }
        )

    def load_message_history(self, room_id: str):
        return self._make_request(
            'chat.loadMessageHistory', payload={'roomId': room_id}
        )

    def pin(self, message_id: str):
        return self._make_request(
            'chat.pinMessage', payload={'messageId': message_id}
        )

    def unpin(self, message_id: str):
        return self._make_request(
            'chat.unPinMessage', payload={'messageId': message_id}
        )

    def get_by_id(self, message_id: str):
        return self._make_request(
            'chat.getMessage', params={'msgId': message_id}, method='get'
        )

    def get_pinned(self, room_id: str):
        return self._make_request(
            'chat.getPinnedMessages',
            params={
                'roomId': room_id,
                'offset': self.settings.offset,
                'count': self.settings.count,
            },
            method='get'
        )

    def react(
            self,
            emoji: str,
            message_id: str,
            room_id: str,
            should_react: bool
    ):
        return self._make_request(
            'chat.react', payload={
                'emoji': emoji,
                'messageId': message_id,
                'roomId': room_id,
                'shouldReact': should_react,
            }
        )

    def get_reactions(
            self,
            message_id: str,
            room_id: str,
    ):
        return self._make_request(
            'chat.messageReactions',
            params={
                'msgId': message_id,
                'roomId': room_id,
                'offset': self.settings.offset,
                'count': self.settings.count,
            },
            method='get'
        )

    def search(self, text: str, room_id: str):
        return self._make_request(
            'chat.search',
            params={
                'searchText': text,
                'roomId': room_id,
            },
            method='get'
        )

    def read_users(
            self,
            message_id: str,
            room_id: str,
    ):
        return self._make_request(
            'chat.messageReadUsers',
            params={
                'msgId': message_id,
                'roomId': room_id,
                'count': self.settings.count,
                'offset': self.settings.offset,
            },
            method='get'
        )

    def draft_post(self, room_id: str, text: str):
        return self._make_request('chat.draft', payload={
            'roomId': room_id,
            'msg': text,
            'mode': {
                'type': "none",
                'data': None
            },
        })

    def draft_get(self, room_id: str):
        return self._make_request(
            'chat.draft', params={'roomId': room_id}, method='get'
        )
