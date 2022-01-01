.. masa filter MASA freedivers

.. _developer_guide:

***************
Developer Guide
***************


Overview
========

Installation
============

Install the package in a *virtualenv* then install *masa* in *developer* mode

.. code-block:: bash

        python3.7 -m venv masa
        cd masa
        source bin/activate
        mkdir src
        cd src
        tar -xzf masa-<version>.tar.gz
        cd masa
        pip install -e .[dev]


Dependecies
-----------

* python >= 3.7
* pandas
* sphinx
* sphinx_rtd_theme
* sphinx-autodoc-typehints
* coverage
* build


Building new release
====================

At the package root directory.

.. code:: bash

    python -m build .


Reference API
=============

.. automodule:: masa
   :members:
   :private-members:
   :special-members:

.. automodule:: masa.scripts.masa_email
   :members:
   :private-members:
   :special-members: