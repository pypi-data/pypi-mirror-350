
"""
Module to expose more detailed version info for the installed `numpy`
"""
version = "2.3.0rc1"
__version__ = version
full_version = version

git_revision = "1d7b93477b5fe94343990ee00171fb501f59a609"
release = 'dev' not in version and '+' not in version
short_version = version.split("+")[0]
