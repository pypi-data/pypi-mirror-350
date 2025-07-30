from pathlib import Path
from typing import List

from .lib import Base


class SuperGroups(Base):
    def create(self, name: str, members: List, topics: List):
        return self._make_request('supergroups.create', payload={
            'supergroups': [
                {
                    'fname': name,
                    'members': members,
                    'topics': topics,
                }
            ]
        })

    def add_topics(self, room_id: str, new_topic_name: str):
        return self._make_request('supergroups.addTopics', payload={
            'roomId': room_id,
            'topics': [
                {
                    'fname': new_topic_name,
                }
            ]
        })

    def remove_topics(self, room_id: str, topics: List[str]):
        return self._make_request('supergroups.removeTopics', payload={
            'roomId': room_id,
            'topicIds': topics
        })

    def get_topics(self, room_id: str):
        return self._make_request(
            'supergroups.topics',
            params={
                'roomId': room_id,
                'sequence': 0,
                'limit': 50
            },
            method='get'
        )

    def edit_topic(self, topic_id: str, new_topic_name: str):
        return self._make_request('supergroups.editTopics', payload={
            'topics': [
                {
                    '_id': topic_id,
                    'fname': new_topic_name
                }
            ]
        })

    def invite(self, room_id: str, user_ids: List[str]):
        return self._make_request('supergroups.invite', payload={
            'roomId': room_id,
            'userIds': user_ids
        })

    def set_avatar(self, sgp_id: str, file: Path):
        files = {'file': open(file, 'rb')}
        return self._make_request(
            f'supergroups.setAvatar/{sgp_id}', files=files
        )

    def rename(self, sgp_id: str, new_name: str):
        return self._make_request('supergroups.rename', payload={
            'roomId': sgp_id,
            'name': new_name
        })

    def add_owner(self, sgp_id: str, user_id: str):
        return self._make_request('supergroups.addOwner', payload={
            'roomId': sgp_id,
            'userId': user_id
        })

    def remove_owner(self, sgp_id: str, user_id: str):
        return self._make_request('supergroups.removeOwner', payload={
            'roomId': sgp_id,
            'userId': user_id
        })

    def convert_to_group(self, sgp_id: str):
        return self._make_request(
            'supergroups.convertToGroup', payload={'roomId': sgp_id}
        )
