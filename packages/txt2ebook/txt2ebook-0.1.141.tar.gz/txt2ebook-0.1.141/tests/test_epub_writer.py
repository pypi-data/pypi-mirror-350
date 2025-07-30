# pylint: disable=C0114,C0116
import argparse

import pytest


@pytest.fixture(name="config")
def fixture_config():
    return argparse.Namespace(
        **{
            "title": False,
            "author": False,
            "cover": None,
            "paragraph_separator": "\n\n",
            "re_delete": False,
            "re_replace": False,
            "re_delete_line": False,
            "re_volume_chapter": (),
            "re_volume": (),
            "re_chapter": (),
            "re_title": (),
            "re_author": (),
            "no_wrapping": False,
            "raise_on_warning": False,
            "width": False,
            "language": "zh-cn",
        }
    )
