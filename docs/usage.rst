Usage Guide
===========

Installation
------------

Install using pip:

.. code-block:: bash

   pip install torhost

Or from source:

.. code-block:: bash

   git clone https://github.com/bytebreach/torhost.git
   cd torhost
   sudo python3 setup.py install

Quick Start
-----------

Start a local service:

.. code-block:: bash

   python3 -m http.server 8080 &

Create a Tor hidden service:

.. code-block:: bash

   sudo torhost --port 8080

The onion address will be printed in the terminal.

Options
-------

- ``--port`` – Local port to expose (default: 8080)
