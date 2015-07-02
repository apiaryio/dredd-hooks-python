===================================================
Python Hooks Bridge for Dredd API Testing Framework
===================================================

About
=====

This package contains a bridge between `Dredd API Testing Framework`_
and Python environment to ease implementation of testing hooks
provided by Dredd_. Write Dredd_ hooks in Python to glue together `API
Blueprint`_ with your Python project

.. _Dredd API Testing Framework: http://dredd.readthedocs.org/en/latest/
.. _Dredd: http://dredd.readthedocs.org/en/latest/
.. _API Blueprint: https://apiblueprint.org/



Usage example::

    import dredd_hooks as dredd

    @dredd.before_all
    def foo(transactions):
        for t in transactions:
            t['foo'] = bar

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

     import dredd_hooks as dredd

     @dredd.before("Machines > Machines collection > Get Machines")
     def before_hook(transaction):
         transaction['skip'] = "true"


2. Run it with Dredd::

     $ dredd apiary.apib localhost:3000 --language python --hookfiles hooks.py

API
===

Module ``dredd_hooks`` defines following decorators ``before``, ``after``,
``before_all``, ``after_all``, ``before_each``, ``after_each``,
``before_validation``, ``before_each_validation``. ``before``,
``before_validation`` and ``after`` hooks are identified by `transaction
name
<http://dredd.readthedocs.org/en/latest/hooks/#getting-transaction-names>`_.

Usage is very similar to `sync JS hooks API
<http://dredd.readthedocs.org/en/latest/hooks/#sync-api>`_

Contributing
============
1. Fork it
2. Create your feature branch (``git checkout -b my-newfeature``)
3. Commit your changes (``git commit -am 'Add some feature'``)
4. Push (``git push origin my-new-feature``)
5. Create a new Pull Request

:copyright: Copyright 2015 by Vilibald Wanča.
:license: MIT, see LICENSE for details.

