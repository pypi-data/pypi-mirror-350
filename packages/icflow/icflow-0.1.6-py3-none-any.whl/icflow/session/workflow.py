"""
Module representing a computational workflow
"""

from pathlib import Path
import json

from pydantic import BaseModel

from iccore.data.units import Unit, find_unit
from iccore.data.quantity import Quantity, update_dates
from iccore.data.source import Source, find_source

from icplot.graph import PlotGroup


def load_model(path: Path, model_type):
    with open(path, "r", encoding="utf8") as f:
        data = json.load(f)
    return model_type(**data)


class Workflow(BaseModel, frozen=True):
    """
    A computational or data-processing workflow

    :cvar name: A name or label
    :cvar plots: Description of plots to generate
    """

    name: str
    plots: list[PlotGroup] = []


def _validate_units(workflow: Workflow, units: list[Unit]):
    for plot in workflow.plots:
        for quantity in plot.quantities:
            if quantity.unit and quantity.unit.name:
                try:
                    find_unit(quantity.unit.name, units)
                except Exception as e:
                    raise RuntimeError(
                        f"Unit {quantity.unit.name} in {quantity.name} not found: {e}."
                    ) from e


def load_workflow(path: Path, units: list[Unit]) -> Workflow:
    model = load_model(path, Workflow)

    _validate_units(model, units)
    return model


def get_quantity(name: str, workflow: Workflow) -> Quantity:
    """
    Find a requested output quantity by name in the
    provided workflow.
    """

    for plot in workflow.plots:
        for q in plot.quantities:
            if name == q.name:
                return update_dates(q, plot.start_date, plot.end_date)
    raise RuntimeError(f"Quantity with name {name} not found.")


def get_output_config(workflow: Workflow, sources: list[Source]) -> dict:
    """
    Collect the quantities to be plotted from the workflow file
    ordered by sensor and dataset.
    """

    quantities = [q for p in workflow.plots for q in p.quantities]

    ret: dict = {}
    for q in quantities:

        if q.sensor not in ret:
            ret[q.sensor] = {
                "sensor": find_source(q.sensor, sources),
                "schemas": {},
            }

        if q.schema_name not in ret[q.sensor]["schemas"]:
            ret[q.sensor]["schemas"][q.schema_name] = []

        output_q = get_quantity(q.name, workflow)
        ret[q.sensor]["schemas"][q.schema_name].append(output_q)
    return ret
