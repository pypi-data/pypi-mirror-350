import os

from setuptools import find_packages
from setuptools import setup


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


long_description = (
    read('README.rst')
    + '\n' +
    read('CHANGES.rst')
)


tests_require = [
    'zope.testing',
    'zope.testrunner',
]

setup(
    name='grokcore.error',
    version='4.1',
    author='Grok Team',
    author_email='zope-dev@zope.dev',
    url='https://github.com/zopefoundation/grokcore.error',
    download_url='http://pypi.python.org/pypi/grokcore.startup',
    description='Paster support for Grok projects.',
    long_description=long_description,
    license='ZPL',
    keywords='zope zope3 grok grokproject WSGI Paste paster',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Framework :: Zope :: 3',
    ],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['grokcore'],
    include_package_data=True,
    zip_safe=False,
    python_requires='>=3.9',
    install_requires=[
        'grokcore.component',
        'setuptools',
        'zope.component',
        'zope.configuration',
        'zope.error',
        'zope.interface',
        'zope.publisher',
    ],
    tests_require=tests_require,
    extras_require={'test': tests_require},
)
