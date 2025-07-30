.. image:: ./images/PyMetric.png
   :width: 300px
   :align: center

PyMetric
===============

|isort| |black| |Pre-Commit| |docformatter| |NUMPSTYLE| |COMMIT| |CONTRIBUTORS| |docs|

.. raw:: html

   <hr style="height:2px;background-color:black">

PyMetric began as the backend for the `Pisces project <https://github.com/Pisces-Project/Pisces>`_ and has grown
into a self-contained package. It provides a seamless interface for performing coordinate-dependent operations in Python—ranging
from coordinate transformations and differential operations to solving equations of motion. In addition, it offers robust
data structures that natively respect and understand underlying coordinate systems and grid architectures, enabling efficient
handling of both curvilinear and structured grids.


.. raw:: html

   <hr style="color:black">

Installation
============

PyMetric is written for Python 3.8+ (with continued support for older versions). For detailed installation instructions
and a quick start guide, please see the :ref:`getting_started` page.

Resources
=========

.. grid:: 2
    :padding: 3
    :gutter: 5

    .. grid-item-card::
        :img-top: images/index/stopwatch_icon.png
        :class-img-top: w-50 m-auto px-1 py-2 dark-light
        :shadow: lg
        :text-align: center

        Getting Started
        ^^^^^^^^^^^^^^^
        New to ``PyMetric``? The getting started guide walks you through installing the library,
        setting up your first coordinate system, and working with fields on structured grids.

        +++

        .. button-ref:: getting_started
            :expand:
            :color: secondary
            :click-parent:

            Go to Getting Started

    .. grid-item-card::
        :img-top: images/index/lightbulb.png
        :class-img-top: w-50 m-auto px-1 py-2 dark-light
        :shadow: lg
        :text-align: center

        Worked Examples
        ^^^^^^^^^^^^^^^
        Explore practical examples that demonstrate how to use ``PyMetric`` to define coordinates,
        manipulate fields, perform differential operations, and more.

        +++

        .. button-ref:: examples
            :expand:
            :color: secondary
            :click-parent:

            Explore Examples

    .. grid-item-card::
        :img-top: images/index/book.svg
        :class-img-top: w-50 m-auto px-1 py-2 dark-light
        :shadow: lg
        :text-align: center

        User Guide
        ^^^^^^^^^^^
        Learn how PyMetric is structured under the hood, including coordinate systems, grids,
        fields, and differential operators. Ideal for in-depth understanding of the core design.

        +++

        .. button-ref:: reference/index
            :expand:
            :color: secondary
            :click-parent:

            View the User Guide

    .. grid-item-card::
        :img-top: images/index/api_icon.png
        :class-img-top: w-50 m-auto px-1 py-2 dark-light
        :shadow: lg
        :text-align: center

        API Reference
        ^^^^^^^^^^^^^
        Need implementation details? The API reference includes docstrings, type hints, and class hierarchies
        for every public-facing component in ``PyMetric``.

        +++

        .. button-ref:: api
            :expand:
            :color: secondary
            :click-parent:

            Open API Reference


Contents
--------

.. raw:: html

   <hr style="height:10px;background-color:black">

.. toctree::
   :maxdepth: 1

   getting_started
   auto_examples/index
   reference/index
   api

- **Getting Started** — A quick guide to installation, basic setup, and your first field.
- **Examples** — Real-world use cases showing how to use PyMetric in practice.
- **User Guide** — In-depth explanations of coordinate systems, grids, and field operations.
- **API Reference** — Full class and function documentation with source code links and type hints.

Indices and Tables
------------------

.. raw:: html

   <hr style="height:10px;background-color:black">

* :ref:`genindex` – General index of all documented terms
* :ref:`modindex` – Python module index
* :ref:`search` – Search the documentation


.. |yt-project| image:: https://img.shields.io/static/v1?label="works%20with"&message="yt"&color="blueviolet"
   :target: https://yt-project.org

.. |docs| image:: https://img.shields.io/badge/docs-latest-brightgreen
   :target: https://eliza-diggins.github.io/Pisces

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000
   :target: https://github.com/psf/black

.. |isort| image:: https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336
   :target: https://pycqa.github.io/isort/

.. |Pre-Commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
   :target: https://github.com/pre-commit/pre-commit
   :alt: pre-commit

.. |CONTRIBUTORS| image:: https://img.shields.io/github/contributors/Pisces-Project/Pisces-Geometry
    :target: https://github.com/eliza-diggins/Pisces/graphs/contributors

.. |COMMIT| image:: https://img.shields.io/github/last-commit/Pisces-Project/Pisces-Geometry

.. |NUMPSTYLE| image:: https://img.shields.io/badge/%20style-numpy-459db9
    :target: https://numpydoc.readthedocs.io/en/latest/format.html

.. |docformatter| image:: https://img.shields.io/badge/%20formatter-docformatter-fedcba
    :target: https://github.com/PyCQA/docformatter
