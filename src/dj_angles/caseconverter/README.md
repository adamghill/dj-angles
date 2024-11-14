# Case Converter

[![pipline](https://img.shields.io/gitlab/pipeline/chrisdoherty4/python-case-converter)](https://gitlab.com/chrisdoherty4/python-case-converter/-/pipelines) [![wheel](https://img.shields.io/pypi/wheel/case-converter)](https://pypi.org/project/case-converter/) ![coverage](https://gitlab.com/chrisdoherty4/python-case-converter/badges/master/coverage.svg) ![license](https://img.shields.io/github/license/chrisdoherty4/python-case-converter)

A robust python package for transforming string cases such as `Hello, world!` into
 `helloWorld` (camelcase).

## General usage

```python
from caseconverter import camelcase

camelcase("Hello, world!") # output: helloWorld
```

## Available conversions

### `camelcase`

```python
from caseconverter import camelcase

camelcase("Hello, world!")
```

```text
helloWorld
```

### `cobolcase`

```python
from caseconverter import cobolcase

cobolcase("Hello, world!")
```

```text
HELLO-WORLD
```

### `flatcase`

```python
from caseconverter import flatcase

flatcase("Hello, world!")
```

```text
helloworld
```

### `kebabcase`

```python

from caseconverter import kebabcase

kebabcase("Hello, world!")
```

```text
hello-world
```

### `macrocase`

```python
from caseconverter import macrocase

macrocase("Hello, world!")
```

```text
HELLO_WORLD
```

#### Additional options

`delims_only : bool` - Only consider delimiters as boundaries (default: `False`).

### `pascalcase`

```python
from caseconverter import pascalcase

pascalcase("Hello, world!")
```

```text
HelloWorld
```

### `snakecase`

```python
from caseconverter import snakecase

snakecase("Hello, world!")
```

```text
hello_world
```

## Options for all conversions

### Stripping punctuation

Punctuation is stripped when doing a case conversion. However, should you
wish to keep the punctuation you can do so by passing `strip_punctuation=False`.

```python
camelcase("Hello, world!", strip_punctuation=False) # output: hello,World!
```

### Delimeter customization

Default delimiters used to denote a token boundary.

```python
DELIMITERS = " -_"
```

You can pass `delims` to each case conversion function to specify a custom
set of delimiters.

```python
# Use a pipe `|` as the only delimiter.
camelcase("Hello,|world!", delims="|") # output: helloWorld
```

## Behavior

### Delimiters

If multiple delimeter characters are identified next to eachother they will be considered as a single delimeter. For example, `-_` contains 2 different delimeter characters and is considered a single delimeter.

### Boundary definitions

|Name|Description|
|---|---|
|OnDelimeterUppercaseNext|On a delimieter, upper case the following character|
|OnDelimeterLowercaseNext|On a delimeter, lower case the following character|
|OnUpperPrecededByLowerAppendUpper|On an upper case character followed by a lower case character, append the upper case character|
|OnUpperPrecededByLowerAppendLower|On an upper case character preceeded by a lower case character append the lower case character|
|OnUpperPrecededByUpperAppendJoin|On an upper case caharacter preceeded by an upper append the join character. Join characters are context dependent. Example: macro cast join character is `_`|
|OnUpperPrecededByUpperAppendCurrent|On an upper case character preceeded by an upper case character append the upper case character|

## Contributing

1. Write clean code.
2. Write new tests for new use-cases.
3. Test your code before raising a PR.
4. Use [black](https://pypi.org/project/black/) to format your code.
