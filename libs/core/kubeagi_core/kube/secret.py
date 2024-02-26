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

from kubeagi_core.kube.client import KubeEnv

logger = logging.getLogger(__name__)


class Secret:
    """Operate Kubernetes resources secret"""

    def __init__(self, namespace, name, kubeconfig_path):
        self._namespace = namespace
        self._name = name
        self._kube = KubeEnv(kubeconfig_path=kubeconfig_path)

    def get_secret_info(self):
        """get secret info by name and namespace.

        name: model name;
        namespace: namespace;
        """
        try:
            return self._kube.get_secret_info(
                namespace=self._namespace, name=self._name
            )
        except Exception as ex:
            logger.error(str(ex))
            return None
