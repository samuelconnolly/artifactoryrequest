"""
python-setuptools definition for mkbranch
"""

from setuptools import setup, find_packages

setup(name='ArtifactoryRequest',
      version='1.0.0',
      setup_requires=['setuptools_scm'],
      install_requires=['gitpython'],
      packages=find_packages('src'),
      package_dir={'': 'src'})
