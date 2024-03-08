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


import emoji
import opencc
import re
import ftfy

from selectolax.parser import HTMLParser
from . import special_characters


class DataConvert:
    def chinese_convert(self, text, mode: str = "t2s"):
        """
        :param mode: Choose the mode to convert Chinese,
        s2t: Simplified Chinese to Traditional Chinese,
        t2s: Traditional Chinese to Simplified Chinese,
        s2tw: Simplified Chinese to Traditional Chinese (Taiwan Standard),
        tw2s: Traditional Chinese (Taiwan Standard) to Simplified Chinese,
        s2hk: Simplified Chinese to Traditional Chinese (Hong Kong variant),
        hk2s: Traditional Chinese (Hong Kong variant) to Simplified Chinese,
        s2twp: Simplified Chinese to Traditional Chinese (Taiwan Standard)
               with Taiwanese idiom,
        tw2sp: Traditional Chinese (Taiwan Standard) to Simplified Chinese
               with Mainland Chinese idiom,
        t2tw: Traditional Chinese to Traditional Chinese (Taiwan Standard),
        tw2t: Traditional Chinese (Taiwan standard) to Traditional Chinese,
        hk2t: Traditional Chinese (Hong Kong variant) to Traditional Chinese,
        t2hk: Traditional Chinese to Traditional Chinese (Hong Kong variant),
        t2jp: Traditional Chinese Characters (Kyūjitai) to New Japanese Kanji,
        jp2t: New Japanese Kanji (Shinjitai) to Traditional Chinese Characters,
        """
        mode_list = [
            "s2t",
            "t2s",
            "s2tw",
            "tw2s",
            "s2hk",
            "hk2s",
            "s2twp",
            "tw2sp",
            "t2tw",
            "tw2t",
            "hk2t",
            "t2hk",
            "t2jp",
            "jp2t",
        ]
        assert mode in mode_list, "Please make sure mode is one of {}".format(mode_list)

        clean_text = opencc.OpenCC(mode).convert(text)
        return clean_text

    def bank_card_convert(self, text, pattern: str = None, repl: str = ""):
        """convert bank card in text."""
        if pattern is None:
            pattern = r"\b([1-9]{1})(\d{15}|\d{18})(?![0-9])"

        if not re.search(pattern, text, flags=re.DOTALL):
            return text

        clean_text = re.sub(pattern=pattern, repl=repl, string=text, flags=re.DOTALL)
        return clean_text

    def email_convert(self, text, pattern: str = None, repl: str = ""):
        """convert email in text."""
        if pattern is None:
            pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

        if not re.search(pattern, text, flags=re.DOTALL):
            return text

        clean_text = re.sub(pattern=pattern, repl=repl, string=text, flags=re.DOTALL)
        return clean_text

    def emojis_convert(self, text, pattern: str = None, repl: str = ""):
        """convert emojis in text."""
        if pattern is None:
            emojis = list(emoji.EMOJI_DATA.keys())
            pattern = "|".join(re.escape(value) for value in emojis)

        if not re.search(pattern, text, flags=re.DOTALL):
            return text

        clean_text = re.sub(pattern=pattern, repl=repl, string=text, flags=re.DOTALL)
        return clean_text

    def id_card_convert(self, text, repl: str = ""):
        """convert id card in text."""
        pattern = [
            r"\b([1-9]\d{5}[1-9]\d{3})((0\d)|(1[0-2]))(([0|1|2]\d)|(3[0-1]))(\d{3}[0-9Xx])(?![0-9])",
            r"\b([1-9]\d{7})((0\d)|(1[0-2]))(([0-2][1-9])|(3[0-1]))(\d{2}[0-9Xx])(?![0-9])",
        ]

        for regex_exp in pattern:
            text = re.sub(pattern=regex_exp, repl=repl, string=text, flags=re.DOTALL)
        return text

    def ip_convert(self, text, pattern: str = None, repl: str = ""):
        """convert ip in text."""
        if pattern is None:
            pattern = "".join(
                [
                    r"((?:(?:1[0-9][0-9]\.)|(?:2[0-4][0-9]\.)|",
                    r"(?:25[0-5]\.)|(?:[1-9][0-9]\.)|(?:[0-9]\.))",
                    r"{3}(?:(?:1[0-9][0-9])|(?:2[0-4][0-9])|",
                    r"(?:25[0-5])|(?:[1-9][0-9])|(?:[0-9]))|",
                    r"([\da-fA-F]{1,4}:){7}[\da-fA-F]{1,4})",
                ]
            )

        if not re.search(pattern, text, flags=re.DOTALL):
            return text

        clean_text = re.sub(pattern=pattern, repl=repl, string=text, flags=re.DOTALL)
        return clean_text

    def phone_convert(self, text, pattern: str = None, repl: str = ""):
        """convert ip in text."""
        if pattern is None:
            pattern = r"((\+|00)86)?(1)((3[\d])|(4[5,6,7,9])|(5[0-3,5-9])|(6[5-7])|(7[0-8])|(8[\d])|(9[1,8,9]))(\d{8})(?![0-9])"

        if not re.search(pattern, text, flags=re.DOTALL):
            return text

        clean_text = re.sub(pattern=pattern, repl=repl, string=text, flags=re.DOTALL)
        return clean_text

    def weixin_convert(self, text, pattern: str = None, repl: str = ""):
        """convert weixin in text."""
        if pattern is None:
            pattern = [
                r"vxin[：|:][a-zA-Z0-9{3,20}]+",
                r"vx[：|:][a-zA-Z0-9{3,20}]+",
                r"VX[：|:][a-zA-Z0-9{3,20}]+",
                r"Vxin[：|:][a-zA-Z0-9{3,20}]+",
                r"wx[：|:][a-zA-Z0-9{3,20}]+",
                r"WX[：|:][a-zA-Z0-9{3,20}]+",
                r"wei xin[：|:][a-zA-Z0-9{3,20}]+",
                r"weixin[：|:][a-zA-Z0-9{3,20}]+",
                r"微信[：|:][a-zA-Z0-9{3,20}]+",
                r"微信号[：|:][a-zA-Z0-9{3,20}]+",
                r"薇信[：|:][a-zA-Z0-9{3,20}]+",
                r"薇信号[：|:][a-zA-Z0-9{3,20}]+",
                r"v信[：|:][a-zA-Z0-9{3,20}]+",
                r"V信[：|:][a-zA-Z0-9{3,20}]+",
            ]

        for regex_exp in pattern:
            text = re.sub(pattern=regex_exp, repl=repl, string=text, flags=re.DOTALL)
        return text

    def invisible_characters_convert(self, text, pattern: str = None, repl: str = ""):
        """convert invisible characters in text."""
        if pattern is None:
            pattern = r"[\x00-\x1F\x7F-\x9F\xAD\r\t\b\x0B\x1C\x1D\x1E]"

        if not re.search(pattern, text, flags=re.DOTALL):
            return text

        clean_text = re.sub(pattern=pattern, repl=repl, string=text, flags=re.DOTALL)
        return clean_text

    def space_convert(self, text, pattern: str = None, repl: str = " "):
        """convert space in text."""
        if pattern is None:
            various_whitespaces = special_characters.VARIOUS_WHITESPACES
            pattern = "|".join(re.escape(value) for value in various_whitespaces)

        if not re.search(pattern, text, flags=re.DOTALL):
            return text

        clean_text = re.sub(pattern=pattern, repl=repl, string=text, flags=re.DOTALL)
        return clean_text


class Clean:
    def clean_html(self, text):
        """clean html in text."""
        text = text.replace("<li>", "\n*")
        text = text.replace("</li>", "")
        text = text.replace("<ol>", "\n*")
        text = text.replace("</ol>", "")
        parser = HTMLParser(text)

        clean_text = parser.text()
        return clean_text


class FixUnicode:
    """fix unicode errors in text."""

    def __init__(self, normalization: str = None):
        """
        Initialization method.

        :param normalization: the specified form of Unicode
             normalization mode, which can be one of ['NFC',
            'NFKC', 'NFD', and 'NFKD'], default 'NFC'
        """
        if normalization and len(normalization) > 0:
            self._normalization = normalization.upper()
        else:
            self._normalization = "NFC"

        if self._normalization.upper() not in ["NFC", "NFKC", "NFD", "NFKD"]:
            raise ValueError(
                f"Normalization mode [{normalization}] is not "
                "supported. Can only be one of "
                '["NFC", "NFKC", "NFD", "NFKD"]'
            )

    def process(self, text):
        clean_text = ftfy.fix_text(text, normalization=self._normalization)
        return clean_text
