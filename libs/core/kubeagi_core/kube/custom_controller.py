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

import datetime
import logging

import pytz
from kubeagi_core.kube.client import KubeEnv

logger = logging.getLogger(__name__)


class Dataset:
    def __init__(self, namespace, version_data_set_name, kubeconfig_path):
        self._namespace = namespace
        self._version_data_set_name = version_data_set_name
        self._kube = KubeEnv(kubeconfig_path=kubeconfig_path)

    def update_dataset_k8s_cr(self, reason, message):
        """Update the condition info for the dataset.

        message: dataset message;
        reason: the update reason;
        """
        try:
            one_cr_datasets = self._kube.get_versioneddatasets_status(
                self._namespace, self._version_data_set_name
            )

            conditions = one_cr_datasets["status"]["conditions"]
            now_utc_str = datetime.datetime.now(pytz.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

            found_index = None
            for i in range(len(conditions)):
                item = conditions[i]
                if item["type"] == "DataProcessing":
                    found_index = i
                    break

            if found_index is None:
                conditions.append(
                    {
                        "lastTransitionTime": now_utc_str,
                        "reason": reason,
                        "status": "True",
                        "type": "DataProcessing",
                        "message": message,
                    }
                )
            else:
                conditions[found_index] = {
                    "lastTransitionTime": now_utc_str,
                    "reason": reason,
                    "status": "True",
                    "type": "DataProcessing",
                    "message": message,
                }

            self._kube.patch_versioneddatasets_status(
                self._namespace,
                self._version_data_set_name,
                {"status": {"conditions": conditions}},
            )

            return {"status": 200, "message": "更新数据集状态成功", "data": ""}
        except Exception as ex:
            logger.error(str(ex))
            return {"status": 400, "message": "更新数据集状态失败", "data": ""}


class Model:
    def __init__(self, namespace, name, kubeconfig_path):
        self._namespace = namespace
        self._name = name
        self._kube = KubeEnv(kubeconfig_path=kubeconfig_path)

    def get_spec_for_llms_k8s_cr(self):
        """get worker model.

        name: model name;
        namespace: namespace;
        """
        try:
            one_cr_llm = self._kube.get_versionedmodels_status(
                namespace=self._namespace, name=self._name
            )

            provider = one_cr_llm["spec"]

            return {"status": 200, "message": "获取llms中的provider成功", "data": provider}
        except Exception as ex:
            logger.error(str(ex))
            return {"status": 400, "message": "获取llms中的provider失败", "data": ""}

    def get_spec_for_embedding_k8s_cr(self):
        """get embedding.

        name: model name;
        namespace: namespace;
        """
        try:
            one_cr_llm = self._kube.get_versionedembedding_status(
                namespace=self._namespace, name=self._name
            )

            provider = one_cr_llm["spec"]

            return {
                "status": 200,
                "message": "获取embedding中的provider成功",
                "data": provider,
            }
        except Exception as ex:
            logger.error(str(ex))
            return {"status": 400, "message": "获取embedding中的provider失败", "data": ""}
