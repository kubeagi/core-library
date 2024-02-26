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

from kubeagi_core.kube.custom_controller import Model


def test_llms_info():
    print(">>> Start retrieving llms information.")
    model = Model(
        namespace="rag-eval",
        name="qwen-7b",
        kubeconfig_path="/happy_work_space/.kube/config",
    )

    res = model.get_spec_for_llms_k8s_cr()
    print("<<< Finished")
    print(f"{res}")


if __name__ == "__main__":
    test_llms_info()
