_MAJOR = "1"
_MINOR = "1"
# On main and in a nightly release the patch should be one ahead of the last
# released build.
_PATCH = "0"
# This is mainly for nightly builds which have the suffix ".dev$DATE". See
# https://semver.org/#is-v123-a-semantic-version for the semantics.
_SUFFIX = ""

__version__ = f'{_MAJOR}.{_MINOR}.{_PATCH}'
__version_dev__ = f'{__version__}{_SUFFIX}'
__version_short__ = f'{_MAJOR}.{_MINOR}'