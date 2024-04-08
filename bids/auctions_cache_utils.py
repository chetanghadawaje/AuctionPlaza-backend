import json
from typing import List, Any

from django_redis import get_redis_connection


cache = get_redis_connection('default')


class BidCaches:
    @classmethod
    def create_list_for_bids(cls, bid_id: str, user_data: dict) -> None:
        """
        This function create list for all bids user in live time
        """
        cache.hmset(f'user_bid_{bid_id}', user_data)

    @classmethod
    def get_list_for_bids(cls, bid_id: str) -> list[Any]:
        """
        This function get list for bids
        """
        list_of_bids = cache.hgetall(f"user_bid_{bid_id}")
        print(list_of_bids)
        return [json.loads(entry) for entry in list_of_bids]

