### IMPORTS
### ============================================================================
## Standard Library
import datetime

### CONSTANTS
### ============================================================================
## Version Information
## -----------------------------------------------------------------------------
VERSION = '0.1.0'
BUILD_GIT_HASH = 'g9dadbdc16e7be4e80b8cd0cd9f181fe626bac3e0'
BUILD_GIT_HASH_SHORT = BUILD_GIT_HASH[:8] if BUILD_GIT_HASH is not None else None
BUILD_GIT_BRANCH = 'main'
BUILD_GIT_DIRTY = False
BUILD_DATETIME = datetime.datetime(2024, 5, 11, 7, 12, 8, 777949, tzinfo=datetime.timezone.utc)
BUILD_TIMESTAMP = int(BUILD_DATETIME.timestamp())

## Version Information Templates
## -----------------------------------------------------------------------------
VERSION_INFO_SHORT = f"{VERSION}"
VERSION_INFO = f"{VERSION}@{BUILD_GIT_HASH_SHORT}"
VERSION_INFO_LONG = f"{VERSION} ({BUILD_GIT_BRANCH}@{BUILD_GIT_HASH_SHORT})"
VERSION_INFO_FULL = (
    f"{VERSION} ({BUILD_GIT_BRANCH}@{BUILD_GIT_HASH})\n"
    f"Built: {BUILD_DATETIME}"
)
