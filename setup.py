"""
python-setuptools definition for mkbranch
"""

from setuptools import setup, find_packages

setup(name='ArtifactoryRequest',
      use_scm_version=True,
      setup_requires=['setuptools_scm'],
      install_requires=['gitpython'],
      packages=find_packages('src'),
      package_dir={'': 'src'})
