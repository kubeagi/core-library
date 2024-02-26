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

import base64
import logging
import traceback

import yaml
from kubeagi_core.kube.client import KubeEnv

logger = logging.getLogger(__name__)


class ConfigMap:
    """Operate Kubernetes resources configmap"""

    def __init__(self, namespace, name, kubeconfig_path):
        self._namespace = namespace
        self._name = name
        self._kube = KubeEnv(kubeconfig_path=kubeconfig_path)

    def get_minio_config_in_k8s_configmap(self):
        """Get the MinIO config info in the configmap.

        namespace: namespace;
        name: config map name
        """
        try:
            config_map = self._kube.read_namespaced_config_map(
                namespace=self._namespace, name=self._name
            )

            config = config_map.data.get("config")

            json_data = yaml.safe_load(config)

            datasource = json_data["systemDatasource"]

            minio_cr_object = self._kube.get_datasource_object(
                namespace=datasource["namespace"], name=datasource["name"]
            )

            minio_api_url = minio_cr_object["spec"]["endpoint"]["url"]

            minio_secure = True
            insecure = minio_cr_object["spec"]["endpoint"].get("insecure")
            if insecure is None:
                minio_secure = True
            elif str(insecure).lower() == "true":
                minio_secure = False

            secret_info = self._kube.get_secret_info(
                namespace=self._namespace,
                name=minio_cr_object["spec"]["endpoint"]["authSecret"]["name"],
            )

            return {
                "minio_api_url": minio_api_url,
                "minio_secure": minio_secure,
                "minio_access_key": base64.b64decode(secret_info["rootUser"]).decode(
                    "utf-8"
                ),
                "minio_secret_key": base64.b64decode(
                    secret_info["rootPassword"]
                ).decode("utf-8"),
            }
        except Exception:
            logger.error(
                "".join(
                    [
                        f"Can not get the MinIO config info. The error is: \n",
                        f"{traceback.format_exc()}\n",
                    ]
                )
            )

            return None

    def get_worker_base_url_k8s_configmap(self):
        """get base url for configmap.

        name: model name;
        namespace: namespace;
        """
        try:
            config_map = self._kube.read_namespaced_config_map(
                name=self._name, namespace=self._namespace
            )

            config = config_map.data.get("config")

            json_data = yaml.safe_load(config)
            external_api_server = json_data.get("gateway", {}).get("apiServer")

            return external_api_server
        except Exception as ex:
            logger.error(str(ex))
            return None

    def get_llm_qa_retry_count_in_k8s_configmap(self):
        """Get the llm QA retry count in the configmap.

        namespace: namespace;
        name: config map name
        """
        try:
            config_map = self._kube.read_namespaced_config_map(
                namespace=self._namespace, name=self._name
            )

            config = config_map.data.get("dataprocess")

            json_data = yaml.safe_load(config)

            return json_data["llm"]["qa_retry_count"]
        except Exception:
            logger.error(
                "".join(
                    [
                        f"Can not the llm QA retry count. The error is: \n",
                        f"{traceback.format_exc()}\n",
                    ]
                )
            )

            return None

    def get_postgresql_config_in_k8s_configmap(self):
        """Get the PostgreSQL config info in the configmap.

        namespace: namespace;
        name: config map name
        """
        try:
            config_map = self._kube.read_namespaced_config_map(
                namespace=self._namespace, name=self._name
            )

            config = config_map.data.get("dataprocess")

            json_data = yaml.safe_load(config)

            return json_data["postgresql"]
        except Exception:
            logger.error(
                "".join(
                    [
                        f"Can not get the PostgreSQL config info. The error is: \n",
                        f"{traceback.format_exc()}\n",
                    ]
                )
            )

            return None
