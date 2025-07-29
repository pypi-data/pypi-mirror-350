# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright The Geneva Authors

from pyarrow import DataType


def datafusion_type_name(data_type: DataType) -> str:
    arrow_type_name = str(data_type)
    # see https://datafusion.apache.org/user-guide/sql/data_types.html
    # TODO: add more types. Note that we only support certain types in lance
    # https://github.com/lancedb/lance/blob/644213b9a63e2b143d62cda79e108df831bc5054/rust/lance-datafusion/src/planner.rs#L426-L441
    df_type_name = {
        "int8": "TINYINT",
        "uint8": "TINYINT UNSIGNED",
        "int16": "SMALLINT",
        "uint16": "SMALLINT UNSIGNED",
        "int32": "INT",
        "uint32": "INT UNSIGNED",
        "int64": "BIGINT",
        "uint64": "BIGINT UNSIGNED",
        "float32": "FLOAT",
        "float64": "DOUBLE",
        "string": "STRING",
        "binary": "BINARY",
        "boolean": "BOOLEAN",
    }.get(arrow_type_name)

    if df_type_name is None:
        raise ValueError(f"unsupported arrow type {arrow_type_name}")

    return df_type_name
