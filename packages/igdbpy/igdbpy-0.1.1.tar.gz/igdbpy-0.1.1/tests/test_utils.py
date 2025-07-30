import os

import pytest

from igdbpy import generate_api_key


def test_api_key_success():
    res = generate_api_key(os.getenv("CLIENT_ID"), os.getenv("CLIENT_SECRET"))
    assert res.access_token is not None
    assert res.expires_in is not None
    assert res.token_type is not None


def test_api_key_fail():
    with pytest.raises(Exception):
        generate_api_key("no", "still_no")
