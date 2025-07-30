.. _json:

JSON
====

The JSON mode allows you to use high-level visualization functions to easily and quickly create figures.

What you can do
---------------

You can generate the following types of figures by specifying the ``figure`` key in your JSON file:

.. currentmodule:: canopy.visualization

+----------------+----------------------------------------------+-------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------+
| "figure" key   | Function reference                           | JSON example file                                                                                                       | Remark                                               |
+================+==============================================+=========================================================================================================================+======================================================+
| map_simple     | :func:`map.make_simple_map`                  | `simple_map.json <https://codebase.helmholtz.cloud/canopy/canopy/-/blob/main/json_examples/simple_map.json>`_           | Can concatenate up to two fields (see example below) |
+----------------+----------------------------------------------+-------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------+
| map_diff       | :func:`map.make_diff_map`                    | `diff_map.json <https://codebase.helmholtz.cloud/canopy/canopy/-/blob/main/json_examples/diff_map.json>`_               | Compute the difference between two fields            |
+----------------+----------------------------------------------+-------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------+
| time_series    | :func:`time_series.make_time_series`         | `time_series.json <https://codebase.helmholtz.cloud/canopy/canopy/-/blob/main/json_examples/time_series.json>`_         |                                                      |
+----------------+----------------------------------------------+-------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------+
| static         | :func:`static_plot.make_static_plot`         | `static_plot.json <https://codebase.helmholtz.cloud/canopy/canopy/-/blob/main/json_examples/static_plot.json>`_         |                                                      |
+----------------+----------------------------------------------+-------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------+
| comparison     | :func:`comparison_plot.make_comparison_plot` | `comparison_plot.json <https://codebase.helmholtz.cloud/canopy/canopy/-/blob/main/json_examples/comparison_plot.json>`_ |                                                      |
+----------------+----------------------------------------------+-------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------+

For a complete list of available arguments, refer to the documentation for each function, and consult the corresponding JSON example file for practical usage.

.. currentmodule:: canopy.visualization.map

With ``"figure": "map_simple"``, you can concatenate two fields and visualize them in a single map. For example:

.. code-block:: python

    {
        "figure": "map_simple",
        "input_file": ["example_data/hist/anpp.out.gz","example_data/ssp1A/anpp.out.gz"],
        ...
    }

.. currentmodule:: canopy.core.field

**Other features**

- **Slice reduction:** You can reduce data along ``time``, ``lat``, or ``lon`` dimensions using the ``time_slice``, ``lat_slice``, or ``lon_slice`` keys.
- **Drop layers:** Remove unwanted layers from your data using the ``drop_layers`` key (accept a list).
- **Transform layers:** Apply transformations to layers using the ``red_layers`` key and the :meth:`Field.red_layers` function (accept a dictionnary, see `stacked_time_series.json <https://codebase.helmholtz.cloud/canopy/canopy/-/blob/main/json_examples/stacked_time_series.json>`_ for an example).

What you cannot do
------------------

.. currentmodule:: canopy.visualization.plot_functions

- **Metadata not retrieved:** Metadata from your run is not automatically retrieved. You must explicitly define variable names and units in your JSON file.
- **No multiple time-series:** The current JSON mode does not support the use of multiple time series in a single plot.
- **No multiple figures function:** You cannot use the :func:`multiple_figs` function.
- **No function keyword arguments as JSON keys:** You cannot specify function keyword arguments (``kwargs``) directly as JSON keys.
- **Cannot change units:** Changing units within the JSON configuration is not supported.
- **Cannot filter data:** Filtering the data within the JSON configuration is not supported.
