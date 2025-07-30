.. _quick_start:

Quick Start
===========

You can use **canopy** in two modes:

- **Interactive mode**, an intuitive and flexible mode, that allows you to load and manipulate data, and generate figures **using python functions**.
- **JSON mode**, a easy-to-use and fast mode, to directly generate figures **using a structured JSON configuration file**.

In the examples below, the same figure is created via each mode.

Interactive mode
----------------

.. currentmodule:: canopy.core.field

In python, use :meth:`Field.from_file` to open your data:

.. code-block:: python

    import canopy as cp

    # Load data using Field.from_file
    anpp = cp.Field.from_file("canopy/tests/test_data/anpp_spain_1990_2010.out.gz")

.. currentmodule:: canopy.visualization.map

and :func:`make_simple_map` to make a map:

.. code-block:: python

    import canopy.visualization as cv

    # Create map
    cv.make_simple_map(field=anpp,
                       layer="Total",
                       output_file="anpp_spain_map.png",
                       title="Actual NPP in Spain (1990-2010)",
                       n_classes=7,
                       classification="jenks",
                       palette="YlGnBu",
                       proj="TransverseMercator",
                       x_fig=10,
                       y_fig=8
                       )

.. image:: _static/anpp_spain_map.png
    :alt: Example map output
    :align: center
    :width: 80%

JSON mode
---------

.. currentmodule:: canopy.json.run_json

In your terminal, use :func:`run_json`:

.. code-block:: bash

    python -c "import canopy as cp; cp.run_json('json_examples/simple_map.json')"

There are different examples available in the `json_examples directory <https://codebase.helmholtz.cloud/canopy/canopy/-/tree/main/json_examples>`_.

We recommend starting with one of these examples and modifying the arguments to customize the figure according to your needs.

.. warning::

    The JSON mode does not support the full range of functionalities offered by **canopy**.

    For instance, metadata from your run will not be automatically retrieved. As a result, you must explicitly define variable names, plot titles, and units in the JSON file.

    Additionally, JSON mode does not currently support the use of multiple time series or the specification of function keyword arguments (`kwargs`) as JSON keys.

    You are restricted to the predefined set of arguments accepted by each visualization function (see :ref:`visualization` for reference).

For more information about how to use JSON files with **canopy**, see the :ref:`JSON documentation <json>`.
