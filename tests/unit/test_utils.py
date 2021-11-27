# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Gauvain Pocentek <gauvain@pocentek.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import pytest
import requests
import responses

from gitlab import utils


def test_clean_str_id():
    src = "nothing_special"
    dest = "nothing_special"
    assert dest == utils.clean_str_id(src)

    src = "foo#bar/baz/"
    dest = "foo%23bar%2Fbaz%2F"
    assert dest == utils.clean_str_id(src)

    src = "foo%bar/baz/"
    dest = "foo%25bar%2Fbaz%2F"
    assert dest == utils.clean_str_id(src)


def test_sanitized_url():
    src = "http://localhost/foo/bar"
    dest = "http://localhost/foo/bar"
    assert dest == utils.sanitized_url(src)

    src = "http://localhost/foo.bar.baz"
    dest = "http://localhost/foo%2Ebar%2Ebaz"
    assert dest == utils.sanitized_url(src)


@responses.activate
def test_response_content(capsys):
    responses.add(
        method="GET",
        url="https://example.com",
        status=200,
        body="test",
        content_type="application/octet-stream",
    )

    resp = requests.get("https://example.com", stream=True)
    utils.response_content(resp, streamed=True, action=None, chunk_size=1024)

    captured = capsys.readouterr()
    assert "test" in captured.out


@pytest.mark.parametrize(
    "source,expected",
    [
        ({"a": "", "b": "spam", "c": None}, {"a": "", "b": "spam", "c": None}),
        ({"a": "", "b": {"c": "spam"}}, {"a": "", "b[c]": "spam"}),
    ],
)
def test_copy_dict(source, expected):
    dest = {}

    utils.copy_dict(dest, source)
    assert dest == expected


@pytest.mark.parametrize(
    "dictionary,expected",
    [
        ({"a": None, "b": "spam"}, {"b": "spam"}),
        ({"a": "", "b": "spam"}, {"a": "", "b": "spam"}),
        ({"a": None, "b": None}, {}),
    ],
)
def test_remove_none_from_dict(dictionary, expected):
    result = utils.remove_none_from_dict(dictionary)
    assert result == expected
