import threading
from _typeshed import Incomplete
from collections.abc import Sequence
from tlc.core.objects.tables.system_tables.indexing import _BlacklistExceptionHandler, _ScanIterator, _ScanUrl
from tlc.core.objects.tables.system_tables.timestamp_helper import TimestampHelper as TimestampHelper
from tlc.core.url import Url as Url
from tlc.core.url_adapter import UrlAdapterDirEntry as UrlAdapterDirEntry
from tlc.core.url_adapter_registry import UrlAdapterRegistry as UrlAdapterRegistry

logger: Incomplete

class _ScanUrlHandler:
    def __init__(self, scan_url: _ScanUrl, blacklist_config: list[_BlacklistExceptionHandler] | None, tag: str = '', stop_event: threading.Event | None = None, extensions: Sequence[str] | None = None) -> None: ...
    @staticmethod
    def create_iterator(scan_url: _ScanUrl, blacklist_config: list[_BlacklistExceptionHandler] | None, tag: str, stop_event: threading.Event | None = None, extensions: Sequence[str] | None = None) -> _ScanIterator:
        """Get the optimal iterator for a scan URL."""
    def get_index(self, force: bool = False) -> tuple[Sequence[UrlAdapterDirEntry], bool]:
        """Get the current index and whether changes were detected.

        Performs a scan if needed based on force flag or reindex conditions.
        Returns cached results otherwise.

        :param force: Whether to force a rescan regardless of other conditions
        :return: Tuple of (scan entries, whether changes were detected)
        """
    def get_timestamp_url(self) -> Url: ...
    @staticmethod
    def are_entries_equal(previous_entries: Sequence[UrlAdapterDirEntry] | None, current_entries: Sequence[UrlAdapterDirEntry]) -> bool:
        """
        Compare two (sorted) sequences of directory entries for equality.

        :param previous_entries: Previous scan results, or None if this is first scan
        :param current_entries: Current scan results to compare against
        :return: True if sequences are identical, False if they differ
        """
    def needs_reindex(self) -> bool:
        """Check if this URL needs to be re-indexed based on various conditions.

        Determines if re-indexing is needed by checking:
           1. If there is a timestamp file and its contents are newer than the last_timestamp.
           2. If there are no previous scan results
           3. If the URL is static, it will never be re-indexed
           4. If the configured scan interval has elapsed, this is typically a large number
           5. If there are any blacklisted URLs whose retry time has expired

        :return: True if re-indexing is needed, False otherwise
        """

class _UrlIndexingWorker(threading.Thread):
    """An indexer that crawls a directory and indexes the files in it.

    This is an indexer that repeatedly performs a scan of its directories and indexes the files in it. It runs in
    a separate thread to allow for asynchronous scanning, but has an idle overhead. The indexer can be stopped and
    started again.

    The actual scanning of the directory is done by ScanIterators that wrap around URL-adapters.
    """
    def __init__(self, interval: float, blacklist_config: list[_BlacklistExceptionHandler], tag: str = '', stop_event: threading.Event | None = None, extensions: Sequence[str] | None = None) -> None: ...
    @property
    def new_index_event(self) -> threading.Event: ...
    def get_scan_urls(self) -> list[_ScanUrl]:
        """Get list of scan URLs currently being monitored."""
    def touch(self) -> None:
        """Update the timestamp of the last activity to prevent the indexer from going idle."""
    def add_scan_url(self, url_config: _ScanUrl) -> None:
        """Adds a new URL to the list of URLs to be scanned by the indexer."""
    def remove_scan_url(self, url_config: _ScanUrl) -> None:
        """Removes a URL from the list of URLs to be scanned by the indexer."""
    def handle_pending_scan_urls(self) -> bool:
        """Handle pending scan URLs."""
    def run(self) -> None:
        """Method representing the thread's activity."""
    def wait_for_complete_reindex(self, timeout: float | None = None) -> bool: ...
    def stop(self) -> None:
        """Method to signal the thread to stop its activity.

        This doesn't terminate the thread immediately, but flags it to exit when it finishes its current iteration.
        """
    def join(self, timeout: float | None = None) -> None:
        """Wait for the thread to join.

        This method will block until the thread has finished its current iteration and is ready to join.
        """
    @property
    def is_running(self) -> bool: ...
    def get_index(self) -> dict[Url, Sequence[UrlAdapterDirEntry]]: ...
    def set_index(self, new_partial_index: dict[Url, Sequence[UrlAdapterDirEntry]]) -> None:
        """Set the new index and notify any waiting threads.

        The new data may have removed entries or even be empty.
        """
    def update_index(self) -> dict[Url, Sequence[UrlAdapterDirEntry]] | None:
        """Index all Scan URLs and return an updated data structure if changes are detected.

        Scans through all registered URLs and checks if their contents have changed.
        Only performs full scans on URLs that need re-indexing, otherwise reuses
        existing index data for efficiency.

        Returns:
            A dictionary mapping URLs to their directory entries if changes
            were detected, None otherwise
        """
    def set_force(self) -> None:
        """Make sure the worker does not skip scanning in the next iteration even if no changes are detected.

        Works across all scan URLs"""
