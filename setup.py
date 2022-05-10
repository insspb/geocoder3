

import re
from codecs import open

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('geocoder/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')

with open('README.md', 'r', 'utf-8') as f:
    readme = f.read()

requires = ['requests', 'ratelim', 'click', 'six', 'future']

setup(
    name='geocoder3',
    version=version,
    description="Geocoder is a simple and consistent geocoding library.",
    long_description=readme,
    long_description_content_type="text/markdown",
    author='Andrey Shpak',
    author_email='ashpak@ashpak.ru',
    url='https://github.com/insspb/geocoder3',
    download_url='https://github.com/insspb/geocoder3',
    license="The MIT License",
    entry_points='''
        [console_scripts]
        geocode=geocoder.cli:cli
    ''',
    packages=['geocoder'],
    package_data={'': ['LICENSE', 'README.md']},
    package_dir={'geocoder': 'geocoder'},
    include_package_data=True,
    install_requires=requires,
    zip_safe=False,
    keywords='geocoder arcgis tomtom opencage google bing here',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Internet',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Scientific/Engineering :: GIS',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
