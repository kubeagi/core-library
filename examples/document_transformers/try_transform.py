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


from kubeagi_core.document_transformers.transform import Clean, DataConvert, FixUnicode


def test_traditional_to_simplified():
    print(">>> Starting traditional to simplified")
    text = "風暴帶來的暫停使消防員和其他緊急反應人員得以進入禁區進行結構破壞評估。"
    data_convert = DataConvert()

    clean_text = data_convert.chinese_convert(text)
    print("<<< Finished")
    print(f"clean text: {clean_text}")


def test_bank_card_convert():
    print(">>> Starting convert bank card")
    text = "银行卡号1：1234567890123456，银行卡号2：12345678901234567，银行卡号3：1234567890123456789"
    data_convert = DataConvert()

    clean_text = data_convert.bank_card_convert(text=text, repl="xxxx")
    print("<<< Finished")
    print(f"clean text: {clean_text}")


def test_email_convert():
    print(">>> Starting convert email")
    text = "如果需要可以联系官方邮箱:172817631@qq.com马上申请为你开通"
    data_convert = DataConvert()

    clean_text = data_convert.email_convert(text=text, repl="xxxx")
    print("<<< Finished")
    print(f"clean text: {clean_text}")


def test_emoji_convert():
    print(">>> Starting convert emoji")
    text = "这是一段带有表情符号😊的文本。"
    data_convert = DataConvert()

    clean_text = data_convert.emojis_convert(text=text, repl="xxxx")
    print("<<< Finished")
    print(f"clean text: {clean_text}")


def test_clean_html():
    print(">>> Starting convert emoji")
    text = "<div class='center'><span class='bolded'>学员成绩单分析报告"
    clean = Clean()

    clean_text = clean.clean_html(text=text)
    print("<<< Finished")
    print(f"clean text: {clean_text}")


def test_id_card_convert():
    print(">>> Starting convert id card")
    text = "身份证号1：123451230112121234, 身份证号2：12345123011212123x"
    data_convert = DataConvert()

    clean_text = data_convert.id_card_convert(text=text, repl="xxxx")
    print("<<< Finished")
    print(f"clean text: {clean_text}")


def test_ip_convert():
    print(">>> Starting convert ip")
    text = "服务器登陆ip为192.168.255.255"
    data_convert = DataConvert()

    clean_text = data_convert.ip_convert(text=text, repl="xxxx")
    print("<<< Finished")
    print(f"clean text: {clean_text}")


def test_phone_convert():
    print(">>> Starting convert phone")
    text = "手机号为18672615192"
    data_convert = DataConvert()

    clean_text = data_convert.phone_convert(text=text, repl="xxxx")
    print("<<< Finished")
    print(f"clean text: {clean_text}")


def test_weixin_convert():
    print(">>> Starting convert weixin")
    text = "你的wx：qw123"
    data_convert = DataConvert()

    clean_text = data_convert.weixin_convert(text=text, repl="xxxx")
    print("<<< Finished")
    print(f"clean text: {clean_text}")


def test_fix_unicode():
    print(">>> Starting fix unicode")
    text = "法律工作者。 â€” like this one."
    fix_unicode = FixUnicode()

    clean_text = fix_unicode.process(text=text)
    print("<<< Finished")
    print(f"clean text: {clean_text}")


def test_invisible_characterse_convert():
    print(">>> Starting convert invisible characterse")
    text = "一户一表、水表出户、抄表到户"
    data_convert = DataConvert()

    clean_text = data_convert.invisible_characters_convert(text=text, repl="")
    print("<<< Finished")
    print(f"clean text: {clean_text}")


def test_space_convert():
    print(">>> Starting convert space")
    text = "41　行业大模型标准体系及能力架构研究报告行业大模型“千行百业”落地"
    data_convert = DataConvert()

    clean_text = data_convert.space_convert(text=text, repl=" ")
    print("<<< Finished")
    print(f"clean text: {clean_text}")
