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
from kubeagi_core.kube.client import ConfigMap, Secret, KubeEnv

logger = logging.getLogger(__name__)


class Config:
    """Operate Kubernetes config"""

    def __init__(self, namespace, name, kubeconfig_path):
        self._namespace = namespace
        self._name = name
        self._config = ConfigMap(kubeconfig_path=kubeconfig_path)
        self._kubeEnv = KubeEnv(kubeconfig_path=kubeconfig_path)
        self._secret = Secret(kubeconfig_path=kubeconfig_path)

    def get_system_datasource(self):
        """Get the system datasource info in the configmap.

        namespace: namespace;
        name: config map name
        """
        try:
            config_map = self._config.read_namespaced_config_map(
                namespace=self._namespace, name=self._name
            )

            config = config_map.data.get("config")

            json_data = yaml.safe_load(config)

            datasource = json_data["systemDatasource"]
            minio_cr_object = self._kubeEnv.get_datasource_object(
                namespace=datasource["namespace"], name=datasource["name"]
            )

            minio_api_url = minio_cr_object["spec"]["endpoint"]["url"]

            minio_secure = True
            insecure = minio_cr_object["spec"]["endpoint"].get("insecure")
            if insecure is None:
                minio_secure = True
            elif str(insecure).lower() == "true":
                minio_secure = False

            secret_info = self._secret.read_namespaced_secret(
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

    def get_gateway(self):
        """get base url for configmap.

        name: model name;
        namespace: namespace;
        """
        try:
            config_map = self._config.read_namespaced_config_map(
                name=self._name, namespace=self._namespace
            )

            config = config_map.data.get("config")

            json_data = yaml.safe_load(config)

            return json_data.get("gateway")
        except Exception as ex:
            logger.error(str(ex))
            return None

    def get_dataprocess(self):
        """Get the llm QA retry count in the configmap.

        namespace: namespace;
        name: config map name
        """
        try:
            config_map = self._config.read_namespaced_config_map(
                namespace=self._namespace, name=self._name
            )

            config = config_map.data.get("dataprocess")

            json_data = yaml.safe_load(config)

            return json_data
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

    def get_secret(self):
        """get secret info by name and namespace.

        name: model name;
        namespace: namespace;
        """
        try:
            return self._secret.read_namespaced_secret(
                namespace=self._namespace, name=self._name
            )
        except Exception as ex:
            logger.error(str(ex))
            return None
