# Copyright (c) 2021,2022,2023,2024,2025 Kian-Meng Ang
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""Env subcommand."""

import argparse
import logging
import sys

import jieba.analyse
from bs4 import UnicodeDammit
from langdetect import detect

from txt2ebook.exceptions import EmptyFileError
from txt2ebook.models import Book
from txt2ebook.parser import Parser

logger = logging.getLogger(__name__)


def build_subparser(subparsers) -> None:
    """Build the subparser."""
    parse_parser = subparsers.add_parser(
        "parse", help="parse and validate the txt file"
    )

    parse_parser.add_argument(
        "input_file",
        nargs=None if sys.stdin.isatty() else "?",  # type: ignore
        type=argparse.FileType("rb"),
        default=None if sys.stdin.isatty() else sys.stdin,
        help="source text filename",
        metavar="TXT_FILENAME",
    )

    parse_parser.add_argument(
        "-ps",
        "--paragraph_separator",
        dest="paragraph_separator",
        type=lambda value: value.encode("utf-8").decode("unicode_escape"),
        default="\n\n",
        help="paragraph separator (default: %(default)r)",
        metavar="SEPARATOR",
    )

    parse_parser.set_defaults(func=run)


def run(args: argparse.Namespace) -> Book:
    """Run env subcommand.

    Args:
        args (argparse.Namespace): Config from command line arguments

    Returns:
        None
    """
    logger.info("Parsing txt file: %s", args.input_file.name)

    unicode = UnicodeDammit(args.input_file.read())
    logger.info("Detect encoding : %s", unicode.original_encoding)

    content = unicode.unicode_markup
    if not content:
        raise EmptyFileError(f"Empty file content in {args.input_file.name}")

    args_language = args.language
    detect_language = detect(content)
    args.language = args_language or detect_language
    logger.info("args language: %s", args_language)
    logger.info("Detect language: %s", detect_language)

    if args_language and args_language != detect_language:
        logger.warning(
            "args (%s) and detect (%s) language mismatch",
            args_language,
            detect_language,
        )

    tags = jieba.analyse.extract_tags(content, topK=100)
    logger.info("tags: %s", " ".join(tags))

    parser = Parser(content, args)
    book = parser.parse()

    if args.debug:
        book.debug(args.verbose)

    return book
