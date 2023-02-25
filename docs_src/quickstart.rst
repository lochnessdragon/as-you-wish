Quickstart
==========

Getting started with As You Wish is really easy, no really.
Simply run: ``pip install as-you-wish`` to install.

Then create a file with the following code

.. code-block:: python

  from as-you-wish import Config

  config = Config()
  config.define('server.hostname', '127.0.0.1', 'what should we host the server on')
  config.define('server.port', 8080, 'the port to use for the server')

  config.load('server_settings.ini')

  print(f"Hosting a server on {config.get('server.hostname')}:{config.get('server.port')}")

.. admonition:: Expected output:

  Hosting a server on 127.0.0.1:8080

On the first run, this will create a file that looks like this:::

  [server]
  # what should we host the server on
  hostname = 127.0.0.1
  # the port to use for the server
  port = 8080

You'll also notice that the value of ``'server.hostname'`` is returned as a string and the value of ``'server.port'`` is returned as an integer, so no conversion is required.
