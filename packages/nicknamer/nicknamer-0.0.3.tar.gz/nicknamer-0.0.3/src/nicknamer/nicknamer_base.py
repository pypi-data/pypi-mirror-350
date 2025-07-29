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

"""Base classes for NickNamer.

These provide the base behavior for the nick naming classes.
The actual string creation behavior is controlled by the other classes.
See each class for details.

The NickNamer class provides an optional framework for tracking the state of
the generators.

Pseudocode of typical usage:
  seed = 123
  obj = NickNamer(seed, NICK_NAMER_CLASS, **CLASS_SPECIFIC_CONFIG_VALUES)
  random_str = obj.get_value()
"""

import random
from abc import ABC, abstractmethod
from typing import Any, Protocol


class RandomWithChoice(Protocol):
    """Matches any object that has a suitable choice method."""

    def choice(self, seq: Any, size: int = 1) -> Any:
        """Select a random item from the sequence."""
        ...


class _BaseNickNamer(ABC):
    """Base class for nick namer objects."""

    @abstractmethod
    def get_value_from_generator(self, rng: RandomWithChoice | random.Random) -> str:
        """Return a string created using the given random generator.

        This uses the passed random number generator.

        The value, format, style, etc... of the returned string are controlled
        by the specific class being used. See the class definition for details.

        Args:
          rng: random generator to use in creation

        Returns:
          the randomly generated id
        """


class NickNamer:
    """Generate Random IDs."""

    def __init__(
        self,
        seed: int | float | str | bytes | bytearray | None,
        generator_class: type[_BaseNickNamer],
        **kwargs: Any,
    ) -> None:
        """Initialize the NickNamer object.

        This will internally create an object to generate ids using the given
        `generator_class`. That object will be passed `kwargs` for construction,
        so see the relevant class for details.

        Args:
          seed: the seed for the random number generator
          generator_class: class to use for making the values
          kwargs: values passed to `generator_class` as parameters.
            See the specific class for required and optional values.
        """
        self._rng = random.Random(seed)
        self._name_generator = generator_class(**kwargs)

    def get_value(self) -> str:
        """Return a random id using the internal random generator.

        Returns:
          The random id generated from the object.
        """
        return self._name_generator.get_value_from_generator(self._rng)

    def get_value_from_generator(self, rng: RandomWithChoice | random.Random) -> str:
        """Return a random id using the given random generator.

        Args:
          rng: a random generator that has a choice() method to call

        Returns:
          The random id generated from the object.
        """
        return self._name_generator.get_value_from_generator(rng)
