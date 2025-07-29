# AOChallenge Module

The  module   is  designed   to  speed  up   the  solution   of  certain
coding   challenges.   The   module    is   inspired   by   [Advent   of
Code](https://adventofcode.com/), I have not  used it for anything else,
but it is probably useful for other things.

The use  of the module is  different from the traditional  ones, my goal
was to  be able  to create  a new solution  easily. The  `Solution` base
class provided  by the  module contains some  frequently used  or useful
functions for debugging and only the solutions need to be added.

Each time I start from the code below.

```python
#!/usr/bin/python3 -u

import aochallenge

class Solution(aochallenge.Solution):
    def __init__(self):
        super().__init__()
        data = self.load(True,',',int)

#    def part1(self):

#    def part2(self):

#    def solve_more(self):

solution = Solution()
solution.main()
```

To be more precise, I also use  type annotation, which I have taken from
here.

The `part1`  and `part2` methods  are called  and the returned  value is
displayed by the original class. If the two parts of the challenge build
on each other,  you can also use `solve_more` (generator),  in which the
solutions are returned with the `yield` keyword, so that the computation
can  continue  without  saving  previous results.  Check  out  also  the
[example](#example) at the end of this document.

In the constructor, it makes sense to load and, if necessary, preprocess
the input data, which is well done  by the load function of the Solution
class. Note  that this function  examines the program's  input arguments
and decides which input file to load (test or main) based on them.

## Importing data

For  each challenge  there are  one  or more  test inputs  and there  is
your  challenge one.  The  class expects  the input  files  to be  named
appropriately  to be  able to  load automatically.  For example,  if the
file  name  is "aoc-2201.py",  then  the  input  files should  be  named
"aoc-2201_<id>_.input". E.g.

    aoc/2022/01/
    |---- aoc-2201.py       source code
    |---- aoc-2201-t.input  test input
    \---- aoc-2201.input    challenge input

In this case, you can run your code with the test data as follows:

    $ ./aoc-2201.py -t

And with the challenge data, simply:

    $ ./aoc-2201.py

In some special cases  the input is a single line of  data or some other
simple constructs.  In this case it  is unnecessary to create  files for
each, you can simply pass a look-up-table to the `load` function. E.g.

```python
INPUT = {
    None: 'My challenge input data',
    't': 'My test 1 input data',
    't2': 'My test 2 input data',
}
...
def __init__(self):
    super().__init__()
    data = self.load(lut=INPUT)
```

If you need which variant the solution has been run with, you can check it with
`variant`. It returns `None` if no variant has bee given and the variant id
(E.g. `"-t"`) if it has been:

```python
def __init__(self):
    ...
    if self.variant() is None:
        # no variant branch
```

### Using `load` method

The `load`  method is used to  prepare the data for  further processing.
The input  can come from a  file or from a  predefined look-up-table. If
the latter is not specified, file handling is automatic (see above).

`load` function does  not only import data, but  does some preprocessing
on them:

```python
def load(self,
        splitlines: bool = False,
        splitrecords: str|None = None,
        recordtype:  list|tuple|type|None = None,
        *,
        lut: dict[str|None, Any]|None = None,
        ) -> list[str|int|list]
```

Parameters:

- `splitlines`: boolean  value whether the  input data lines have  to be
  splitted into a list.
- `splitrecords`:  string value  used to  separate the  records in  each
  line. For example, if there  are comma-separated values, this field is
  ",". If set to `None`, items within the row are not split.
- `recordtype`: type of records. For example, if the values are numbers,
  it  can  be `int`  or  even  `float`.  The  `load` function  does  the
  conversion. If  the parameter type  is `list` or `tuple`,  the various
  fields may  have different types.  E.g. `(str, list)` means,  that the
  first record should be a `str`, but all further ones have to be casted
  to `int`.
- `lut` (keyword  only parameter): if  this parameter is  specified, the
  input data will be read from it instead of from an input file.

Note, that  if `splitlines`  is `False`  but `splitrecords`  is defined,
only the  first row  will be processed.  This means that  if you  have a
one-row data set, the return element  is not a two-dimensional list with
a single nested list, but a simple list of values from the first row.

## Displaying temporary results

The  class  contains  some  debugging  solutions  to  display  temporary
results.

- `print_condensed`:  Prints content  of  a  2-dimensional container  of
  characters "condensed". E.g. if data is

      [['#', '#', '.'], ['.', '#', '.'], ['.', '#', '#']]`

  the following will be printed:

      ##.
      .#.
      .##

  Note that the 2-dimensional container can be also a list of strings.
- `def  print_csv`: Prints  content of  a 2-dimensional  container in  a
  comma separated way
- `def  print_arranged`: Prints  content  of  a 2-dimensional  container
  arranged into columns

## Example

**PART 1**: Add up  all the numbers in each row  separated by commas and
print the maximum of these sums.

**PART 2**: Find the 3 largest sums, add them up and determine the final
result.

Using `part1` and `part2`:

```python
#!/usr/bin/python3 -u

import aochallenge

class Solution(aochallenge.Solution):
    def __init__(self):
        super().__init__()
        self.data = self.load(True,',',int)

    def part1(self):
        return max(sum(row) for row in self.data)

    def part2(self):
        return sum(sorted(sum(row) for row in self.data)[-3:])

solution = Solution()
solution.main()
```

Using `solve_more`:

```python
#!/usr/bin/python3 -u

import aochallenge

class Solution(aochallenge.Solution):
    def __init__(self):
        super().__init__()
        self.data = self.load(True,',',int)

    def solve_more(self):
        sums = sorted(sum(row) for row in self.data)
        yield sums[-1]
        yield sum(sums[-3:])

solution = Solution()
solution.main()
```
