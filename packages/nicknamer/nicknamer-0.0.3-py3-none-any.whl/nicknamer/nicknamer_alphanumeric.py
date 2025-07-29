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

"""Class to create alphanumeric strings.

Generates random strings which each character being a random letter or digit.
Letters include both upper or lower case. The desired string length must be
specified.

Typical usage example:
  seed = 123
  rng = random.Random(seed)
  obj = AlphaNumNickNamer(length=10)
  random_str = obj.get_value_from_generator(rng)

Or, to use with NickNamer class:
  seed = 123
  obj = NickNamer(seed, AlphaNumNickNamer, length=10)
  random_str = obj.get_value()
"""

import random
import string

from typing_extensions import override

from nicknamer.nicknamer_base import RandomWithChoice, _BaseNickNamer


class AlphaNumNickNamer(_BaseNickNamer):
    """Generate random alphanumeric sequence.

    Sequence if a defined length string with characters taken from a-zA-Z0-9.
    """

    def __init__(
        self,
        length: int,
    ) -> None:
        """Initialize the object.

        Args:
          length: the desired length of the string

        Raises:
          ValueError: If length is less than 1.
        """
        if length < 1:
            err_msg = "'length' must be >= 1"
            raise ValueError(err_msg)
        self._length = length

    @override
    def get_value_from_generator(self, rng: RandomWithChoice | random.Random) -> str:
        characters = list(string.ascii_letters + string.digits)

        try:
            # Try the numpy version
            vals = rng.choice(  # type: ignore[call-arg]
                characters,
                size=self._length,  # pyright: ignore[reportCallIssue]
            )
            return "".join(vals)
        except TypeError:
            # try the random.Random version
            vals = rng.choices(  # type: ignore[union-attr]  # pyright: ignore[reportAttributeAccessIssue]
                characters,
                k=self._length,
            )
            return "".join(vals)
