import threading
from _typeshed import Incomplete
from collections.abc import Generator
from tlc.core.objects.tables.system_tables.indexing import _BlacklistExceptionHandler, _ScanUrl
from tlc.core.objects.tables.system_tables.project_scan_iterator import _ProjectScanIterator
from tlc.core.url import Url as Url
from tlc.core.url_adapter import UrlAdapterDirEntry as UrlAdapterDirEntry
from tlc.core.url_adapter_registry import UrlAdapterRegistry as UrlAdapterRegistry

logger: Incomplete

class _ProjectConfigScanIterator(_ProjectScanIterator):
    """A scan iterator that yields all Config from a 3LC directory layout.

    Config files are stored in a fixed folder structure:
        - Pattern: <projects_dir>/<project_name>/config.3lc.yaml
        - Glob: <projects_dir>/*/config.3lc.yaml
    """
    def __init__(self, scan_url: _ScanUrl, tag: str, blacklist_config: list[_BlacklistExceptionHandler] | None, stop_event: threading.Event | None = None) -> None: ...
    def scan(self) -> Generator[UrlAdapterDirEntry, None, None]: ...
    def scan_project_url(self, project_url: Url, depth: int) -> Generator[UrlAdapterDirEntry, None, None]: ...
