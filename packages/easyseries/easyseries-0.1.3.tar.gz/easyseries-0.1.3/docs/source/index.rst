EasySeries Documentation
========================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   quickstart
   api
   modules/index

EasySeries is a comprehensive HTTP utility toolkit built on httpx with CLI support.
It provides modern Python developers with a robust foundation for building HTTP clients
and utilities with advanced features like rate limiting, metrics collection, retry logic,
and comprehensive error handling.

Features
--------

* 🚀 **Modern Python**: Built with Python 3.10+ using the latest async/await patterns
* 🔧 **httpx Integration**: Leverages the powerful httpx library for HTTP operations
* 📊 **Metrics & Monitoring**: Built-in request metrics and performance tracking
* 🛡️ **Error Handling**: Comprehensive error handling with custom exceptions
* ⚡ **Rate Limiting**: Configurable rate limiting to respect API limits
* 🔄 **Retry Logic**: Intelligent retry mechanisms with exponential backoff
* 🎯 **CLI Interface**: Friendly command-line interface for testing and utilities
* 📝 **Type Safety**: Full type hints for better development experience
* ⚙️ **Configuration**: Flexible configuration with environment variable support

Quick Example
-------------

.. code-block:: python

   import asyncio
   from easyseries import HTTPClient

   async def main():
       async with HTTPClient(base_url="https://api.example.com") as client:
           response = await client.get("/users")
           users = response.json()
           print(f"Found {len(users)} users")

   asyncio.run(main())

CLI Usage
---------

.. code-block:: bash

   # Make a simple GET request
   easyseries request https://httpbin.org/get

   # POST with JSON data
   easyseries request https://httpbin.org/post \
       --method POST \
       --data '{"name": "John", "age": 30}'

   # Benchmark an endpoint
   easyseries benchmark https://httpbin.org/get \
       --requests 100 \
       --concurrency 10

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
