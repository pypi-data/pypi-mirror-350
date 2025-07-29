from __future__ import annotations
import time
from pathlib import Path
from typing import Union
from ooodev.utils.cache.file_cache.cache_base import CacheBase


class TextCache(CacheBase):
    """
    Singleton Class.
    Caches files and retrieves cached files.
    Cached file are in a subfolder of system tmp dir.
    """

    def get(self, filename: str) -> Union[str, None]:  # type: ignore
        """
        Fetches file contents from cache if it exist and is not expired

        Args:
            filename (str): File to retrieve

        Returns:
            Union[str, None]: File contents if retrieved; Otherwise, ``None``
        """
        if not filename:
            raise ValueError("filename is required")

        if self.seconds <= 0:
            return None
        f = Path(self.path, filename)
        if not f.exists():
            return None

        if self.can_expire:
            f_stat = f.stat()
            if f_stat.st_size == 0:
                # should not be zero byte file.
                try:
                    self.remove(f)
                except Exception as e:
                    self.logger.warning("Not able to delete 0 byte file: %s, error: %s", filename, e)
                return None
            ti_m = f_stat.st_mtime
            age = time.time() - ti_m
            if age >= self.seconds:
                return None

        try:
            # Check if we have this file locally

            with open(f, encoding="utf-8") as fin:
                content = fin.read()
            # If we have it, let's send it
            return content
        except IOError:
            return None

    def put(self, filename: str, content: str) -> None:
        """
        Saves file contents into cache

        Args:
            filename (str): filename to write.
            content (str): Contents to write into file.
        """
        if not filename:
            raise ValueError("filename is required")

        f = Path(self.path, filename)
        # print('Saving a copy of {} in the cache'.format(filename))
        with open(f, "w", encoding="utf-8") as cached_file:
            cached_file.write(content)
