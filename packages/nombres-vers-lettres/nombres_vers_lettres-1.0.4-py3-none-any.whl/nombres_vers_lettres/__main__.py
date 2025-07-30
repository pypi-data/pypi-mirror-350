"""Main entry point for the application when run with the -m switch."""

import argparse
import os
import sys

from nombres_vers_lettres.constants import (
    AVAILABLE_LANGUAGES,
    VALID_FEMININE,
    VALID_MASCULINE,
)
from nombres_vers_lettres.make_letters import make_letters


def main():
    """Main entry point for the application when run with the -m switch."""

    parser = argparse.ArgumentParser(os.path.basename(sys.argv[0]))

    # Add the positional argument for the number
    parser.add_argument(
        "number",
        type=str,
        help="The number as a string to convert to letters (in French)",
    )

    # Add mutually exclusive arguments for nominal, cardinal and ordinal
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--mode",
        type=str,
        help=(
            "The mode to use for the conversion (nominal, cardinal or ordinal)"
        ),
        default=None,
    )
    group.add_argument(
        "--cardinal",
        "-c",
        action="store_true",
        help=(
            "Convert the number to cardinal numbers in letters "
            "(e.g., 'un chat', 'deux ânes', 'quatre-vingts chats',"
            " 'deux-cents billes', etc.)"
        ),
        default=None,
    )
    group.add_argument(
        "--ordinal",
        "-o",
        action="store_true",
        help=(
            "Convert the number to ordinal numbers in letters "
            "(e.g., 'la page un', 'la page quatre-vingt', "
            "'la page deux-cent', etc.)"
        ),
        default=None,
    )
    group.add_argument(
        "--ordinal_nominal",
        "-on",
        action="store_true",
        help=(
            "Convert the number to ordinal nominal numbers in letters "
            "(e.g., 'la quatre-vingtième page', 'la deux-centième page', etc.)"
        ),
        default=None,
    )

    # Add mutually exclusive arguments for masculine and feminine
    group = parser.add_mutually_exclusive_group()

    feminine = ", ".join(VALID_FEMININE)
    masculine = ", ".join(VALID_MASCULINE)

    group.add_argument(
        "--gender",
        "-g",
        help=(
            "The gender to use for the conversion "
            f"({feminine} or {masculine}), default is masculine "
            "(only has an effect on cardinal and ordinal_nominal modes)"
        ),
        type=str,
        default=None,
    )
    group.add_argument(
        "--masculine",
        "-m",
        action="store_true",
        help="Convert the number to masculine letters (e.g., 'un' -> 'un')",
        default=None,
    )
    group.add_argument(
        "--feminine",
        "-f",
        action="store_true",
        help="Convert the number to feminine letters (e.g., 'un' -> 'une')",
        default=None,
    )

    # Add optional argument for plural
    parser.add_argument(
        "--plural",
        "-p",
        action="store_true",
        help=(
            "Convert the number to plural letters (e.g., 'un' -> 'uns'), "
            "only has an effect on cardinal and ordinal_nominal modes"
        ),
        default=None,
    )

    # Add optional argument for post-1990 orthographe
    parser.add_argument(
        "--post_1990_orthographe",
        "-t",
        action="store_true",
        help="Use the tiret character everywhere (e.g., 'vingt-et-un')",
        default=None,
    )

    # Add optional argument for language code
    available_languages = ", ".join(AVAILABLE_LANGUAGES)

    parser.add_argument(
        "--language",
        "-l",
        type=str,
        help=(
            "The language code to use for the conversion "
            f"(e.g., {available_languages})"
        ),
        default="fr_BE",
    )

    argv = sys.argv[1:]

    if len(argv) > 0:
        # The last argument is the number to convert
        argv[-1] = argv[-1].replace(",", ".")

    args = parser.parse_args(argv)

    # Parse mode
    if args.mode is not None:
        selected_mode = args.mode

    elif args.cardinal is not None:
        selected_mode = "cardinal"

    elif args.ordinal is not None:
        selected_mode = "ordinal_adjectival"

    elif args.ordinal_nominal is not None:
        selected_mode = "ordinal_nominal"

    else:
        selected_mode = "cardinal"

    # Parse gender
    if args.gender is not None:
        if args.gender in (VALID_FEMININE + VALID_MASCULINE):
            selected_gender = args.gender

        else:
            sys.exit(
                f"Gender must be either feminine ({feminine})"
                f" or masculine ({masculine})"
            )

    elif args.feminine is not None:
        selected_gender = "feminine"

    else:
        # Default
        selected_gender = "masculine"

    print(
        make_letters(
            args.number,
            gender=selected_gender,
            plural=args.plural,
            language=args.language,
            mode=selected_mode,
            post_1990_orthographe=args.post_1990_orthographe,
        )
    )


if __name__ == "__main__":
    main()

elif __name__ == "nombres_vers_lettres.__main__":
    # Do nothing
    pass

else:
    raise RuntimeError("Only for use with the -m switch, not as a Python API")
