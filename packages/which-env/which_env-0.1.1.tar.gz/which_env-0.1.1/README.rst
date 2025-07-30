
.. image:: https://readthedocs.org/projects/which-env/badge/?version=latest
    :target: https://which-env.readthedocs.io/en/latest/
    :alt: Documentation Status

.. image:: https://github.com/MacHu-GWU/which_env-project/actions/workflows/main.yml/badge.svg
    :target: https://github.com/MacHu-GWU/which_env-project/actions?query=workflow:CI

.. image:: https://codecov.io/gh/MacHu-GWU/which_env-project/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/MacHu-GWU/which_env-project

.. image:: https://img.shields.io/pypi/v/which-env.svg
    :target: https://pypi.python.org/pypi/which-env

.. image:: https://img.shields.io/pypi/l/which-env.svg
    :target: https://pypi.python.org/pypi/which-env

.. image:: https://img.shields.io/pypi/pyversions/which-env.svg
    :target: https://pypi.python.org/pypi/which-env

.. image:: https://img.shields.io/badge/✍️_Release_History!--None.svg?style=social&logo=github
    :target: https://github.com/MacHu-GWU/which_env-project/blob/main/release-history.rst

.. image:: https://img.shields.io/badge/⭐_Star_me_on_GitHub!--None.svg?style=social&logo=github
    :target: https://github.com/MacHu-GWU/which_env-project

------

.. image:: https://img.shields.io/badge/Link-API-blue.svg
    :target: https://which-env.readthedocs.io/en/latest/py-modindex.html

.. image:: https://img.shields.io/badge/Link-Install-blue.svg
    :target: `install`_

.. image:: https://img.shields.io/badge/Link-GitHub-blue.svg
    :target: https://github.com/MacHu-GWU/which_env-project

.. image:: https://img.shields.io/badge/Link-Submit_Issue-blue.svg
    :target: https://github.com/MacHu-GWU/which_env-project/issues

.. image:: https://img.shields.io/badge/Link-Request_Feature-blue.svg
    :target: https://github.com/MacHu-GWU/which_env-project/issues

.. image:: https://img.shields.io/badge/Link-Download-blue.svg
    :target: https://pypi.org/pypi/which-env#files


Welcome to ``which_env`` Documentation
==============================================================================
.. image:: https://which-env.readthedocs.io/en/latest/_static/which_env-logo.png
    :target: https://which-env.readthedocs.io/en/latest/

Managing multiple deployment environments (dev, staging, production) is essential for safe software delivery, but manually specifying environments leads to configuration errors and inconsistent deployments. ``which_env`` solves this by providing intelligent environment detection that adapts to your runtime context - defaulting to development locally while automatically detecting the correct environment in CI/CD pipelines and production deployments.

The library uses a simple inheritance pattern where you define your project's environments once, then rely on smart detection logic that prioritizes user overrides while maintaining safety through validation. This eliminates environment misconfiguration bugs and streamlines deployment workflows across local development, automated testing, and production systems.


.. _install:

Install
------------------------------------------------------------------------------

``which_env`` is released on PyPI, so all you need is to:

.. code-block:: console

    $ pip install which-env

To upgrade to latest version:

.. code-block:: console

    $ pip install --upgrade which-env
