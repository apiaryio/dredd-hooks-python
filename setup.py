# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

long_desc = open('README.rst').read()

setup(
    name='dredd_hooks',
    version='0.2.0',
    url='https://github.com/apiaryio/dredd-hooks-python/',
    download_url='http://pypi.python.org/pypi/dredd_hooks',
    license='MIT License',
    author='Vilibald Wanča',
    author_email='vilibald.wanca@oracle.com',
    maintainer='Apiary',
    maintainer_email='support@apiary.io',
    description='Python Hooks Bridge for Dredd API Testing Framework',
    long_description=long_desc,
    zip_safe=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
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
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'dredd-hooks-python = dredd_hooks.__main__:main'
        ],
    },
    tests_require=['flake8'],
    test_suite='test',
)
