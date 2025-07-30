# nombres_vers_lettres

A Python package to write numbers in French, with a simple script. The reason I made this package is the complexity of this simple task that often lead the implementation of such a tool to produce erroneous results (see [this issue](https://github.com/savoirfairelinux/num2words/issues/532)).

## Installation

You can easily install this package using `pip`.

```bash
python -m pip install nombres_vers_lettres
```

Or for the development version:

```bash
python -m pip install git+https://github.com/Vincent-Stragier/nombres_vers_lettres.git
```

### Example

It is better to have your number in strings, this avoids conversion error between `int` or `float` and strings (see [floating point precision](https://docs.python.org/3/tutorial/floatingpoint.html) for more details).

```python
import nombres_vers_lettres as nvl
from nombres_vers_lettres import constants

# List available languages
print(f"{constants.AVAILABLE_LANGUAGES = }")

# List available currencies
print(f"{constants.CURRENCY_FORMS_FR_CODES = }")

# Print the number 42 in French (cardinal mode, new orthographe)
# Default language is fr_BE
cardinal_42 = nvl.make_letters(
    42, language="fr_FR", post_1990_orthographe=True
)

print(f"{cardinal_42 = }")

# Print 42e in French (cardinal mode, new orthographe)
ordinal_nominal_42 = nvl.make_letters(
    42, language="fr_FR", mode="ordinal_nominal", post_1990_orthographe=True
)

print(f"{ordinal_nominal_42 = }")

# Print €420,69 in French (new orthographe)
currency_420_69 = nvl.make_letters(
    "420,69",
    language="fr_FR",
    mode="EUR",
    post_1990_orthographe=True,
    # By default, non-breaking spaces are used
    use_non_breaking_spaces=False,
)

print(f"{currency_420_69 = }")

# Write 1st feminine plural
ordinal_nominal_1st_f_p = nvl.make_letters(
    "1",
    language="fr_FR",
    mode="ordinal_nominal",
    gender="feminine",
    plural=True,
    post_1990_orthographe=True,
)
print(f"{ordinal_nominal_1st_f_p = }")

```

### Script usage

After installing this package, Python gives you access to two entry points: `nombres_vers_lettres` or `nvl`.

```bash
$ nvl -h
usage: nvl [-h] [--mode MODE | --cardinal | --ordinal | --ordinal_nominal] [--gender GENDER | --masculine | --feminine] [--plural]
           [--post_1990_orthographe] [--language LANGUAGE]
           number

positional arguments:
  number                The number as a string to convert to letters (in French)

options:
  -h, --help            show this help message and exit
  --mode MODE           The mode to use for the conversion (nominal, cardinal or ordinal)
  --cardinal, -c        Convert the number to cardinal numbers in letters (e.g., 'un chat', 'deux ânes', 'quatre-vingts chats', 'deux-cents
                        billes', etc.)
  --ordinal, -o         Convert the number to ordinal numbers in letters (e.g., 'la page un', 'la page quatre-vingt', 'la page deux-cent', etc.)
  --ordinal_nominal, -on
                        Convert the number to ordinal nominal numbers in letters (e.g., 'la quatre-vingtième page', 'la deux-centième page',
                        etc.)
  --gender GENDER, -g GENDER
                        The gender to use for the conversion (feminine, féminin, feminin, f or masculine, masculin, m), default is masculine
                        (only has an effect on cardinal and ordinal_nominal modes)
  --masculine, -m       Convert the number to masculine letters (e.g., 'un' -> 'un')
  --feminine, -f        Convert the number to feminine letters (e.g., 'un' -> 'une')
  --plural, -p          Convert the number to plural letters (e.g., 'un' -> 'uns'), only has an effect on cardinal and ordinal_nominal modes
  --post_1990_orthographe, -t
                        Use the tiret character everywhere (e.g., 'vingt-et-un')
  --language LANGUAGE, -l LANGUAGE
                        The language code to use for the conversion (e.g., fr_BE, fr_CD, fr_FR, fr_CA, fr_CH, fr_IT)
```

## How to contribute

If you spotted an error, you can [open an issue in this repository](https://github.com/Vincent-Stragier/nombres_vers_lettres/issues/new/choose). Moreover, you can help to fix [**`num2words`**](https://github.com/savoirfairelinux/num2words).

And you can also open Pull Request for this repository.

After locally cloning your fork of this repository, you can install all the tools needed to check the code:

```bash
python -m pip install -r requirements-dev.txt

# Ideally, also install the pre-commit hooks,
# which will be executed before each commit
precommit install
```

### Pre-commit

If you cannot manage to commit your code due to the pre-commit hooks, simply uninstall them (`precommit uninstall`).

You can still manually run them using `precommit run -a -v` to see where the issues are.

### Coverage

Some tests have been implemented to check if you broke the current code. Ideally, you should add new test before changing the codebase to check if it indeed solves the issue, etc. Those tests are run by the pre-commit hooks.

#### Run the tests

```bash
coverage run -m pytest
```

#### Get some simple coverage information

```bash
coverage report
```

#### Generate an HTML report of the test coverage

```bash
coverage html
```

## Some references

Important references are in italic.

- [Writing numbers in letters according to Le Figaro](https://leconjugueur.lefigaro.fr/frlesnombres.php)
- [Writing numbers in euros according to Le Figaro](https://leconjugueur.lefigaro.fr/frlesnombreseneuros.php)
- [How to write numbers in French according to Bescherelle](https://www.bescherelle.com/faq/comment-ecrire-les-nombres-en-lettres/)
- [How to write numbers in Canadian French according to Bescherelle](https://bescherelle.ca/ecriture-des-nombres/)
- [_How to write numbers in French according to Wikipedia_](https://fr.wikipedia.org/wiki/Nombres_en_fran%C3%A7ais#Apr%C3%A8s_la_virgule) ←
- [_How to write big numbers in French according to Wikipedia_](https://fr.wikipedia.org/wiki/Noms_des_grands_nombres) ←
- [_How to write ordinal numbers according to Lingolia_](https://francais.lingolia.com/fr/vocabulaire/nombres-date-et-heure/les-nombres-ordinaux) ←
- [How to write cardinal numbers according to Lingolia](https://francais.lingolia.com/fr/vocabulaire/nombres-date-et-heure/les-nombres-cardinaux)
