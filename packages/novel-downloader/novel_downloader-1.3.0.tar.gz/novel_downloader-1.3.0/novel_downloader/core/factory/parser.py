#!/usr/bin/env python3
"""
novel_downloader.core.factory.parser_factory
--------------------------------------------

This module implements a factory function for creating parser instances
based on the site name and parser mode specified in the configuration.
"""

from collections.abc import Callable

from novel_downloader.config import ParserConfig, load_site_rules
from novel_downloader.core.interfaces import ParserProtocol
from novel_downloader.core.parsers import (
    BiqugeParser,
    CommonParser,
    QidianBrowserParser,
    QidianSessionParser,
)

ParserBuilder = Callable[[ParserConfig], ParserProtocol]

_site_map: dict[str, dict[str, ParserBuilder]] = {
    "qidian": {
        "browser": QidianBrowserParser,
        "session": QidianSessionParser,
    },
    "biquge": {
        "session": BiqugeParser,
    },
}


def get_parser(site: str, config: ParserConfig) -> ParserProtocol:
    """
    Returns a site-specific parser instance.

    :param site: Site name (e.g., 'qidian')
    :param config: Configuration for the parser
    :return: An instance of a parser class
    """
    site_key = site.lower()

    if site_key in _site_map:
        site_entry = _site_map[site_key]
        if isinstance(site_entry, dict):
            parser_class = site_entry.get(config.mode)
        else:
            parser_class = site_entry

        if parser_class:
            return parser_class(config)

    # Fallback: site not mapped specially, try to load rule
    site_rules = load_site_rules()
    site_rule = site_rules.get(site_key)
    if site_rule is None:
        raise ValueError(f"Unsupported site: {site}")

    return CommonParser(config, site_key, site_rule)
