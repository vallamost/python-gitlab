# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 Gauvain Pocentek <gauvain@pocentek.net>
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

from gitlab import types


def test_gitlab_attribute_get():
    o = types.GitlabAttribute("whatever")
    assert o.get() == "whatever"

    o.set_from_cli("whatever2")
    assert o.get() == "whatever2"
    assert o.get_for_api() == "whatever2"
    assert o.get_as_tuple_list(key="foo") == [("foo", "whatever2")]

    o = types.GitlabAttribute()
    assert o._value is None


# ArrayAttribute tests
def test_array_attribute_input():
    o = types.ArrayAttribute()
    o.set_from_cli("foo,bar,baz")
    assert o.get() == ["foo", "bar", "baz"]

    o.set_from_cli("foo")
    assert o.get() == ["foo"]


def test_array_attribute_empty_input():
    o = types.ArrayAttribute()
    o.set_from_cli("")
    assert o.get() == []

    o.set_from_cli("  ")
    assert o.get() == []


def test_array_attribute_get_for_api_from_cli():
    o = types.ArrayAttribute()
    o.set_from_cli("foo,bar,baz")
    assert o.get_for_api() == "foo,bar,baz"


def test_array_attribute_get_for_api_from_list():
    o = types.ArrayAttribute(["foo", "bar", "baz"])
    assert o.get_for_api() == "foo,bar,baz"


def test_array_attribute_get_for_api_from_int_list():
    o = types.ArrayAttribute([1, 9, 7])
    assert o.get_for_api() == "1,9,7"


def test_array_attribute_get_as_tuple_list_from_list():
    o = types.ArrayAttribute(["foo", "bar", "baz"])
    assert o.get_as_tuple_list(key="identifier") == [
        ("identifier[]", "foo"),
        ("identifier[]", "bar"),
        ("identifier[]", "baz"),
    ]


def test_array_attribute_get_as_tuple_list_from_int_list():
    o = types.ArrayAttribute([1, 9, 7])
    assert o.get_as_tuple_list(key="identifier") == [
        ("identifier[]", "1"),
        ("identifier[]", "9"),
        ("identifier[]", "7"),
    ]


def test_array_attribute_does_not_split_string():
    o = types.ArrayAttribute("foo")
    assert o.get_for_api() == "foo"


# CsvStringAttribute tests
def test_csv_string_attribute_get_for_api_from_cli():
    o = types.CsvStringAttribute()
    o.set_from_cli("foo,bar,baz")
    assert o.get_for_api() == "foo,bar,baz"


def test_csv_string_attribute_get_for_api_from_list():
    o = types.CsvStringAttribute(["foo", "bar", "baz"])
    assert o.get_for_api() == "foo,bar,baz"


def test_csv_string_attribute_get_for_api_from_int_list():
    o = types.CsvStringAttribute([1, 9, 7])
    assert o.get_for_api() == "1,9,7"


def test_csv_string_attribute_get_as_tuple_list_from_list():
    o = types.CsvStringAttribute(["foo", "bar", "baz"])
    assert o.get_as_tuple_list(key="identifier") == [("identifier", "foo,bar,baz")]


def test_csv_string_attribute_get_as_tuple_list_from_int_list():
    o = types.CsvStringAttribute([1, 9, 7])
    assert o.get_as_tuple_list(key="identifier") == [("identifier", "1,9,7")]


# LowercaseStringAttribute tests
def test_lowercase_string_attribute_get_for_api():
    o = types.LowercaseStringAttribute("FOO")
    assert o.get_for_api() == "foo"


def test_lowercase_string_attribute_get_as_tuple():
    o = types.LowercaseStringAttribute("FOO")
    assert o.get_as_tuple_list(key="user_name") == [("user_name", "foo")]
