# Copyright 2024 KubeAGI.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import logging
import traceback

from kubeagi_core.kube.custom_resources import (
    arcadia_resource_datasources,
    arcadia_resource_embedding,
    arcadia_resource_models,
    arcadia_resource_versioneddatasets,
)
from kubernetes import config
from kubernetes.client import CoreV1Api, CustomObjectsApi

logger = logging.getLogger(__name__)


class KubeEnv:
    def __init__(self, kubeconfig_path):
        if kubeconfig_path:
            config.load_kube_config(kubeconfig_path)
            logger.debug(f"Load kubeconfig from {kubeconfig_path}")
        else:
            try:
                logger.debug("Try to loading kubeconfig from in cluster config")
                config.load_incluster_config()
            except config.ConfigException:
                logger.error(
                    f"There is an error ",
                    f"when load kubeconfig from in cluster config.\n {traceback.format_exc()}",
                )
                raise RuntimeError(
                    "".join(
                        [
                            "Failed to load incluster config. ",
                            "Make sure the code is running inside a Kubernetes cluster.",
                        ]
                    )
                )

    def patch_versioneddatasets_status(self, namespace: str, name: str, status: any):
        CustomObjectsApi().patch_namespaced_custom_object_status(
            arcadia_resource_versioneddatasets.get_group(),
            arcadia_resource_versioneddatasets.get_version(),
            namespace,
            arcadia_resource_versioneddatasets.get_name(),
            name,
            status,
        )

    def get_versioneddatasets_status(self, namespace: str, name: str):
        return CustomObjectsApi().get_namespaced_custom_object_status(
            arcadia_resource_versioneddatasets.get_group(),
            arcadia_resource_versioneddatasets.get_version(),
            namespace,
            arcadia_resource_versioneddatasets.get_name(),
            name,
        )

    def get_versionedmodels_status(self, namespace: str, name: str):
        return CustomObjectsApi().get_namespaced_custom_object_status(
            arcadia_resource_models.get_group(),
            arcadia_resource_models.get_version(),
            namespace,
            arcadia_resource_models.get_name(),
            name,
        )

    def read_namespaced_config_map(self, namespace: str, name: str):
        return CoreV1Api().read_namespaced_config_map(namespace=namespace, name=name)

    def get_secret_info(self, namespace: str, name: str):
        """Get the secret info."""
        data = CoreV1Api().read_namespaced_secret(namespace=namespace, name=name)
        return data.data

    def get_datasource_object(self, namespace: str, name: str):
        """Get the Datasource object."""
        return CustomObjectsApi().get_namespaced_custom_object(
            group=arcadia_resource_models.get_group(),
            version=arcadia_resource_models.get_version(),
            namespace=namespace,
            plural=arcadia_resource_datasources.get_name(),
            name=name,
        )

    def get_versionedembedding_status(self, namespace: str, name: str):
        return CustomObjectsApi().get_namespaced_custom_object_status(
            arcadia_resource_embedding.get_group(),
            arcadia_resource_embedding.get_version(),
            namespace,
            arcadia_resource_embedding.get_name(),
            name,
        )
