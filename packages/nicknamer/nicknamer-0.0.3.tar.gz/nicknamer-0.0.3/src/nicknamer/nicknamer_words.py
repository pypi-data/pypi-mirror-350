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

"""Class to create random words.

Generates random strings with defined format that contains specific parts of
speech. Example format: "<noun>.<verb>" gives a noun and verb, separated by
a period. For example 'truck.sing'.

Typical usage example:
  seed = 123
  rng = random.Random(seed)
  format_str = "<noun>.<verb>"
  obj = WordNickNamer(format_str)
  random_str = obj.get_value_from_generator(rng)

Or, to use with NickNamer class:
  seed = 123
  format_str = "<noun>.<verb>"
  obj = NickNamer(seed, WordNickNamer, format_str=format_str)
  random_str = obj.get_value()
"""


import importlib.resources
import random
import re
from typing import ClassVar

from typing_extensions import override

from nicknamer.nicknamer_base import RandomWithChoice, _BaseNickNamer


class WordNickNamer(_BaseNickNamer):
    """Generate random word sequence."""

    _wordlist: ClassVar[dict[str, list[str]]] = {}

    def __init__(
        self,
        format_str: str,
    ) -> None:
        """Initialize the object.

        `format_str` is a string describing which random words will be used and what
        the format of the final string will be. For example, "<noun>.<noun>" will
        give two random nounds separated by a '.'. For example:
        bag.line, store.peanut, car.house

        valid parts of speech are: adjective, noun, and verb.

        Parameters
        ----------
        format_str
            Format of the random str
        """
        # create wordlist on first instance
        if not WordNickNamer._wordlist:
            WordNickNamer._fill_wordlist()

        self._format = format_str
        self._parsed_format = self._get_parsed_format()

    def _get_parsed_format(self) -> list[str]:
        """Parse the format string into a sequence parts.

        This is done to allow the format to be used without using a regular
        expression every time.

        This will take "<noun>, <verb>, and <noun>!" and return:
        ["<noun>", ", ", "<verb>", ", and ", "<noun>", "!"]
        When generating a new random value, <noun>, <verb>, and <noun> will be
        replaced with random words of the appropriate type.

        Returns:
          A list of the format sequence parts
        """
        # format for a word, example <noun>
        pattern = re.compile(r"(<.*?>)")
        parsed_format: list[str] = []
        last_pos = 0

        for match in pattern.finditer(self._format):
            # everything before the match, the matched word type
            parsed_format.extend(
                (self._format[last_pos : match.start()], match.group(1)),
            )
            last_pos = match.end()

        # The rest of the text after the last match
        parsed_format.append(self._format[last_pos:])

        # remove '' from the list
        return [i for i in parsed_format if i]

    @classmethod
    def _fill_wordlist(cls) -> None:
        """Read the word lists from the resource files."""
        for word_type in ["adjective", "noun", "verb"]:
            filename = f"{word_type}.txt"

            with importlib.resources.open_text("nicknamer.resources", filename) as f:
                cls._wordlist[f"<{word_type}>"] = [
                    word.strip() for word in f.read().strip().split(",")
                ]

    @override
    def get_value_from_generator(self, rng: RandomWithChoice | random.Random) -> str:
        return "".join(
            rng.choice(self._wordlist[part]) if part in self._wordlist else part
            for part in self._parsed_format
        )
