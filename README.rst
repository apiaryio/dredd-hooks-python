===================================================
Python Hooks Bridge for Dredd API Testing Framework
===================================================

.. image:: https://travis-ci.org/apiaryio/dredd-hooks-python.svg?branch=master
    :target: https://travis-ci.org/apiaryio/dredd-hooks-python

About
=====

This package contains a bridge between `Dredd API Testing Framework`_
and Python environment to ease implementation of testing hooks
provided by Dredd_. Write Dredd_ hooks in Python to glue together `API
Blueprint`_ with your Python project

.. _Dredd API Testing Framework: http://dredd.readthedocs.org/en/latest/
.. _Dredd: http://dredd.readthedocs.org/en/latest/
.. _API Blueprint: https://apiblueprint.org/



Usage example:

.. code-block:: python

    import dredd_hooks as hooks

    @hooks.before_all
    def foo(transactions):
        for t in transactions:
            t['request']['headers']['content-type'] = 'application/json'

Download
========

You can see all the `available versions`__ at PyPI_.

__ http://pypi.python.org/pypi/dredd_hooks


From source (tar.gz or checkout)
--------------------------------

Unpack the archive, enter the ``dredd-hooks-python`` directory and run::

    python setup.py install


Setuptools/PyPI_
----------------

Alternatively it can be installed from PyPI_, either manually
downloading the files and installing as described above or using::

    pip install dredd_hooks

.. _PyPI: http://pypi.python.org/pypi

Usage
=====

1. Create a hook file in ``hooks.py``:

.. code-block:: python

     import dredd_hooks as hooks

     @hooks.before("Machines > Machines collection > Get Machines")
     def before_hook(transaction):
         transaction['skip'] = "true"


2. Run it with Dredd::

     $ dredd apiary.apib localhost:3000 --language python --hookfiles ./hooks.py

API
===

Module ``dredd_hooks`` defines following decorators ``before``, ``after``,
``before_all``, ``after_all``, ``before_each``, ``after_each``,
``before_validation``, ``before_each_validation``. ``before``,
``before_validation`` and ``after`` hooks are identified by `transaction
name
<http://dredd.readthedocs.org/en/latest/hooks/#getting-transaction-names>`_.

You can combine those decorators together. So one function can be used
for different hooks but be aware that some hooks have a list of all
transactions as an argument and not a single transaction.

.. code-block:: python

     import dredd_hooks as hooks

     @hooks.after_all
     @hooks.before_all
     @hooks.before_each
     @hooks.after_each
     @hooks.before_validation('Machines > Machines collection > Get Machines')
     @hooks.before("Machines > Machines collection > Get Machines")
     @hooks.after("Machines > Machines collection > Get Machines")
     def multi_hook_function(trans):
        if isinstance(trans, list):
            print('called with list of transactions')
        else:
            if trans['name'] == 'Machines > Machines collection > Get Machines':
                trans['skip'] = 'true'


Usage is very similar to `sync JS hooks API
<http://dredd.readthedocs.org/en/latest/hooks/#sync-api>`_

Contributing
============
1. Fork it
2. Create your feature branch (``git checkout -b my-newfeature``)
3. Commit your changes (``git commit -am 'Add some feature'``)
4. Push (``git push origin my-new-feature``)
5. Create a new Pull Request

Testing
=======

Don't forget about tests, see ``test`` directory. The project uses
``unittest`` package and ``tox``.

For integration test with Dredd_ interface the project uses ruby based
`aruba <https://github.com/cucumber/aruba>`_ so to get it running make
sure you have Ruby installed and then do::

  $ bundle install

After the setup you can run the test easily with::

  $ bundle exec cucumber

More details about the integration test can be found in the
`dredd-hooks-template repo
<https://github.com/apiaryio/dredd-hooks-template>`_


:copyright: Copyright (c) 2015 Apiary Czech Republic, s.r.o.
:license: MIT, see LICENSE for details.

