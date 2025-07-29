"""
Module to run a workflow
"""

from pathlib import Path
import logging

from iccore.data import Schema, Series, Array, convert
from iccore.data.units import Unit, DateRange
from iccore.data.source import Source
from iccore.data.quantity import Quantity, sync

from icplot.graph import plot_quantity

from icflow.data import csv, netcdf

from .workflow import Workflow, get_output_config


logger = logging.getLogger(__name__)


def _extract(
    cache: Path,
    source: Source,
    schema: Schema,
    quantities: list[str],
    dates: list[DateRange],
    netcdf_handlers: dict | None = None,
) -> Series | None:
    """
    Extract the requested data from the cache using the provided sensor and
    data schema.
    """

    source_cache = cache / source.name

    logger.info(
        "Loading data for source '%s' with schema '%s'", source.name, schema.name
    )

    if schema.format == "csv":
        return csv.load_dir(source_cache, schema, quantities, dates[0])

    if schema.format == "netcdf":
        if netcdf_handlers and source.name in netcdf_handlers:
            return netcdf.load(
                source_cache,
                schema,
                quantities,
                netcdf_handlers[source.name],
                excludes=schema.path_excludes,
            )
        return netcdf.load(
            source_cache, schema, quantities, excludes=schema.path_excludes
        )

    raise RuntimeError(f"Data requested in unsupported format: {schema.format}")


def _transform(series: Series, outputs: list[Quantity], units: list[Unit]) -> Series:

    if series.is_compound:
        return Series(
            name=series.name,
            components=[_transform(s, outputs, units) for s in series.components],
        )

    output_lookup = {o.name: o for o in outputs}

    values = []
    for array in series.values:
        if array.quantity.name in output_lookup:

            output = output_lookup[array.quantity.name]
            updated_array = convert(
                Array(quantity=sync(array.quantity, output), data=array.data),
                output.unit.name,
                units,
            )

            values.append(updated_array)

    y = series.y
    if series.y is not None:
        y = convert(series.y, "", units)

    return Series(
        name=series.name, x=series.x, y=y, values=values, components=series.components
    )


def _process(
    cache: Path, sources: list[Source], units: list[Unit], outputs: dict
) -> dict:
    """
    Loop through each sensor and dataset and load in the required quantities
    from each, returning time or time-height series.
    """

    ret: dict = {}
    for sensor_name, values in outputs.items():
        sensor = values["sensor"]

        ret[sensor_name] = {}

        for schema_name, quantities in values["schemas"].items():
            series = _extract(
                cache,
                sensor,
                sensor.get_schema(schema_name),
                [q.name for q in quantities],
                [q.dates for q in quantities],
            )
            if series:
                ret[sensor_name][schema_name] = _transform(series, quantities, units)

    return ret


def run(
    cache: Path,
    output: Path,
    sources: list[Source],
    units: list[Unit],
    workflow: Workflow,
):

    logger.info("Launching workflow: %s", workflow.name)

    output_config = get_output_config(workflow, sources)

    logger.info("Start processing data")

    data = _process(cache, sources, units, output_config)

    logger.info("Finished processing data")

    logger.info("Generating plots")
    for plot_config in workflow.plots:
        if not plot_config.active:
            continue

        for q in plot_config.quantities:
            logger.info("Plotting %s:%s:%s", q.sensor, q.schema_name, q.name)
            plot_quantity(output, plot_config, data[q.sensor][q.schema_name], q)
    logger.info("Finished generating plots")
