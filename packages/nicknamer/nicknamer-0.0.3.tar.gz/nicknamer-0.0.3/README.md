# NickNamer

NickNamer is a Python library for generating random names.

There are two options for random generation. The first is a random sequence of
words that can be included with a defined format. The format is a string using
tags for the available word types. A format string of "\<noun\>-\<verb\>" will
return a string with a noun and a verb, separated by a dash. For example:
'car-run' or 'chair-talk'. Valid word type tags are: "\<noun\>", "\<verb\>", and
"\<adjective\>".

The second option is a string of random letters (both capital and lower case)
and digits. The length of the string is configurable. For a length of 8, some
examples outputs are: 'mzSsqUOR', 'YkDXJF0E', 'zv52JbGH', 'czHoBnkJ'.


## Installation

Install via [pip](https://pip.pypa.io/en/stable/):

```bash
pip install nicknamer
```

## Usage

Below are example usages for the library. The docstrings for the individual
classes may have more information.

### Random word generation
To use the random word generation:

```python
import nicknamer

# example format string
format_str="<noun>-<verb>-<adjective>"
word_generator = nicknamer.NickNamer(
    seed=12345,
    generator_class=nicknamer.WordNickNamer,
    format_str=format_str,
)
# print 3 example values
print(word_generator.get_value())
print(word_generator.get_value())
print(word_generator.get_value())
```

This will print:
```
Immortality-Sightsman-Aculeate
Stratifying-Touser-Vermifugal
Evangelistary-Upholsterer-Inductive
```

Changing the seed changes the values.
The `NickNamer` class handles the random numbers, but you can also can also
do that yourself and use `WordNickNamer` directly:

```python
import random
import nicknamer

# example format string
format_str="<noun>-<verb>-<adjective>"
word_generator_alt = nicknamer.WordNickNamer(format_str=format_str)

rng = random.Random(12345)

# print 3 example values
print(word_generator_alt.get_value_from_generator(rng))
print(word_generator_alt.get_value_from_generator(rng))
print(word_generator_alt.get_value_from_generator(rng))
```

This gives the same results. `get_value_from_generator()` will accept any
generator that implements a `choice()` function to select a value from a
list. For example, a numpy random generator will work. Note that numpy
must be installed separately.

```python
import numpy
import nicknamer

# example format string
format_str="random verb: <verb>"
word_generator_alt = nicknamer.WordNickNamer(format_str=format_str)

rng = numpy.random.default_rng(12345)

# print example value
print(word_generator_alt.get_value_from_generator(rng))
```

### Random alphanumeric generation

To use the random alphanumeric generation:

```python
import nicknamer

alphanum_generator = nicknamer.NickNamer(
    seed=12345,
    generator_class=nicknamer.AlphaNumNickNamer,
    length=10,
)
# print 3 example values
print(alphanum_generator.get_value())
print(alphanum_generator.get_value())
print(alphanum_generator.get_value())
```

This will print:
```
zaZswmJkhA
IkIw7f8zFj
Slvbv78Ua6
```

This can also be used directly with an external random generator by creating
the object `nicknamer.AlphaNumNickNamer(length=10)` and using
`get_value_from_generator(rng)` as above.

## License

[apache-2.0](https://choosealicense.com/licenses/apache-2.0/)
