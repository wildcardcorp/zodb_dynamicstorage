import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()

requires = [
    #'ZODB3==3.10.5'
    #'ZODB',
    #'ZEO'
]

setup(name='zodb_dynamicstorage',
      version='1.0',
      description='',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python"
        ],
      author='',
      author_email='',
      url='',
      keywords='',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      entry_points="""\
      """,
      )
