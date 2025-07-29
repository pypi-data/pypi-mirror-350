#!/usr/bin/env python3
"""
novel_downloader.core.downloaders.base.base_sync
------------------------------------------------

Defines the abstract base class `BaseDownloader`, which provides a
common interface and reusable logic for all downloader implementations.
"""

import abc
import logging
from pathlib import Path

from novel_downloader.config import DownloaderConfig
from novel_downloader.core.interfaces import (
    ParserProtocol,
    SaverProtocol,
    SyncDownloaderProtocol,
    SyncRequesterProtocol,
)


class BaseDownloader(SyncDownloaderProtocol, abc.ABC):
    """
    Abstract downloader that defines the initialization interface
    and the general batch download flow.

    Subclasses must implement the logic for downloading a single book.
    """

    def __init__(
        self,
        requester: SyncRequesterProtocol,
        parser: ParserProtocol,
        saver: SaverProtocol,
        config: DownloaderConfig,
        site: str,
    ):
        """
        Initialize the downloader with its components.

        :param requester: Object implementing RequesterProtocol, used to fetch raw data.
        :param parser: Object implementing ParserProtocol, used to parse page content.
        :param saver: Object implementing SaverProtocol, used to save final output.
        :param config: Downloader configuration object.
        """
        self._requester = requester
        self._parser = parser
        self._saver = saver
        self._config = config
        self._site = site

        self._raw_data_dir = Path(config.raw_data_dir) / site
        self._cache_dir = Path(config.cache_dir) / site
        self._raw_data_dir.mkdir(parents=True, exist_ok=True)
        self._cache_dir.mkdir(parents=True, exist_ok=True)

        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")

    def download(self, book_ids: list[str]) -> None:
        """
        The general batch download process:
          1. Iterate over all book IDs
          2. For each ID, call `download_one()`

        :param book_ids: A list of book identifiers to download.
        """
        self.prepare()

        for idx, book_id in enumerate(book_ids, start=1):
            self.logger.debug(
                "[downloader] Starting download for book_id: %s (%s/%s)",
                book_id,
                idx,
                len(book_ids),
            )
            try:
                self.download_one(book_id)
            except Exception as e:
                self._handle_download_exception(book_id, e)

    @abc.abstractmethod
    def download_one(self, book_id: str) -> None:
        """
        The full download logic for a single book.

        Subclasses must implement this method.

        :param book_id: The identifier of the book to download.
        """
        ...

    def prepare(self) -> None:
        """
        Optional hook called before downloading each book.

        Subclasses can override this method to perform pre-download setup.
        """
        return

    @property
    def requester(self) -> SyncRequesterProtocol:
        """
        Access the current requester.

        :return: The internal requester instance.
        """
        return self._requester

    @property
    def parser(self) -> ParserProtocol:
        """
        Access the current parser.

        :return: The internal parser instance.
        """
        return self._parser

    @property
    def saver(self) -> SaverProtocol:
        """
        Access the current saver.

        :return: The internal saver instance.
        """
        return self._saver

    @property
    def config(self) -> DownloaderConfig:
        """
        Access the downloader configuration.

        :return: The internal DownloaderConfig object.
        """
        return self._config

    @property
    def raw_data_dir(self) -> Path:
        """
        Access the root directory for storing raw downloaded data.

        :return: Path to the raw data directory.
        """
        return self._raw_data_dir

    @property
    def cache_dir(self) -> Path:
        """
        Access the directory used for temporary caching during download.

        :return: Path to the cache directory.
        """
        return self._cache_dir

    @property
    def site(self) -> str:
        return self._site

    @property
    def save_html(self) -> bool:
        return self._config.save_html

    @property
    def skip_existing(self) -> bool:
        return self._config.skip_existing

    @property
    def login_required(self) -> bool:
        return self._config.login_required

    @property
    def request_interval(self) -> float:
        return self._config.request_interval

    def set_requester(self, requester: SyncRequesterProtocol) -> None:
        """
        Replace the requester instance with a new one.

        :param requester: The new requester to be used.
        """
        self._requester = requester

    def set_parser(self, parser: ParserProtocol) -> None:
        """
        Replace the parser instance with a new one.

        :param parser: The new parser to be used.
        """
        self._parser = parser

    def set_saver(self, saver: SaverProtocol) -> None:
        """
        Replace the saver instance with a new one.

        :param saver: The new saver to be used.
        """
        self._saver = saver

    def _handle_download_exception(self, book_id: str, error: Exception) -> None:
        """
        Handle download errors in a consistent way.

        This method can be overridden or extended to implement retry logic, etc.

        :param book_id: The ID of the book that failed.
        :param error: The exception raised during download.
        """
        self.logger.warning("[downloader] Failed to download %s: %s", book_id, error)
