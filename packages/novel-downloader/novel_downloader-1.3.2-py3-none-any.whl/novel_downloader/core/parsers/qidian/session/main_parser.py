#!/usr/bin/env python3
"""
novel_downloader.core.parsers.qidian.session.main_parser
--------------------------------------------------------

Main parser class for handling Qidian chapters rendered via a session.

This module defines `QidianSessionParser`, a parser implementation that supports
content extracted from dynamically rendered Qidian HTML pages.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any

from novel_downloader.config.models import ParserConfig
from novel_downloader.core.parsers.base import BaseParser
from novel_downloader.utils.chapter_storage import ChapterDict
from novel_downloader.utils.state import state_mgr

from ..shared import (
    is_encrypted,
    parse_book_info,
)
from .chapter_router import parse_chapter

if TYPE_CHECKING:
    from novel_downloader.utils.fontocr import FontOCR


class QidianSessionParser(BaseParser):
    """
    Parser for Qidian site using a session HTML workflow.
    """

    def __init__(self, config: ParserConfig):
        """
        Initialize the QidianBrowserParser with the given configuration.

        :param config: ParserConfig object controlling:
        """
        super().__init__(config)

        # Extract and store parser flags from config
        self._decode_font: bool = config.decode_font
        self._save_font_debug: bool = config.save_font_debug

        self._fixed_font_dir: Path = self._base_cache_dir / "fixed_fonts"
        self._fixed_font_dir.mkdir(parents=True, exist_ok=True)
        self._font_debug_dir: Path | None = None

        qd_cookies = state_mgr.get_cookies("qidian")
        self._fuid: str = qd_cookies.get("ywguid", "")

        self._font_ocr: FontOCR | None = None
        if self._decode_font:
            from novel_downloader.utils.fontocr import FontOCR

            self._font_ocr = FontOCR(
                cache_dir=self._base_cache_dir,
                use_freq=config.use_freq,
                use_ocr=config.use_ocr,
                use_vec=config.use_vec,
                batch_size=config.batch_size,
                gpu_mem=config.gpu_mem,
                gpu_id=config.gpu_id,
                ocr_weight=config.ocr_weight,
                vec_weight=config.vec_weight,
                font_debug=config.save_font_debug,
            )
            self._font_debug_dir = self._base_cache_dir / "qidian" / "font_debug"
            self._font_debug_dir.mkdir(parents=True, exist_ok=True)

    def parse_book_info(
        self,
        html_str: list[str],
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        Parse a book info page and extract metadata and chapter structure.

        :param html_str: Raw HTML of the book info page.
        :return: Parsed metadata and chapter structure as a dictionary.
        """
        if not html_str:
            return {}
        return parse_book_info(html_str[0])

    def parse_chapter(
        self,
        html_str: list[str],
        chapter_id: str,
        **kwargs: Any,
    ) -> ChapterDict | None:
        """
        :param html: Raw HTML of the chapter page.
        :param chapter_id: Identifier of the chapter being parsed.
        :return: Cleaned chapter content as plain text.
        """
        if not html_str:
            return None
        return parse_chapter(self, html_str[0], chapter_id)

    def is_encrypted(self, html_str: str) -> bool:
        """
        Return True if content is encrypted.

        :param html: Raw HTML of the chapter page.
        """
        return is_encrypted(html_str)

    def _init_cache_folders(self) -> None:
        """
        Prepare cache folders for plain/encrypted HTML and font debug data.
        Folders are only created if corresponding debug/save flags are enabled.
        """
        base = self._base_cache_dir

        # Font debug folder
        if self._save_font_debug and self.book_id:
            self._font_debug_dir = base / self.book_id / "font_debug"
            self._font_debug_dir.mkdir(parents=True, exist_ok=True)
        else:
            self._font_debug_dir = None

    def _on_book_id_set(self) -> None:
        self._init_cache_folders()
