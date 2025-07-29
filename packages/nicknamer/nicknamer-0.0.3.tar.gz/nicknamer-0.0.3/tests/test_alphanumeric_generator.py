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


def test_alphanumeric_length() -> None:
    """Test that lengths are handled correctly."""
    right_seed = 123
    rng = random.Random(right_seed)

    for length in range(1, 5):
        obj = nicknamer.AlphaNumNickNamer(length=length)
        if len(obj.get_value_from_generator(rng)) != length:
            err_msg = "Wrong length returned from AlphaNumNickNamer"
            raise AssertionError(err_msg)

    for length in [-10, 0]:
        with pytest.raises(ValueError, match="'length' must be >= 1"):
            _ = nicknamer.AlphaNumNickNamer(length=length)


# length, seed, example result1, examplt result2
result_examples = [
    (12, 123, "dfzg3cHu0juu", "paBfLetB4fiW"),
    (30, 324, "KS7DHZeqlvwNy1JX0CimS0Oda6MVZV", "XaRucukpUt9Hjq09VKNhsVoffdi0rN"),
    (6, 1, "i0VpEB", "OWfbZA"),
]


@pytest.mark.parametrize(
    ("length", "seed", "example_result1", "example_result2"),
    result_examples,
)
def test_alphanumeric_generator(
    length: int,
    seed: int,
    example_result1: str,
    example_result2: str,
) -> None:
    """Test that words are generated as expected."""
    obj = nicknamer.NickNamer(
        seed=seed,
        generator_class=nicknamer.AlphaNumNickNamer,
        length=length,
    )
    for expected in [example_result1, example_result2]:
        actual_value = obj.get_value()
        if actual_value != expected:
            err_msg = (
                "AlphaNumNickNamer: output does not match expected: ",
                f"{actual_value} != {expected}",
            )
            raise AssertionError(err_msg)
