sphinx-pushfeedback
===================

Feedback widget for Sphinx documentation sites.

Installation
------------

#. Create a `PushFeedback account <http://pushfeedback.com/>`_.

#. Install ``sphinx-pushfeedback`` using PIP.

   .. code-block:: bash

      pip install sphinx-pushfeedback

#. Add the extension to your Sphinx project ``conf.py`` file.

   .. code-block:: python

      extensions = ['sphinx_pushfeedback']

#. Configure your project ID in the ``conf.py`` file:

   .. code-block:: python

     pushfeedback_project = '<YOUR_PROJECT_ID>'

   Replace ``<YOUR_PROJECT_ID>`` with your project's ID from the `PushFeedback dashboard <https://docs.pushfeedback.com/#2-create-a-project>`_.

#. Build the documentation:

   .. code-block:: bash

      make html

   Once built, open your documentation in a web browser. Verify that the feedback button appears and works correctly on your site.

For advanced configuration options, see `Sphinx PushFeedback documentation <https://docs.pushfeedback.com/installation/sphinx>`_.

License
-------

Copyright (c) 2023 PushFeedback.com
Licensed under the `MIT License <https://github.com/dgarcia360/sphinx-pushfeedback/blob/main/LICENSE.md>`_.
