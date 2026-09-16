"""CoCGEC data preparation toolkit."""

from .annotation import annotate_record, annotate_records, error_range

__all__ = ["annotate_record", "annotate_records", "error_range"]
__version__ = "0.1.0"
