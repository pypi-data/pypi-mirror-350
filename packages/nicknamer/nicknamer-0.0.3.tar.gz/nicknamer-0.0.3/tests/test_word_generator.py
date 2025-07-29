# Copyright (c) 2025 Mobius Logic, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Run tests on the word generator."""

import random

import pytest

import nicknamer

# format string, expected parsed list
format_examples = [
    ("<noun>", ["<noun>"]),
    ("<noun><noun>", ["<noun>", "<noun>"]),
    ("<noun>.<noun>", ["<noun>", ".", "<noun>"]),
    (
        "<noun>, <verb>, and <noun>!",
        ["<noun>", ", ", "<verb>", ", and ", "<noun>", "!"],
    ),
    ("<adjective>_<noun>_<verb>", ["<adjective>", "_", "<noun>", "_", "<verb>"]),
    ("", []),
]


@pytest.mark.parametrize(("format_string", "output_list"), format_examples)
def test_formatter(format_string: str, output_list: list[str]) -> None:
    """Test that format parsing works as expected."""
    obj = nicknamer.WordNickNamer(format_str=format_string)
    actual_parsing = obj._parsed_format  # noqa: SLF001
    if actual_parsing != output_list:
        err_msg = (
            "WordNickNamer: parsed format does not match expected: ",
            f"{actual_parsing} != {output_list}",
        )
        raise AssertionError(err_msg)


result_examples_seed123 = [
    ("<noun>", "Articulateness"),
    ("<noun><noun>", "ArticulatenessEbrillade"),
    ("<noun>.<noun>", "Articulateness.Ebrillade"),
    ("<noun>, <verb>, and <noun>!", "Articulateness, Embosser, and Bishopdom!"),
    ("<adjective>_<noun>_<verb>", "Araneiform_Ebrillade_Bonesetter"),
    ("", ""),
]


@pytest.mark.parametrize(("format_string", "output_value"), result_examples_seed123)
def test_word_generator(format_string: str, output_value: str) -> None:
    """Test that words are generated as expected."""
    seed = 123
    obj = nicknamer.NickNamer(
        seed=seed,
        generator_class=nicknamer.WordNickNamer,
        format_str=format_string,
    )
    actual_value = obj.get_value()
    if actual_value != output_value:
        err_msg = (
            "WordNickNamer: output does not match expected: ",
            f"{actual_value} != {output_value}",
        )
        raise AssertionError(err_msg)


@pytest.mark.parametrize(("format_string", "output_value"), result_examples_seed123)
def test_word_generator_external(format_string: str, output_value: str) -> None:
    """Test that words are generated as expected using external generator."""
    wrong_seed = 456  # this will not give the expected value
    obj = nicknamer.NickNamer(
        seed=wrong_seed,
        generator_class=nicknamer.WordNickNamer,
        format_str=format_string,
    )
    wrong_value = obj.get_value()  # should be wrong because the seed is wrong

    # ignore empty output_value, which will match regardless of seed
    if wrong_value == output_value and output_value:
        err_msg = (
            "WordNickNamer: output is wrong: ",
            f"{wrong_value} == {output_value}  ;{format_string};",
        )
        raise AssertionError(err_msg)

    right_seed = 123
    rng = random.Random(right_seed)
    right_value = obj.get_value_from_generator(rng)  # uses correct generator
    if right_value != output_value:
        err_msg = (
            "WordNickNamer: output incorrect with external generator ",
            f"{right_value} != {output_value}",
        )
        raise AssertionError(err_msg)
