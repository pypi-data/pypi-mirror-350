from .lib import Base


class Thread(Base):
    def create(self, message_id: str, room_id: str):
        return self._make_request(
            'thread.createOrJoinWithMessage', payload={
                'mid': message_id,
                'roomId': room_id,
            }
        )
