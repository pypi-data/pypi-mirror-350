import re

from typing import Literal, TypedDict

CH_ARAB = r"\d"
CH_ATOZ = r"a-zA-Zα-ωΑ-Ω"
CH_CJK = r"\u4E00-\u9FFF\u3040-\u30FF〇"
CH_DASH = r"\-\+\_\."
CH_MASK = r"▂"

RE_ARAB = rf"[{CH_ARAB}]+"
RE_ATOZ = rf"[{CH_ATOZ}]+"
RE_CJK = rf"[{CH_CJK}]+"
RE_DASH = rf"[{CH_DASH}]+"
RE_MASK = rf"[{CH_MASK}]+"
RE_NORD = rf"[^{CH_ARAB}{CH_ATOZ}{CH_CJK}{CH_DASH}{CH_MASK}]+"

RE_CATOG = rf"(?P<arab>{RE_ARAB})|(?P<atoz>{RE_ATOZ})|(?P<cjk>{RE_CJK})|(?P<dash>{RE_DASH})|(?P<mask>{RE_MASK})|(?P<nord>{RE_NORD})"

PT_CATOG = re.compile(RE_CATOG)

TOKEN_TYPE = Literal["arab", "atoz", "cjk", "dash", "mask", "nord"]


class TokenInfo(TypedDict):
    token: str
    type: TOKEN_TYPE
    beg: int
    end: int
    idx: int


class NgramTokenInfo(TokenInfo):
    type: Literal["ngram"] = "ngram"
    size: int


class SentenceCategorizer:
    def categorize(self, sentence: str, mask_nord: bool = True) -> list[TokenInfo]:
        """Categorize sentence to parts with types.

        Keys:
            - "token"
            - "type"
                - "arab", "atoz", "cjk", "dash", "mask", "nord"
            - "beg"
            - "end"
        """
        token_infos = []
        for match in PT_CATOG.finditer(sentence):
            token_text = match.group(0)
            token_type = match.lastgroup
            beg = match.start()
            end = match.end()
            token_info = {
                "token": token_text,
                "type": token_type,
                "beg": beg,
                "end": end,
            }
            token_infos.append(token_info)
        return token_infos

    def break_cjk(self, token_infos: list[TokenInfo]) -> list[TokenInfo]:
        """Break down multi-char cjk tokens into single-char tokens."""
        broken_token_infos: list[TokenInfo] = []
        token_idx = 0
        for token_info in token_infos:
            if token_info["type"] == "cjk" and len(token_info["token"]) > 1:
                for i, char in enumerate(token_info["token"]):
                    new_token_info = {
                        "token": char,
                        "type": "cjk",
                        "beg": token_info["beg"] + i,
                        "end": token_info["beg"] + i + 1,
                        "idx": token_idx,
                    }
                    broken_token_infos.append(new_token_info)
                    token_idx += 1
            else:
                broken_token_infos.append(token_info)
                token_idx += 1
        return broken_token_infos

    def ngramize(
        self,
        token_infos: list[TokenInfo],
        ngram_size: int,
        skip_nord: bool = True,
        replace_nord_with_whitespace: bool = True,
    ) -> list[TokenInfo]:
        """Create ngram tokens with ngram_size."""
        if ngram_size <= 1:
            return token_infos
        ngram_token_infos: list[TokenInfo] = []
        token_idx = 0
        for i in range(len(token_infos) - ngram_size + 1):
            if token_infos[i]["type"] == "nord" and skip_nord:
                continue
            ngram_token_info: NgramTokenInfo = {
                "token": "",
                "type": "ngram",
                "size": ngram_size,
                "beg": token_infos[i]["beg"],
                "end": -1,
            }
            ngram_count = 0
            for end_token_info in token_infos[i:]:
                if end_token_info["type"] == "nord" and skip_nord:
                    if replace_nord_with_whitespace:
                        ngram_token_info["token"] += " "
                    continue
                if ngram_count >= ngram_size:
                    break
                ngram_token_info["token"] += end_token_info["token"]
                ngram_token_info["end"] = end_token_info["end"]
                ngram_count += 1
            if ngram_count >= ngram_size:
                ngram_token_info["idx"] = token_idx
                ngram_token_infos.append(ngram_token_info)
                token_idx += 1
        return ngram_token_infos
