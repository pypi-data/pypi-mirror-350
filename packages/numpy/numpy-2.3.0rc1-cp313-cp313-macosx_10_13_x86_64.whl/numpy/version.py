
"""
Module to expose more detailed version info for the installed `numpy`
"""
version = "2.3.0rc1"
__version__ = version
full_version = version

git_revision = "3abd5872db8b87f350ad1a7c931f8d8cee62c1fa"
release = 'dev' not in version and '+' not in version
short_version = version.split("+")[0]
