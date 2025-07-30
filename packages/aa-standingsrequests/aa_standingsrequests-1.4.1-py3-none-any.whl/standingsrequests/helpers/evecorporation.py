from concurrent.futures import ThreadPoolExecutor
from typing import Iterable, List, Optional

from bravado.exception import HTTPError

from django.contrib.auth.models import User
from django.core.cache import cache
from eveuniverse.models import EveEntity

from allianceauth.eveonline.evelinks import eveimageserver
from allianceauth.eveonline.models import EveCharacter
from allianceauth.services.hooks import get_extension_logger
from app_utils.logging import LoggerAddTag

from standingsrequests import __title__
from standingsrequests.constants import DEFAULT_IMAGE_SIZE
from standingsrequests.providers import esi

logger = LoggerAddTag(get_extension_logger(__name__), __title__)

MAX_WORKERS = 10


class EveCorporation:
    CACHE_PREFIX = "STANDINGS_REQUESTS_EVECORPORATION_"
    CACHE_TIME = 60 * 60  # 60 minutes

    def __init__(self, **kwargs):
        self.corporation_id = int(kwargs.get("corporation_id", 0))
        self.corporation_name = kwargs.get("corporation_name")
        self.ticker = kwargs.get("ticker")
        self.member_count = kwargs.get("member_count")
        self.ceo_id = kwargs.get("ceo_id")
        self.alliance_id = kwargs.get("alliance_id")
        self.alliance_name = kwargs.get("alliance_name")

    def __str__(self):
        return self.corporation_name

    def __eq__(self, o: "EveCorporation") -> bool:
        return (
            isinstance(o, type(self))
            and self.corporation_id == o.corporation_id
            and self.corporation_name == o.corporation_name
            and self.ticker == o.ticker
            and self.member_count == o.member_count
            and self.ceo_id == o.ceo_id
            and self.alliance_id == o.alliance_id
            and self.alliance_name == o.alliance_name
        )

    @property
    def is_npc(self) -> bool:
        """returns true if this corporation is an NPC, else false"""
        return self.corporation_is_npc(self.corporation_id)

    @staticmethod
    def corporation_is_npc(corporation_id: int) -> bool:
        """returns true if this corporation is an NPC, else false"""
        return 1000000 <= corporation_id <= 2000000

    def logo_url(self, size: int = DEFAULT_IMAGE_SIZE) -> str:
        return eveimageserver.corporation_logo_url(self.corporation_id, size)

    def member_tokens_count_for_user(
        self, user: User, quick_check: bool = False
    ) -> int:
        """returns the number of character tokens the given user owns
        for this corporation

        Params:
        - user: user owning the characters
        - quick: if True will not check if tokens are valid to save time
        """
        from standingsrequests.models import StandingRequest

        corporation_members = (
            EveCharacter.objects.filter(character_ownership__user=user)
            .select_related("character_ownership__user__profile__state")
            .filter(corporation_id=self.corporation_id)
        )

        return sum(
            (
                1
                if StandingRequest.has_required_scopes_for_request(
                    character=character, user=user, quick_check=quick_check
                )
                else 0
            )
            for character in corporation_members
        )

    def user_has_all_member_tokens(self, user: User, quick_check: bool = False) -> bool:
        """returns True if given user owns same amount of token than there are
        member characters in this corporation, else False

        Params:
        - user: user owning the characters
        - quick: if True will not check if tokens are valid to save time
        """
        return (
            self.member_count is not None
            and self.member_tokens_count_for_user(user=user, quick_check=quick_check)
            >= self.member_count
        )

    @classmethod
    def get_by_id(
        cls, corporation_id: int, ignore_cache: bool = False
    ) -> Optional["EveCorporation"]:
        """Get a corporation from the cache or ESI if not cached
        Corps are cached for 3 hours

        Params
        - corporation_id: int corporation ID to get
        - ignore_cache: when true will always get fresh from API

        Returns corporation object or None
        """
        logger.debug("Getting corporation by id %d", corporation_id)
        my_cache_key = cls._get_cache_key(corporation_id)
        corporation = cache.get(my_cache_key)
        if corporation is None or ignore_cache:
            logger.debug("Corp not in cache or ignoring cache, fetching")
            corporation = cls.fetch_corporation_from_api(corporation_id)
            if corporation is not None:
                cache.set(my_cache_key, corporation, cls.CACHE_TIME)
        else:
            logger.debug("Retrieving corporation %s from cache", corporation_id)
        return corporation

    @classmethod
    def _get_cache_key(cls, corporation_id: int) -> str:
        return cls.CACHE_PREFIX + str(corporation_id)

    @classmethod
    def fetch_corporation_from_api(
        cls, corporation_id: int
    ) -> Optional["EveCorporation"]:
        logger.debug(
            "Attempting to fetch corporation from ESI with id %s", corporation_id
        )
        try:
            info = esi.client.Corporation.get_corporations_corporation_id(
                corporation_id=corporation_id
            ).results()
        except HTTPError:
            logger.exception(
                "Failed to fetch corporation from ESI with id %i", corporation_id
            )
            return None

        args = {
            "corporation_id": corporation_id,
            "corporation_name": info["name"],
            "ticker": info["ticker"],
            "member_count": info["member_count"],
            "ceo_id": info["ceo_id"],
        }
        if "alliance_id" in info and info["alliance_id"]:
            args["alliance_id"] = info["alliance_id"]
            args["alliance_name"] = EveEntity.objects.resolve_name(info["alliance_id"])

        return cls(**args)

    @classmethod
    def get_many_by_id(cls, corporation_ids: Iterable[int]) -> List["EveCorporation"]:
        """Returns multiple corporations by ID

        Fetches requested corporations from cache or API as needed.
        Uses threads to fetch them in parallel.
        """
        corporation_ids_unique = set(corporation_ids)
        if not corporation_ids_unique:
            return []

        # make sure client is loaded before starting threads
        esi.client.Status.get_status().results()
        logger.info(
            "Starting to fetch the %d corporations from ESI with up to %d workers",
            len(corporation_ids_unique),
            MAX_WORKERS,
        )
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = [
                executor.submit(cls.get_by_id, corporation_id)
                for corporation_id in corporation_ids_unique
            ]
            logger.info("Waiting for all threads fetching corporations to complete...")

        logger.info(
            "Completed fetching %d corporations from ESI", len(corporation_ids_unique)
        )
        results_raw = (f.result() for f in futures)
        results = [obj for obj in results_raw if obj is not None]
        return results
