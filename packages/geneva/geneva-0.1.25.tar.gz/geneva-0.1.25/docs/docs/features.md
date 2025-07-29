# Feature Engineering

Geneva improves the productivity of AI engineers by streamlining feature engineering tasks.  It is designed to reduce the time required to prototype, perform experiments, scale up, and move to production.

Geneva uses Python User Defined Functions (**UDFs**) to define features as columns in a Lance dataset.  Adding a feature is straightforward:

1. Prototype your Python function in your favorite environment.
2. Wrap the function with small UDF decorator.
3. Register the UDF as a virtual column using `Table.add_columns()`.
4. Trigger a backfill operation.

## Prototyping your Python function

Build your Python feature generator function in an IDE or notebook using your project's Python versions and dependencies.

*That's it.*

Geneva will automate much of the dependency and version management needed to move from prototype to scale and production.


## Converting functions into UDFs

Converting your Python code to a Geneva UDF is simple.  There are three kinds of UDFs that you can provide — scalar UDFs, batched UDFs and stateful UDFs.

In all cases, Geneva uses Python type hints from your functions to infer the input and output
[arrow data types](https://arrow.apache.org/docs/python/api/datatypes.html) that LanceDB uses.

### Scalar UDFs

The **simplest** form is a scalar UDF, which processes one row at a time:

```python
from geneva import udf

@udf
def area_udf(x: int, y: int) -> int:
    return x * y

@udf
def download_udf(filename:str) -> bytes:
    import requests
    resp = requests.get(filename)
    res.raise_for_status()
    return resp.content

```

This UDF will take the value of x and value of y from each row and return the product.  The `@udf` wrapper is all that is needed.

### Batched UDFs

For **better performance**, you can also define batch UDFs that process multiple rows at once.

You can use `pyarrow.Array`s:

```python
import pyarrow as pa
from geneva import udf

@udf(data_type=pa.int32())
def batch_filename_len(filename: pa.Array) -> pa.Array:
    lengths = [len(str(f)) for f in filename]
    return pa.array(lengths, type=pa.int32())
```

Or take entire rows using `pyarrow.RecordBatch`:

```python
import pyarrow as pa
from geneva import udf

@udf(data_type=pa.int32())
def recordbatch_filename_len(batch: pa.RecordBatch) -> pa.Array:
    filenames = batch["filename"] 
    lengths = [len(str(f)) for f in filenames]
    return pa.array(lengths, type=pa.int32())
```

!!! note

    Batch UDFS require you to specify `data_type` in the ``@udf`` decorator for batched UDFs,
    which defines `pyarrow.DataType` of the returned `pyarrow.Array`.


### Stateful UDFs

You can also define a **stateful** UDF that retains its state across calls.

This can be used to share code and **parameterize your UDFs**.  In the example below, the model being used is a parameter that can be specified at UDF registration time.  It can also be used to paramterize input column names of `pa.RecordBatch` batch UDFS.

This also can be used to **optimize expensive initialization** that may require heavy resource on the distributed workers.  For example, this can be used to load an model to the GPU once for all records sent to a worker instead of once per record or per batch of records.

A stateful UDF is a `Callable` class, with `__call__()` method.  The call method can be a scalar function or a batched function.

```python
from typing import Callable
from openai import OpenAI

@udf(data_type=pa.list_(pa.float32(), 1536))
class OpenAIEmbedding(Callable):
    def __init__(self, model: str = "text-embedding-3-small"):
        self.model = model
        # Per-worker openai client
        self.client: OpenAI | None = None

    def __call__(self, text: str) -> pa.Array:
        if self.client is None:
            self.client = OpenAI()

        resp = self.client.embeddings.create(model=self.model, input=text)
        return pa.array(resp.data[0].embeddings)
```

!!! note

    The state is will be independently managed on each distributed Worker.


## Registering Features with UDFs

Registering a feature is done by providing the `Table.add_columns()` function a new column name and the Geneva UDF.

Let's start by obtaining the table `tbl`
```python
import geneva
import numpy as np
import pyarrow as pa

lancedb_uri="gs://bucket/db"
db = geneva.connect(lancedb_uri)

# Define schema for the video table
schema = pa.schema([
    ("filename", pa.string()),
    ("duration_sec", pa.float32()),
    ("x", pa.int32()),
    ("y", pa.int32()),
])
tbl = db.create_table("videos", schema=schema, mode="overwrite")

# Generate fake data
N = 10
data = {
    "filename": [f"video_{i}.mp4" for i in range(N)],
    "duration_sec": np.random.uniform(10, 300, size=N).astype(np.float32),
    "x": np.random.choice([640, 1280, 1920], size=N),
    "y": np.random.choice([360, 720, 1080], size=N),
    "caption": [f"this is video {i}" for i in range(N)]
}

# Convert to Arrow Table and add to LanceDB
batch = pa.table(data, schema=schema)
tbl.add(batch)
```

Here's how to register a simple UDF:
```python
@udf
def area_udf(x: int, y: int) -> int:
    return x * y

@udf
def download_udf(filename: str) -> bytes:
    ...

# {'new column name': <udf>, ...}
# simple_udf's arguments are `x` and `y` so the input columns are
# inferred to be columns `x` amd `y`
tbl.add_columns({"area": area_udf, "content": download_udf })
```

Batched UDFs require return type in their `udf` annotations

```python
@udf(data_type=pa.int32())
def batch_filename_len(filename: pa.Array) -> pa.Array:
    ...

# {'new column name': <udf>}
# batch_filename_len's input, `filename` input column is
# specified by the UDF's argument name.
tbl.add_columns({"filename_len": batch_filename_len})
```

or

```python
@udf(data_type=pa.int32())
def recordbatch_filename_len(batch: pa.RecordBatch) -> pa.Array:
    ...

# {'new column name': <udf>}
# batch_filename_len's input.  pa.RecordBatch typed UDF
# argument pulls in all the column values for each row.
tbl.add_columns({"filename_len": recordbatch_filename_len})
```

Similarly, a stateful UDF is registered by providing an instance of the Callable object.  The call method may be a per-record function or a batch function.
```python
@udf(data_type=pa.list_(pa.float32(), 1536))
class OpenAIEmbedding(Callable):
    ...
    def __call__(self, text: str) -> pa.Array:
        ...

# OpenAIEbmedding's call method input is inferred to be 'text' of
# type string from the __call__'s arguments, and its output type is
# a fixed size list of float32.
tbl.add_columns({"embedding": OpenAIEmbedding()})
```

## Triggering backfill

Triggering backfill creates a distributed job to run the UDF and populate the column values in your LanceDB table. The Geneva framework simplifies several aspects of distributed execution.

* **Environment management**:  Geneva automatically packages and deploys your Python execution environment to worker nodes.  This ensures that distributed execution occurs in the same environment and depedencies as your prototype.
* **Checkpoints**:  Each batch of UDF execution is checkpointed so that partial results are not lost in case of job failures.  Jobs can resume and avoid most of the expense of having to recalculate values.

We currently support one processing backend: [Ray](https://www.anyscale.com/product/open-source/ray).  This is deployed on an existing Ray cluster or on a kubernetes cluster on demand.

!!! Note
    If you are using a remote Ray cluster, you will need to have the notebook or script that code is packaged on running the same CPU architecture / OS.  By default, Ray clusters are run in Linux.   If you host a jupyter service on a Mac, Geneva will attempt to deploy Mac shared libraries to a linux cluster and result in `Module not found` errors.  You can instead host your jupyter or python envrionment on a Linux VM or container.

=== "Ray on Kubernetes"

    Geneva uses KubeRay to deploy Ray on Kubernetes.  You can define a `RayCluster` by specifying the pod name, the Kubernetes namespace, credentials to use for deploying Ray, and characteristics of your workers.

    This approach makes it easy to tailor resource requirements to your particular UDFs.

    You can then wrap your table backfill call with the RayCluster context.

    ```python
    from geneva.runners.ray.raycluster import _HeadGroupSpec, _WorkerGroupSpec
    from geneva.runners._mgr import ray_cluster

    override_config(from_kv({"uploader.upload_dir": images_path + "/zips"}))

    with ray_cluster(
            name=k8s_name,  # prefix of your k8s pod
            namespace=k8s_namespace,
            skip_site_packages=False, # optionally skip shipping python site packages if already in image
            use_portforwarding=True,  # required for kuberay to expose ray ports
            head_group=_HeadGroupSpec(
                service_account="geneva-integ-test", # k8s service account bound geneva runs as
                image="rayproject/ray:latest-py312" # optionally specified custom docker image
                num_cpus=8,
                node_selector={"geneva.lancedb.com/ray-head":""}, # k8s label required for head
            ),
            worker_groups=[
                _WorkerGroupSpec(  # specification per worker for cpu-only nodes
                    name="cpu",
                    num_cpus=60,
                    memory="120G",
                    service_account="geneva-integ-test",
                    image="rayproject/ray:latest-py312"
                    node_selector={"geneva.lancedb.com/ray-worker-cpu":""}, # k8s label for cpu worker
                ),
                _WorkerGroupSpec( # specification per worker for gpu nodes
                    name="gpu",
                    num_cpus=8,
                    memory="32G",
                    num_gpus=1,
                    service_account="geneva-integ-test",
                    image="rayproject/ray:latest-py312-gpu"
                    node_selector={"geneva.lancedb.com/ray-worker-gpu":""}, # k8s label for gpu worker
                ),
            ],
        ):

        tbl.backfill("xy_product")
    ```

    For more interactive usage, you can use this pattern:

    ```python
    # this is a k8s pod spec.
    raycluster = ray_cluster(...)
    raycluster.__enter__() # equivalent of ray.init()

    #  trigger the backfill on column "filename_len" 
    tbl.backfill("filename_len") 

    raycluster.__exit__()
    ```

    Whne you become more confident with your feature, you can trigger the backfill by specifying the `backfill` kwarg on `Table.add_columns()`.

    ```python
    tbl.add_columns({"filename_len": filename_len}, ["prompt"], backfill=True)
    ```

=== "Existing Ray Cluster"

    !!! Warning

        This is a work in progress


=== "Ray Auto Connect"

    To use ray, you can just trigger the `Table.backfill` method or the `Table.add_columns(..., backfill=True)` method.   This will autocreate a local Ray cluster and is only suitable prototyping on small datasets.

    ```python
    tbl.backfill("area")
    ```

    ```python
    # add column 'filename_len' and trigger the job
    tbl.backfill("filename_len")  # trigger the job
    ```

    Whne you become more confident with your feature, you can trigger the backfill by specifying the `backfill` kwarg on `Table.add_columns()`.

    ```python
    tbl.add_column({"filename_len": filename_len}, ["prompt"], backfill=True)
    ```



## Filtered Backfills

Geneva allows you to specify filters on the backfill operation.  This lets you to apply backfills to a specified subset of the table's rows.

```python
    # only backfill video content whose filenames start with 'a'
    tbl.backfill("content", where="starts_with(filename, 'a')")
    # only backfill embeddings of only those videos with content
    tbl.backfill("embedding", where="content is not null")
```

Geneva also allows you to incrementally add more rows or have jobs that just update rows that were previously skipped.

If new rows are added, we can run the same command and the new rows that meet the criteria will be updated.

```python
    # only backfill video content whose filenames start with 'a'
    tbl.backfill("content", where="starts_with(filename, 'a')")
    # only backfill embeddings of only those videos with content
    tbl.backfill("embedding", where="content is not null")
```

Or, you can use filters to add in or overwrite content in rows previously backfilled.

```python
    # only backfill video content whose filenames start with 'a' or 'b' but only if content not pulled previously
    tbl.backfill("content", where="(starts_with(filename, 'a') or starts_with(filename, 'b')) and content is null")
    # only backfill embeddings of only those videos with content and no prevoius embeddings
    tbl.backfill("embedding", where="content is not null and embeddding is not null")
```

## APIs

### UDF API
All UDFs are decorated by ``@geneva.udf``.

::: geneva.udf
    options:
      annotations_path: brief
      show_source: false

### Backfill API

::: geneva.table.Table.backfill
    options:
      annotations_path: brief
      show_source: false