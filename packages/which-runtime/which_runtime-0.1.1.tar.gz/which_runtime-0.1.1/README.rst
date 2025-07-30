
.. image:: https://readthedocs.org/projects/which-runtime/badge/?version=latest
    :target: https://which-runtime.readthedocs.io/en/latest/
    :alt: Documentation Status

.. image:: https://github.com/MacHu-GWU/which_runtime-project/actions/workflows/main.yml/badge.svg
    :target: https://github.com/MacHu-GWU/which_runtime-project/actions?query=workflow:CI

.. image:: https://codecov.io/gh/MacHu-GWU/which_runtime-project/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/MacHu-GWU/which_runtime-project

.. image:: https://img.shields.io/pypi/v/which-runtime.svg
    :target: https://pypi.python.org/pypi/which-runtime

.. image:: https://img.shields.io/pypi/l/which-runtime.svg
    :target: https://pypi.python.org/pypi/which-runtime

.. image:: https://img.shields.io/pypi/pyversions/which-runtime.svg
    :target: https://pypi.python.org/pypi/which-runtime

.. image:: https://img.shields.io/badge/✍️_Release_History!--None.svg?style=social&logo=github
    :target: https://github.com/MacHu-GWU/which_runtime-project/blob/main/release-history.rst

.. image:: https://img.shields.io/badge/⭐_Star_me_on_GitHub!--None.svg?style=social&logo=github
    :target: https://github.com/MacHu-GWU/which_runtime-project

------

.. image:: https://img.shields.io/badge/Link-API-blue.svg
    :target: https://which-runtime.readthedocs.io/en/latest/py-modindex.html

.. image:: https://img.shields.io/badge/Link-Install-blue.svg
    :target: `install`_

.. image:: https://img.shields.io/badge/Link-GitHub-blue.svg
    :target: https://github.com/MacHu-GWU/which_runtime-project

.. image:: https://img.shields.io/badge/Link-Submit_Issue-blue.svg
    :target: https://github.com/MacHu-GWU/which_runtime-project/issues

.. image:: https://img.shields.io/badge/Link-Request_Feature-blue.svg
    :target: https://github.com/MacHu-GWU/which_runtime-project/issues

.. image:: https://img.shields.io/badge/Link-Download-blue.svg
    :target: https://pypi.org/pypi/which-runtime#files


Welcome to ``which_runtime`` Documentation
==============================================================================
.. image:: https://which-runtime.readthedocs.io/en/latest/_static/which_runtime-logo.png
    :target: https://which-runtime.readthedocs.io/en/latest/

In modern software development, especially in cloud and DevOps environments, the same codebase often runs across multiple runtime environments. The ``which_runtime`` library provides a powerful, centralized solution for detecting and managing different computational contexts.


What is a Runtime?
------------------------------------------------------------------------------
A runtime is a specific computational environment where your code executes. This could be:

- Local development machine
- Cloud environments (AWS Lambda, EC2, Batch)
- Continuous Integration (CI) platforms (GitHub Actions, CodeBuild)
- Development environments (Cloud9)
- Containerized environments


Why Runtime Detection Matters
------------------------------------------------------------------------------
Different runtimes often require different configurations and behaviors:

- Authentication methods vary (local AWS CLI profiles vs. IAM roles)
- Resource access differs between environments
- Logging and monitoring approaches change
- Environment-specific optimizations


Key Features
------------------------------------------------------------------------------
- Detect runtime environment with simple boolean checks
- Support for multiple runtime types (local, cloud, CI)
- Lightweight and easy to integrate
- Helps create adaptive, environment-aware code


Quick Example
------------------------------------------------------------------------------
.. code-block:: python

    from which_runtime.api import runtime

    if runtime.is_aws_lambda:
        # Lambda-specific configuration
        use_lambda_credentials()
    elif runtime.is_local:
        # Local development setup
        use_local_aws_profile()


.. _install:

Install
------------------------------------------------------------------------------

``which_runtime`` is released on PyPI, so all you need is to:

.. code-block:: console

    $ pip install which-runtime

To upgrade to latest version:

.. code-block:: console

    $ pip install --upgrade which-runtime
