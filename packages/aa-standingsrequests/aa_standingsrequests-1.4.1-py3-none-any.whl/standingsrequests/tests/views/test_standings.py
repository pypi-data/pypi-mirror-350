import datetime as dt
from unittest.mock import patch

from django.test import RequestFactory, TestCase
from django.urls import reverse
from django.utils.timezone import now
from eveuniverse.models import EveEntity

from allianceauth.eveonline.models import EveAllianceInfo, EveCharacter
from allianceauth.tests.auth_utils import AuthUtils
from app_utils.testing import add_character_to_user

from standingsrequests.core.contact_types import ContactTypeId
from standingsrequests.models import CharacterAffiliation, Contact, StandingRequest
from standingsrequests.tests.testdata.my_test_data import (
    create_contacts_set,
    create_eve_objects,
    load_corporation_details,
    load_eve_entities,
)
from standingsrequests.tests.utils import PartialDictEqualMixin, json_response_to_dict_2
from standingsrequests.views import standings
from standingsrequests.views.standings import _identify_main_for_character

TEST_SCOPE = "publicData"
MODULE_PATH = "standingsrequests.views.standings"


@patch("standingsrequests.core.app_config.STANDINGS_API_CHARID", 1001)
class TestStandingsView(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.factory = RequestFactory()
        load_eve_entities()
        create_eve_objects()
        cls.contact_set = create_contacts_set()
        CharacterAffiliation.objects.update_evecharacter_relations()

        cls.user = AuthUtils.create_member("John Doe")
        cls.user = AuthUtils.add_permission_to_user_by_name(
            "standingsrequests.request_standings", cls.user
        )

    def test_can_open_standings_page(self):
        # given
        request = self.factory.get(reverse("standingsrequests:standings"))
        request.user = self.user
        # when
        response = standings.standings(request)
        # then
        self.assertEqual(response.status_code, 200)


class TestCharacterStandingsData(PartialDictEqualMixin, TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.factory = RequestFactory()
        load_eve_entities()
        create_eve_objects()
        cls.contact_set = create_contacts_set()
        CharacterAffiliation.objects.update_evecharacter_relations()

        member_state = AuthUtils.get_member_state()
        member_state.member_alliances.add(EveAllianceInfo.objects.get(alliance_id=3001))
        cls.user = AuthUtils.create_member("John Doe")
        cls.user = AuthUtils.add_permission_to_user_by_name(
            "standingsrequests.request_standings", cls.user
        )
        EveCharacter.objects.get(character_id=1009).delete()
        cls.main_character_1 = EveCharacter.objects.get(character_id=1002)
        cls.user_1 = AuthUtils.create_member(cls.main_character_1.character_name)
        add_character_to_user(
            cls.user_1,
            cls.main_character_1,
            is_main=True,
            scopes=[TEST_SCOPE],
        )
        cls.alt_character_1 = EveCharacter.objects.get(character_id=1007)
        add_character_to_user(
            cls.user_1,
            cls.alt_character_1,
            scopes=[TEST_SCOPE],
        )

    def test_normal_with_full_permissions(self):
        # given
        self.user = AuthUtils.add_permission_to_user_by_name(
            "standingsrequests.view", self.user
        )
        self.maxDiff = None
        request = self.factory.get(
            reverse("standingsrequests:character_standings_data")
        )
        request.user = self.user
        my_view_without_cache = standings.character_standings_data.__wrapped__
        # when
        response = my_view_without_cache(request)
        # then
        self.assertEqual(response.status_code, 200)
        data = json_response_to_dict_2(response, "character_id")
        expected = {1001, 1002, 1003, 1004, 1005, 1006, 1008, 1009, 1010, 1110}
        self.assertSetEqual(set(data.keys()), expected)

        data_character_1002 = data[1002]
        expected = {
            "character_id": 1002,
            "corporation_name": "Wayne Technologies",
            "alliance_name": "Wayne Enterprises",
            "faction_name": "",
            "standing": 10.0,
            "labels_str": "blue, green",
            "main_character_name": "Peter Parker",
            "state": "Member",
        }
        self.assertPartialDictEqual(data_character_1002, expected)

        data_character_1009 = data[1009]
        expected = {
            "character_id": 1009,
            "corporation_name": "Lexcorp",
            "alliance_name": "",
            "faction_name": "",
            "standing": -10.0,
            "labels_str": "red",
            "main_character_name": "-",
            "state": "-",
        }
        self.assertPartialDictEqual(data_character_1009, expected)

    def test_normal_with_basic_permission(self):
        # given
        self.maxDiff = None
        request = self.factory.get(
            reverse("standingsrequests:character_standings_data")
        )
        request.user = self.user
        my_view_without_cache = standings.character_standings_data.__wrapped__
        # when
        response = my_view_without_cache(request)
        # then
        self.assertEqual(response.status_code, 200)
        data = json_response_to_dict_2(response, "character_id")
        expected = {1001, 1002, 1003, 1004, 1005, 1006, 1008, 1009, 1010, 1110}
        self.assertSetEqual(set(data.keys()), expected)

        data_character_1002 = data[1002]
        expected = {
            "character_id": 1002,
            "corporation_name": "Wayne Technologies",
            "alliance_name": "Wayne Enterprises",
            "faction_name": "",
            "standing": 10.0,
            "labels_str": "blue, green",
            "main_character_name": "",
            "state": "",
        }
        self.assertPartialDictEqual(data_character_1002, expected)

    def test_identify_main_works_without_main(self):
        # given
        character = EveCharacter.objects.get(character_id=1004)
        add_character_to_user(
            self.user,
            character,
            scopes=[TEST_SCOPE],
        )
        character_entity = EveEntity.objects.get(id=1004)
        contact = Contact.objects.create(
            contact_set=self.contact_set,
            eve_entity=character_entity,
            standing=10.0,
        )
        # checks that there's no main defined
        self.assertIsNone(self.user.profile.main_character)
        # when
        state, main_character_name, main_character_html = _identify_main_for_character(
            contact
        )
        # then
        self.assertEqual(main_character_name, "No main associated")
        self.assertEqual(main_character_html, "")
        self.assertEqual(
            state, "Member"
        )  # AuthUtils.create_member gives them Member by default


class TestCorporationStandingsData(PartialDictEqualMixin, TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.factory = RequestFactory()
        cls.contact_set = create_contacts_set()
        load_eve_entities()
        create_eve_objects()
        load_corporation_details()
        member_state = AuthUtils.get_member_state()
        member_state.member_alliances.add(EveAllianceInfo.objects.get(alliance_id=3001))
        cls.user_1 = AuthUtils.create_member("John Doe")
        cls.user_1 = AuthUtils.add_permission_to_user_by_name(
            "standingsrequests.request_standings", cls.user_1
        )
        EveCharacter.objects.get(character_id=1009).delete()
        cls.main_character_1 = EveCharacter.objects.get(character_id=1002)
        cls.user_2 = AuthUtils.create_member(cls.main_character_1.character_name)
        add_character_to_user(
            cls.user_2,
            cls.main_character_1,
            is_main=True,
            scopes=[TEST_SCOPE],
        )
        cls.alt_character_1 = EveCharacter.objects.get(character_id=1007)
        add_character_to_user(
            cls.user_2,
            cls.alt_character_1,
            scopes=[TEST_SCOPE],
        )
        StandingRequest.objects.create(
            user=cls.user_2,
            contact_id=2102,
            contact_type_id=ContactTypeId.CORPORATION,
            action_by=cls.user_1,
            action_date=now() - dt.timedelta(days=1, hours=1),
            is_effective=True,
            effective_date=now() - dt.timedelta(days=1),
        )

    def test_with_full_permissions(self):
        # given
        self.user_1 = AuthUtils.add_permission_to_user_by_name(
            "standingsrequests.view", self.user_1
        )
        self.maxDiff = None
        request = self.factory.get(
            reverse("standingsrequests:corporation_standings_data")
        )
        request.user = self.user_1
        my_view_without_cache = standings.corporation_standings_data.__wrapped__
        # when
        response = my_view_without_cache(request)
        # then
        self.assertEqual(response.status_code, 200)
        data = json_response_to_dict_2(response, "corporation_id")
        self.assertSetEqual(set(data.keys()), {2001, 2003, 2102})
        obj = data[2001]
        expected = {
            "corporation_id": 2001,
            "alliance_name": "Wayne Enterprises",
            "faction_name": "",
            "standing": 10.0,
            "state": "-",
            "main_character_name": "-",
        }
        self.assertPartialDictEqual(obj, expected)
        obj = data[2102]
        self.assertPartialDictEqual(
            obj,
            {
                "corporation_id": 2102,
                "alliance_name": "",
                "faction_name": "",
                "standing": -10.0,
                "state": "Member",
                "main_character_name": "Peter Parker",
            },
        )

    def test_with_basic_permissions(self):
        # given
        self.maxDiff = None
        request = self.factory.get(
            reverse("standingsrequests:corporation_standings_data")
        )
        request.user = self.user_1
        my_view_without_cache = standings.corporation_standings_data.__wrapped__
        # when
        response = my_view_without_cache(request)
        # then
        self.assertEqual(response.status_code, 200)
        data = json_response_to_dict_2(response, "corporation_id")
        obj = data[2102]
        self.assertPartialDictEqual(
            obj,
            {
                "corporation_id": 2102,
                "alliance_name": "",
                "faction_name": "",
                "standing": -10.0,
                "state": "",
                "main_character_name": "",
            },
        )


class TestAllianceStandingsData(PartialDictEqualMixin, TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.factory = RequestFactory()
        cls.contact_set = create_contacts_set()
        load_eve_entities()
        create_eve_objects()
        load_corporation_details()
        member_state = AuthUtils.get_member_state()
        member_state.member_alliances.add(EveAllianceInfo.objects.get(alliance_id=3001))
        cls.user = AuthUtils.create_member("John Doe")
        cls.user = AuthUtils.add_permission_to_user_by_name(
            "standingsrequests.request_standings", cls.user
        )
        EveCharacter.objects.get(character_id=1009).delete()
        cls.main_character_1 = EveCharacter.objects.get(character_id=1002)
        cls.user_1 = AuthUtils.create_member(cls.main_character_1.character_name)
        add_character_to_user(
            cls.user_1,
            cls.main_character_1,
            is_main=True,
            scopes=[TEST_SCOPE],
        )
        cls.alt_character_1 = EveCharacter.objects.get(character_id=1007)
        add_character_to_user(
            cls.user_1,
            cls.alt_character_1,
            scopes=[TEST_SCOPE],
        )

    def test_normal(self):
        # given
        self.maxDiff = None
        request = self.factory.get(reverse("standingsrequests:alliance_standings_data"))
        request.user = self.user
        my_view_without_cache = standings.alliance_standings_data.__wrapped__
        # when
        response = my_view_without_cache(request)
        # then
        self.assertEqual(response.status_code, 200)
        data = json_response_to_dict_2(response, "alliance_id")
        self.assertSetEqual(set(data.keys()), {3010})
        obj = data[3010]
        self.assertPartialDictEqual(obj, {"alliance_id": 3010, "standing": -10.0})
