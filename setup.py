from __future__ import with_statement


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def readme():
    with open('README.rst') as f:
        return f.read()


if sys.version_info >= (3,4):
    install_requires = []
else:
    install_requires = ['asyncio']


setup(
    name='aioirc',
    packages = ['aioirc']
    version='0.1',
    description='AsyncIO IRC Library for >= Python 3.3',
    long_description=readme(),
    url='https://github.com/devunt/aioirc',
    download_url='',
    author='JuneHyeon Bae',
    author_email='devunt' '@' 'gmail.com',
    license='License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
    py_modules=['aioirc'],
    keywords = ['irc', 'asyncio']
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Communications :: Chat :: Internet Relay Chat',
    ],
    install_requires = install_requires,
)
