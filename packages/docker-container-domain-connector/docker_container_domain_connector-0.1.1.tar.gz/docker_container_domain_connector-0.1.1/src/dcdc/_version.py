### IMPORTS
### ============================================================================
## Standard Library
import datetime

### CONSTANTS
### ============================================================================
## Version Information
## -----------------------------------------------------------------------------
VERSION = '0.1.1'
BUILD_GIT_HASH = 'gd3c8a21d92ac25fb5d4ae453970b1e0f7a843d2f'
BUILD_GIT_HASH_SHORT = BUILD_GIT_HASH[:8] if BUILD_GIT_HASH is not None else None
BUILD_GIT_BRANCH = 'main'
BUILD_GIT_DIRTY = False
BUILD_DATETIME = datetime.datetime(2025, 5, 24, 2, 50, 57, 999189, tzinfo=datetime.timezone.utc)
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
