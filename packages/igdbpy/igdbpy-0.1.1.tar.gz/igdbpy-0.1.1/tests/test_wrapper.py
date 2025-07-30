import os

import pytest

from igdbpy import IgdbWrapper


@pytest.fixture
def wrapper():
    return IgdbWrapper(os.getenv("CLIENT_ID"), os.getenv("ACCESS_TOKEN"))


class TestIgdbWrapper:
    def test_init(self, wrapper):
        assert wrapper.client_id is not None
        assert wrapper.access_token is not None
        assert wrapper.timeout == 3

    def test_generic_request(self, wrapper):
        jstr = wrapper.make_request("age_ratings", "fields *;")[0]

        assert jstr["checksum"] is not None
        assert jstr["content_descriptions"] is not None
        assert jstr["rating_category"] is not None

    def test_generic_filtered_request(self, wrapper):
        # Filter must be in double quotes for strings
        jstr = wrapper.make_request(
            "companies", 'fields *; where slug="supergiant-games";'
        )[0]

        assert jstr["start_date"] == 1262217600
        assert jstr["country"] == 840
        assert len(jstr["developed"]) == 6

    def test_game_endpoint(self, wrapper):
        jstr = wrapper.request_game("fields *;")
        assert len(jstr) == 10

        jstr = wrapper.request_game("fields genres,name,themes; where id = 113112;")[0]
        assert len(jstr["genres"]) == 4
        assert jstr["name"] == "Hades"
        assert len(jstr["themes"]) == 3
