# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

long_desc = ''' This package contains a bridge between `Dredd API Testing
Framework`_ and Python environment to ease implementation of testing
hooks provided by Dredd_. Write Dredd_ hooks in Python to glue together
`API Blueprint`_ with your Python project

.. _Dredd API Testing Framework: http://dredd.readthedocs.org/en/latest/
.. _Dredd: http://dredd.readthedocs.org/en/latest/
.. _API Blueprint: https://apiblueprint.org/

Usage example::

    import dredd_hooks as dredd

    @dredd.before_all
    def foo(transactions):
        for t in transactions:
            t['foo'] = bar
'''

requires = ['']

setup(
    name='dredd_hooks',
    version='0.0.1',
    url='https://github.com/apiaryio/dredd-hooks-python/',
    download_url='http://pypi.python.org/pypi/dredd_hooks',
    license='MIT License',
    author='Vilibald Wanča',
    author_email='wvi@apiary.io',
    description='Python Hooks Bridge for Dredd API Testing Framework',
    long_description=long_desc,
    zip_safe=False,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Testing',
        'Topic :: Software Development :: Build Tools',
    ],
    keywords='HTTP API testing Dredd',
    platforms='any',
    scripts=['bin/dredd-hooks-python'],
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
    namespace_packages=[],
    test_suite="test",
)
