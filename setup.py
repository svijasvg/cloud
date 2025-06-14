import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-svija',
    version='2.3.3',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'svija': [
            'locale/*/LC_MESSAGES/*.mo',
            'locale/*/LC_MESSAGES/*.po',
        ]
    },

#   package_data={'fixtures': ['svija/fixtures/*.json']},
    license='MIT License',
    description='A CMS for web sites built with Adobe Illustrator pages.',
    long_description=README,
    url='https://tech.svija.com/',
    author='Andrew Swift',
    author_email='hello@svija.com',
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
