
"""
Module to expose more detailed version info for the installed `numpy`
"""
version = "1.1.0a1"
__version__ = version
full_version = version

git_revision = "9b6f45995103a9ff8c0b2611193fef3d056cf32d"
release = 'dev' not in version and '+' not in version
short_version = version.split("+")[0]
