"""
프로젝트명 패키지
"""

try:
    from qore_client.version import __version__
except ImportError:
    __version__ = "unknown"

from qore_client.client import QoreClient

__all__ = ["QoreClient"]
