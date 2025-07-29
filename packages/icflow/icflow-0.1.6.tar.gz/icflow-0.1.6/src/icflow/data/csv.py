"""
Base sensor description
"""

import logging
from pathlib import Path

import pandas as pd

from iccore.units import DateRange
from iccore.filesystem import get_csv_files
from iccore.data.schema import Schema
from iccore.data.series import Array, Series


logger = logging.getLogger(__name__)


def gettype(name):

    if name == "str":
        return str
    raise ValueError(name)


def load_dir(
    path: Path, schema: Schema, quantities: list[str], dates: DateRange | None
) -> Series:
    """
    Load the only csv file from the provided directory.

    Return a dict keyed on quantity labels, with values as a tuple of
    the Quantity type and the corresponding pandas dataframe.
    """

    csv_files = get_csv_files(path)
    assert len(csv_files) == 1

    return load(csv_files[0], schema, quantities, dates)


def load(
    path: Path, schema: Schema, quantities: list[str], dates: DateRange | None
) -> Series:
    """
    Load the requested quantities from the provided path.

    Return a dict keyed on quantity labels, with values as a tuple of
    the Quantity type and the corresponding pandas dataframe.
    """

    logger.info("Loading data from %s.", path)

    dtypes = {k: gettype(v) for k, v in schema.type_specs.items()}

    # dates are in column =dataset.time_column in datestring format, automatically
    # parse them and use them as an index
    data = pd.read_csv(path, parse_dates=True, index_col=schema.x.column, dtype=dtypes)

    array_schemas = [v for v in schema.values if v.quantity.name in quantities]

    values = []
    for s in array_schemas:
        values.append(Array(quantity=s.quantity, data=data[s.get_name()]))

    return Series(
        values=values, x=Array(quantity=schema.x.quantity, data=data.index.values)
    )
