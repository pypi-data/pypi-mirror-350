from pathlib import Path
import logging
import gzip

import numpy as np
from netCDF4 import Dataset

from iccore.units import to_timestamps
from iccore.data import Schema, Series, Array, insert_series

logger = logging.getLogger(__name__)

_TIME_REF = "2001-01-01T00:00:00Z"


# TODO - fix arg types in iccore and use those interfaces instead


def is_file_with_extensions(
    f, extensions: tuple[str, ...], excludes: list[str] | None = None
):
    """
    True if the path item is a file and has one of the provided extensions
    """

    if not f.is_file():
        return False
    for ext in extensions:
        check_str = str(f).lower()
        if check_str.endswith(f".{ext.lower()}"):
            if excludes:
                for exclude in excludes:
                    if check_str.endswith(f"{exclude.lower()}.{ext.lower()}"):
                        return False
            return True
    return False


def get_files_recursive(
    path: Path, extensions: tuple[str, ...], excludes: list[str] | None = None
):
    """
    Get all provided files recursively, filter on extensions and excludes
    """
    return [
        f for f in path.rglob("*") if is_file_with_extensions(f, extensions, excludes)
    ]


def _load_nc(nc, schema, quantities) -> Series:

    x = Array(
        quantity=schema.x.quantity,
        data=np.array(
            to_timestamps(nc.variables[schema.x.quantity.name][:], _TIME_REF)
        ),
    )

    if schema.y:
        y = Array(
            quantity=schema.y.quantity, data=nc.variables[schema.y.quantity.name][:]
        )
    else:
        y = None

    return Series(
        x=x,
        y=y,
        values=[
            Array(quantity=schema.get_quantity(q), data=nc.variables[q][:])
            for q in quantities
        ],
    )


def load_single(
    path: Path, schema: Schema, quantities: list[str], load_func
) -> Series | None:

    logger.info("Reading data from %s", path)

    if str(path).endswith(".gz"):
        with gzip.open(path) as gz:
            with Dataset("dummy", mode="r", memory=gz.read()) as nc:
                if schema.group_prefix:
                    for name, group in nc.groups.items():
                        if name.startswith(schema.group_prefix):
                            return load_func(group, schema, quantities)
                    raise RuntimeError("No group found in netcdf archive")
                return load_func(nc, schema, quantities)

    else:
        with Dataset(path, mode="r") as nc:
            if schema.group_prefix:
                for name, group in nc.groups.items():
                    if name.startswith(schema.group_prefix):
                        return load_func(group, schema, quantities)
                raise RuntimeError("No group found in netcdf archive")
            return load_func(nc, schema, quantities)


def load(
    path: Path,
    schema: Schema,
    quantities: list[str],
    load_func=_load_nc,
    excludes: list[str] | None = None,
) -> Series | None:

    prefix = f"{schema.name}." if schema.name != "default" else ""
    schema_files = get_files_recursive(
        path, (f"{prefix}nc", f"{prefix}nc.gz"), excludes=excludes
    )

    if not schema_files:
        raise RuntimeError("No valid netcdf files found")

    working: Series | None = None
    for path in schema_files:
        try:
            next_set = load_single(path, schema, quantities, load_func)
        except Exception:
            logger.error("Failed to load netcdf series for: %s", path)
            continue

        if not working:
            working = next_set
        elif next_set:
            working = insert_series(working, next_set)

    return working
