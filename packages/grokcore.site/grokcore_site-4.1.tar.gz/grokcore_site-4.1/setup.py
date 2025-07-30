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
    'zope.app.appsetup',
    'zope.component',
    'zope.configuration',
    'zope.testing',
    'grokcore.content',
]

setup(
    name='grokcore.site',
    version='4.1',
    author='Grok Team',
    author_email='zope-dev@zope.dev',
    url='https://github.com/zopefoundation/grokcore.site',
    description='Grok-like configuration for Zope local site and utilities',
    long_description=long_description,
    license='ZPL',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Zope :: 3',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python',
    ],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['grokcore'],
    include_package_data=True,
    zip_safe=False,
    python_requires='>=3.9',
    install_requires=['setuptools',
                      'grokcore.component >= 2.1',
                      'martian >= 0.13',
                      'persistent',
                      'zope.annotation',
                      'zope.component',
                      'zope.container',
                      'zope.event',
                      'zope.interface',
                      'zope.lifecycleevent',
                      'zope.schema',
                      'zope.site >= 4.4',
                      ],
    tests_require=tests_require,
    extras_require={'test': tests_require},
)
