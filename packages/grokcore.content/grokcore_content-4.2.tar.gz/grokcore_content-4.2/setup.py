import os

from setuptools import find_packages
from setuptools import setup


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


long_description = "{}\n\n.. contents::\n\n{}".format(
    read('README.rst'), read('CHANGES.rst'))
install_requires = [
    'setuptools',
    'persistent',
    'grokcore.component >= 2.1',
    'zope.annotation',
    'zope.container',
    'zope.interface',
    'zope.lifecycleevent',
]
tests_require = [
    'zope.component',
    'zope.testing',
    'zope.testrunner',
]

setup(
    name='grokcore.content',
    version='4.2',
    author='Grok Team',
    author_email='zope-dev@zope.dev',
    url='https://github.com/zopefoundation/grokcore.content',
    download_url='https://pypi.org/project/grokcore.content',
    description='Base content types for Grok',
    long_description=long_description,
    license='ZPL',
    python_requires='>=3.9',
    install_requires=install_requires,
    extras_require={'test': tests_require},
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['grokcore'],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Framework :: Zope :: 3',
        'License :: OSI Approved :: Zope Public License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
)
