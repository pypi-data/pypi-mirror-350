Quick Start Guide
=================

This guide will help you get started with EasySeries quickly.

Basic HTTP Client Usage
-----------------------

Creating a Simple Client
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import asyncio
   from easyseries import HTTPClient

   async def main():
       # Create a client with base URL
       async with HTTPClient(base_url="https://jsonplaceholder.typicode.com") as client:
           # Make a GET request
           response = await client.get("/posts/1")
           post = response.json()
           print(f"Post title: {post['title']}")

   asyncio.run(main())

Making Different Types of Requests
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   async def crud_examples():
       async with HTTPClient(base_url="https://api.example.com") as client:
           # GET request
           users = await client.get("/users")

           # POST request with JSON data
           new_user = await client.post("/users", json={
               "name": "John Doe",
               "email": "john@example.com"
           })

           # PUT request
           updated_user = await client.put("/users/1", json={
               "name": "John Smith",
               "email": "john.smith@example.com"
           })

           # DELETE request
           await client.delete("/users/1")

Configuration and Settings
-------------------------

Using Environment Variables
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a `.env` file in your project root:

.. code-block:: bash

   # .env
   EASYSERIES_TIMEOUT=60.0
   EASYSERIES_MAX_RETRIES=5
   EASYSERIES_BASE_URL=https://api.myservice.com
   EASYSERIES_USER_AGENT=MyApp/1.0.0
   EASYSERIES_ENABLE_METRICS=true

The settings will be automatically loaded:

.. code-block:: python

   from easyseries.core.config import settings

   print(f"Timeout: {settings.timeout}")
   print(f"Base URL: {settings.base_url}")

Custom Configuration
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from easyseries import HTTPClient

   client = HTTPClient(
       base_url="https://api.example.com",
       timeout=30.0,
       max_retries=3,
       headers={
           "Authorization": "Bearer your-token",
           "X-API-Version": "v1"
       }
   )

Error Handling
--------------

.. code-block:: python

   from easyseries.core.exceptions import HTTPClientError, RateLimitError

   async def handle_errors():
       async with HTTPClient() as client:
           try:
               response = await client.get("https://api.example.com/data")
               return response.json()
           except HTTPClientError as e:
               print(f"HTTP error: {e.message}")
               print(f"Details: {e.details}")
           except RateLimitError as e:
               print(f"Rate limit exceeded: {e}")

Using the CLI
-------------

Basic Request
~~~~~~~~~~~~~

.. code-block:: bash

   # Simple GET request
   easyseries request https://httpbin.org/get

   # POST with data
   easyseries request https://httpbin.org/post \
       --method POST \
       --data '{"key": "value"}'

   # Custom headers
   easyseries request https://httpbin.org/headers \
       --headers '{"Authorization": "Bearer token123"}'

Benchmarking
~~~~~~~~~~~~

.. code-block:: bash

   # Basic benchmark
   easyseries benchmark https://httpbin.org/get

   # Custom parameters
   easyseries benchmark https://httpbin.org/get \
       --requests 100 \
       --concurrency 10

Configuration Management
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # View current configuration
   easyseries config

   # Check version
   easyseries version

Advanced Features
----------------

Metrics Collection
~~~~~~~~~~~~~~~~~

.. code-block:: python

   import os
   os.environ["EASYSERIES_ENABLE_METRICS"] = "true"

   async def collect_metrics():
       async with HTTPClient() as client:
           # Make some requests
           await client.get("https://httpbin.org/get")
           await client.post("https://httpbin.org/post", json={"test": True})

           # Get metrics
           metrics = client.get_metrics()
           for metric in metrics:
               print(f"{metric.method} {metric.url}: {metric.duration:.3f}s")

Rate Limiting
~~~~~~~~~~~~

.. code-block:: python

   # Client with rate limiting
   client = HTTPClient(rate_limit=60)  # 60 requests per minute

   # This will automatically enforce rate limits
   async with client:
       for i in range(100):
           try:
               await client.get(f"https://api.example.com/item/{i}")
           except RateLimitError:
               print("Rate limit hit, waiting...")
               await asyncio.sleep(60)

Next Steps
----------

* Read the :doc:`api` documentation for detailed API reference
* Check out the :doc:`modules/index` for specific module documentation
* Look at the GitHub repository for more examples and contributions
