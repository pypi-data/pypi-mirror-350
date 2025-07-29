import hashlib
import random

import attrs
from kubernetes import client
from kubernetes import config as kube_config

from geneva.config import ConfigBase

KUBERAY_API_GROUP = "ray.io"
KUBERAY_API_VERSION = "v1"
KUBERAY_API_GROUP_VERSION = f"{KUBERAY_API_GROUP}/{KUBERAY_API_VERSION}"
KUBERAY_JOB_API_KIND = "RayJob"
KUBERAY_JOB_API_NAME = "rayjobs"


@attrs.define
class KuberayConfig(ConfigBase):
    checkpoint_store: str = attrs.field()
    ray_version: str = attrs.field()
    namespace: str = attrs.field(default="lancedb")
    worker_min_replicas: int = attrs.field(default=0)
    worker_max_replicas: int = attrs.field(default=10)

    @classmethod
    def name(cls) -> str:
        return "kuberay"


def launch_kuberay_job(
    db_uri: str,
    table_name: str,
    column: str,
    image: str,
    kuberay_config: KuberayConfig,
) -> None:
    # TODO api docs explaining the args supposed to be passed

    kube_config.load_kube_config()
    api = client.CustomObjectsApi()

    job_definition = {
        "apiVersion": KUBERAY_API_GROUP_VERSION,
        "kind": KUBERAY_JOB_API_KIND,
        "metadata": {
            "name": generate_job_name(db_uri, table_name, column),
            "namespace": kuberay_config.namespace,
        },
        "spec": {
            "entrypoint": f"python3 -m geneva.runners.ray --db_uri {db_uri} --table_name {table_name} --column {column} --checkpoint_store {kuberay_config.checkpoint_store}",  # noqa E501
            "rayClusterSpec": {
                "rayVersion": kuberay_config.namespace,
                "headGroupSpec": {
                    "rayStartParams": {},
                    "template": {
                        "spec": {
                            "containers": [
                                {
                                    "name": "ray-head",
                                    "image": image,
                                    "imagePullPolicy": "IfNotPresent",
                                    "ports": [
                                        {
                                            "containerPort": 10001,
                                            "name": "client",
                                            "protocol": "TCP",
                                        },
                                        {
                                            "containerPort": 8265,
                                            "name": "dashboard",
                                            "protocol": "TCP",
                                        },
                                        {
                                            "containerPort": 6379,
                                            "name": "gsc-server",
                                            "protocol": "TCP",
                                        },
                                    ],
                                }
                            ]
                        }
                    },
                },
                "workerGroupSpecs": [
                    {
                        "groupName": "worker-group-1",
                        "minReplicas": kuberay_config.worker_min_replicas,
                        "maxReplicas": kuberay_config.worker_max_replicas,
                        "rayStartParams": {},
                        "template": {
                            "spec": {
                                "containers": [
                                    {
                                        "name": "ray-worker",
                                        "image": image,
                                        "imagePullPolicy": "IfNotPresent",
                                    }
                                ]
                            }
                        },
                    }
                ],
            },
        },
    }

    api.create_namespaced_custom_object(
        group=KUBERAY_API_GROUP,
        version=KUBERAY_API_VERSION,
        namespace=kuberay_config.namespace,
        plural=KUBERAY_JOB_API_NAME,
        body=job_definition,
    )


def generate_job_name(
    db_uri: str,
    table_name: str,
    column: str,
) -> str:
    db_name = db_uri.split("/")[-1]
    seed = random.randint(0, 1000000)
    job_name = f"ray-geneva-{db_name[:6]}-{table_name[6]}-{column[:6]}-{hashlib.md5(str(seed).encode()).hexdigest()[:6]}"  # noqa E501
    return job_name
