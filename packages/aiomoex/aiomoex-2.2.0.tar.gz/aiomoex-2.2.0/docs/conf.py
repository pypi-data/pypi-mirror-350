import os
import re
import sys

_package_name = "aiomoex"

_route_path = os.path.abspath("../")
sys.path.insert(0, _route_path)
_version_path = os.path.abspath(os.path.join(_route_path, "pyproject.toml"))
with open(_version_path) as file:
    try:
        _version_info = re.search(
            r"^version = \"" r"(?P<major>\d+)" r"\.(?P<minor>\d+)" r"\.(?P<patch>\d+)\"$",
            file.read(),
            re.M,
        ).groupdict()
    except IndexError:
        raise RuntimeError("Unable to determine version.")

version = "{major}.{minor}".format(**_version_info)
release = "{major}.{minor}.{patch}".format(**_version_info)

extensions = ["sphinx.ext.autodoc", "sphinx.ext.githubpages"]
autodoc_member_order = "bysource"
templates_path = ["templates"]
html_static_path = ["static"]

source_suffix = ".rst"
master_doc = "index"
project = _package_name
copyright = "2018, Mikhail Korotkov aka WLMike"
author = "Mikhail Korotkov aka WLMike"
language = "ru"
exclude_patterns = ["build"]
highlight_language = "default"
html_theme = "aiohttp_theme"

html_theme_options = {
    "logo": "",
    "description": "Asyncio MOEX ISS API",
    "canonical_url": "https://wlm1ke.github.io/aiomoex",
    "github_user": "WLM1ke",
    "github_repo": "aiomoex",
    "github_button": False,
    "github_type": "",
    "github_banner": True,
    "badges": [
        {
            "image": "https://badge.fury.io/py/aiomoex.svg",
            "target": "https://badge.fury.io/py/aiomoex",
            "height": "20",
            "alt": "Latest PyPI package version",
        },
    ],
    "sidebar_collapse": False,
}

html_sidebars = {"**": ["about.html", "navigation.html"]}
