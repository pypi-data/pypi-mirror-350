import threading
from _typeshed import Incomplete
from collections.abc import Sequence
from tlc.core.objects.tables.system_tables.indexing import _UrlContent
from tlc.core.url import Url as Url
from tlc.core.url_adapter import UrlAdapterDirEntry as UrlAdapterDirEntry
from tlc.core.url_adapter_registry import UrlAdapterRegistry as UrlAdapterRegistry
from typing import Callable

logger: Incomplete

class _UrlReaderWorker(threading.Thread):
    '''A threaded class that periodically reads files from a _ThreadedDirectoryFileIndexer instance.

    :Example:

    ```python
    scan_urls = ["./path/to/dir", "./another/path"]
    indexer = _UrlIndexingWorker(scan_urls)
    file_reader = _UrlReaderWorker(indexer)
    file_reader.start()
    # Get the file contents
    files = file_reader.get_files()
    ```

    :param indexer: An instance of _UrlIndexingWorker which provides the index scanning.
    '''
    def __init__(self, index_event: threading.Event, index_getter: Callable[[], dict[Url, Sequence[UrlAdapterDirEntry]]], tag: str = '', stop_signal: threading.Event = ...) -> None: ...
    def is_reading(self) -> bool:
        """Returns whether the reader is currently reading files."""
    def remove_scan_url(self, url: Url) -> None:
        """Remove a scan URL from the reader."""
    @property
    def counter(self) -> int:
        """Returns the number of times files have been read by the reader."""
    def run(self) -> None:
        """Method representing the thread's activity.

        Do not call this method directly. Use the start() method instead, which will in turn call this method.
        """
    def start(self) -> None: ...
    def stop(self) -> None:
        """Method to signal the thread to stop its activity.

        This doesn't terminate the thread immediately, but flags it to exit when it finishes its current iteration.
        """
    def update_files_for_scan_url(self, base_url: Url, current_index: dict[Url, _UrlContent], new_entries: Sequence[UrlAdapterDirEntry]) -> tuple[dict[Url, _UrlContent], bool]:
        """Scans for new, updated and removed files, reads their content, and stores them.

        :param base_url: Base URL being scanned
        :param current_index: Current index of URL contents
        :param new_entries: New directory entries to process
        :returns: Tuple of (updated content dictionary, whether changes were detected)
        """
    def update_files(self) -> bool:
        """Scans for new and updated files, reads their content, and stores them."""
    def touch(self) -> None:
        """Update last read timestamp."""
    def get_content(self) -> dict[Url, dict[Url, _UrlContent]]:
        """Returns a copy of the latest read Url contents partitioned per base URL.

        :returns: A dictionary of base URL to a dictionary of URL to _UrlContent instances representing the latest read
            contents.
        """
    @property
    def is_running(self) -> bool:
        """Returns the current running state."""
