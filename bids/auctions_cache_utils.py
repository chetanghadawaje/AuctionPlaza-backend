import logging

from django_redis import get_redis_connection

cache = get_redis_connection('default')
logger = logging.getLogger(__name__)


class BidCaches:

    @classmethod
    def live_user_added(cls, bid_id: str, user_id: int, ttl: int = 10) -> None:
        """
        This function is used to maintain live user information
        ttl is set default is 10 seconds.
        """
        flag = cache.set(f"live_{bid_id}_{str(user_id)}", str(user_id), ttl)
        logger.info(f"Live user information added to cache. Flag: {flag} | Bid: {bid_id} | User: {user_id}")

    @classmethod
    def live_user_count(cls, bid_id: str) -> int:
        """
        This function is used to get how may live user for bids
        """
        list_user = cache.get(f"live_{bid_id}*")
        live_count = len(list_user)
        return live_count

    @classmethod
    def create_list_for_bids(cls, bid_id: str, user_id: int, user_data: dict) -> None:
        """
        This function create list for all bids user in live time
        """
        flag = cache.hmset(f'user_bid_{bid_id}_{str(user_id)}', user_data)
        logger.info(f"Bid related data added in cache. Flag: {flag} | Bid: {bid_id} | User: {user_data}")

    @classmethod
    def get_list_of_bid(cls, bid_id: str):
        """
        This function get list for bids
        """
        list_user_bids = cache.get(f'user_bid_{bid_id}_*')
        list_of_data = [cache.get(bid) for bid in list_user_bids]
        return list_of_data
