Djamo Installing / Upgrading
============================
.. highlight:: bash

**Djamo** is in the `Python Package Index
<http://pypi.python.org/pypi/pymongo/>`_.

Dependencies
------------
**Djamo** depends on:

* Pymongo
* Sphinx(for documents)

.. note:: You need sphinx package only when you install Djamo from source and
          need to build its documents.

.. note:: Don't bother about dependencies if you use ``pip`` for installing.

Installing with pip
-------------------

We prefer `pip <http://pypi.python.org/pypi/pip>`_
to install Djamo::

  $ pip install djamo

To get a specific version of Djamo::

  $ pip install djamo==2.67.0

To upgrade using pip::

  $ pip install --upgrade djamo

Installing with easy_install
----------------------------

If you must install Djamo using
`setuptools <http://pypi.python.org/pypi/setuptools>`_ do::

  $ easy_install djamo

To upgrade do::

  $ easy_install -U djamo


Installing from source
----------------------

If you'd rather install directly from the source (i.e. to stay on the
bleeding edge), Install the Djamo dependencies first and the check out
the latest source from github and install the
driver from the resulting tree::

  $ git clone git://github.com/Yellowen/Djamo.git
  $ cd Djamo
  $ python setup.py install
