import uuid

import pyarrow as pa

import geneva
from geneva.runners.ray.raycluster import RayCluster


# use a random version to force checkpoint to invalidate
@geneva.udf(num_cpus=1, version=uuid.uuid4().hex)
def plus_one(a: int) -> int:
    return a + 1


SIZE = 1024


def test_ray_add_column_pipeline(
    geneva_test_bucket: str,
    standard_cluster: RayCluster,
) -> None:
    conn = geneva.connect(geneva_test_bucket)
    table_name = uuid.uuid4().hex
    table = conn.create_table(
        table_name,
        pa.Table.from_pydict({"a": pa.array(range(SIZE))}),
    )
    with standard_cluster:
        table.add_columns(
            {"b": plus_one},
            backfill=True,
            batch_size=32,
            concurrency=2,
            intra_applier_concurrency=2,
        )

    assert table.to_arrow() == pa.Table.from_pydict(
        {"a": pa.array(range(SIZE)), "b": pa.array(range(1, SIZE + 1))}
    )
    conn.drop_table(table_name)


def test_ray_add_column_pipeline_cpu_only_pool(
    geneva_test_bucket: str,
    standard_cluster: RayCluster,
) -> None:
    conn = geneva.connect(geneva_test_bucket)
    table_name = uuid.uuid4().hex
    table = conn.create_table(
        table_name,
        pa.Table.from_pydict({"a": pa.array(range(SIZE))}),
    )
    with standard_cluster:
        table.add_columns(
            {"b": plus_one},
            backfill=True,
            batch_size=32,
            concurrency=4,
            use_cpu_only_pool=True,
        )

    assert table.to_arrow() == pa.Table.from_pydict(
        {"a": pa.array(range(SIZE)), "b": pa.array(range(1, SIZE + 1))}
    )
    conn.drop_table(table_name)
