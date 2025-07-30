AUTHOR = 'Vsevolod Novikov'
AUTHOR_EMAIL = 'nnseva@gmail.com'
URL = 'https://github.com/nnseva/django2-postgres-backport'

import django2_postgres

from setuptools import setup, find_packages

description = 'Django 2.x PostgreSQL backports collection'

with open('README.rst') as f:
    long_description = f.read()

setup(
    name = 'django2-postgres-backport',
    version = django2_postgres.__version__,
    description = description,
    long_description = long_description,
    author = AUTHOR,
    author_email = AUTHOR_EMAIL,
    url = URL,
    packages = [
        'django2_postgres',
    ],
    include_package_data = True,
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        'Development Status :: 4 - Beta',
        "Framework :: Django",
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Framework :: Django :: 3.1',
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
    ],
    keywords="django postgres backport",
    license='LGPL',
    zip_safe = False,
    install_requires=['packaging']
)
