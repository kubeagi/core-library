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

from kubeagi_core.kube.client import ConfigMap


class Config:
    """Operate Kubernetes config"""

    def __init__(self, namespace, name, kubeconfig_path):
        config_map = ConfigMap(kubeconfig_path=kubeconfig_path)
        self._config = config_map.read_namespaced_config_map(
            name=name, namespace=namespace
        )
        self._config = self._config.data.get("config")

    def get_config(self):
        """get config info."""
        return self._config
