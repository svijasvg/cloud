import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'readme.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-svija',
    version='2.0.17',
    packages=find_packages(),
    include_package_data=True,
    license='BSD License',
    description='A CMS for web sites built with Adobe Illustrator pages.',
    long_description=README,
    url='https://docs.svija.com/',
    author='Andrew Swift',
    author_email='andrew@svija.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.2.1',  # replace "X.Y" as appropriate
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',  # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
