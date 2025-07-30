Installation
============

Requirements
------------

* Python 3.10 or higher
* pip or uv (recommended)

Installing from PyPI
--------------------

The easiest way to install EasySeries is using pip:

.. code-block:: bash

   pip install easyseries

Or using uv (recommended for faster installation):

.. code-block:: bash

   uv add easyseries

Development Installation
------------------------

For development, clone the repository and install with development dependencies:

.. code-block:: bash

   git clone https://github.com/ScienisTmiaoT/easyseries.git
   cd easyseries
   uv sync --all-extras --dev

This will install:

* All runtime dependencies
* Development tools (pytest, ruff, mypy, etc.)
* Documentation tools (sphinx, etc.)

Optional Dependencies
--------------------

EasySeries has several optional dependency groups:

.. code-block:: bash

   # Install with development tools
   pip install "easyseries[dev]"

   # Install with documentation tools
   pip install "easyseries[docs]"

   # Install with testing tools
   pip install "easyseries[test]"

   # Install everything
   pip install "easyseries[dev,docs,test]"

Verifying Installation
---------------------

You can verify the installation by running:

.. code-block:: bash

   easyseries version

This should display the current version of EasySeries.

You can also check the configuration:

.. code-block:: bash

   easyseries config
