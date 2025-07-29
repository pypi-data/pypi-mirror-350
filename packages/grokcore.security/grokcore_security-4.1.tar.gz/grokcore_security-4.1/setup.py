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
    'grokcore.view[test]',
    'zope.app.wsgi',
    'zope.configuration',
    'zope.securitypolicy',
    'zope.testing',
]

setup(
    name='grokcore.security',
    version='4.1',
    author='Grok Team',
    author_email='zope-dev@zope.dev',
    url='https://github.com/zopefoundation/grokcore.security',
    description='Grok-like configuration for Zope security components',
    long_description=long_description,
    license='ZPL',
    classifiers=[
        'Intended Audience :: Developers',
        'Development Status :: 6 - Mature',
        'License :: OSI Approved :: Zope Public License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['grokcore'],
    include_package_data=True,
    zip_safe=False,
    python_requires='>=3.9',
    install_requires=[
        'Chameleon >= 2',
        'grokcore.component >= 2.1',
        'martian >= 0.13',
        'setuptools',
        'zope.component',
        'zope.dottedname',
        'zope.interface',
        'zope.security',
    ],
    tests_require=tests_require,
    extras_require={
        'role': [
            'zope.securitypolicy',
        ],
        'test': tests_require
    },
)
