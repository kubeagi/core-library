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

from kubeagi_core.kube.custom_controller import Dataset


def test_update_dataset_k8s_cr():
    print(">>> Starting update dataset k8s cr status.")
    dataset = Dataset(
        namespace="rag-eval",
        version_data_set_name="test-v1",
        kubeconfig_path="/happy_work_space/.kube/config",
    )

    res = dataset.update_dataset_k8s_cr(
        reason="processing", message="Data processing in progress"
    )
    print("<<< Finished")
    print(f"{res}")


if __name__ == "__main__":
    test_updata_dataset_k8s_cr()
