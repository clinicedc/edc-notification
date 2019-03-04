import os
from setuptools import find_packages
from setuptools import setup
from os.path import join, abspath, normpath, dirname


with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

with open(os.path.join(os.path.dirname(__file__), 'VERSION')) as f:
    VERSION = f.read()

tests_require = ["requests_mock", "edc-model-admin", "edc-sites"]
with open(join(dirname(abspath(__file__)), 'requirements.txt')) as f:
    for line in f:
        tests_require.append(line.strip())

# allow setup.py to be run from any path
os.chdir(normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='edc_notification',
    version=VERSION,
    author=u'Erik van Widenfelt',
    author_email='ew2789@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    url='http://github.com/clinicedc/edc-notification',
    license='GPL license, see LICENSE',
    description='Simple notification classes for clinic/edc',
    long_description=README,
    zip_safe=False,
    keywords='edc notification',
    install_requires=[
        'django_simple_history',
        'edc-model',
        'edc-utils',
        'requests'
        'twilio',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    python_requires=">=3.7",
    tests_require=tests_require,
    test_suite='runtests.main',
)
