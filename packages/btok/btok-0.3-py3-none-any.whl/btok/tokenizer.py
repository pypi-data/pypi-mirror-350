import sentencepiece as spm

from pathlib import Path
from tclogger import logstr
from typing import Union

from .constants import PT_NON_WORD
from .constants import PT_DIGITS_ZH_WITH_UNIT, PT_DIGITS_UNITS_AND_NON_WORDS
from .constants import PT_ATOZ, PT_ATOZ_DIGITS_WORD
from .constants import PT_DIGITS_NUMBER, PT_ATOZ_DIGITS_NUMBER
from .constants import PT_DIGITS_ZH_WITH_UNIT_SINGLE_CHAR
from .constants import PT_CONCAT

from .utils import mask_ws_between_atoz, replace_mask_to_ws, calc_cjk_char_len
from .simplify import ChineseSimplifier

SP_MODEL_PATH = Path(__file__).parent / "sp.model"


class SentencePreTokenizer:
    def fill_str_parts(
        self, parts: list[tuple[int, int, str, str]], sentence: str
    ) -> list[tuple[str, str]]:
        """Fill str parts between non-word and digits
        Input: list of tuple: [(start:int, end:int, part:str, type:str), ...]
        Output: list of tuple: [(part:str, type:str), ...]
        """
        res: list[tuple[str, str]] = []
        parts.sort()
        start = 0
        for part_start, part_end, part, part_type in parts:
            if start < part_start:
                res.append((sentence[start:part_start], "str"))
            res.append((part, part_type))
            start = part_end
        if start < len(sentence):
            res.append((sentence[start:], "str"))
        return res

    def tokenize(self, sentence: str) -> list[tuple[str, str]]:
        """Split sentence by multiple parts, non-word, digits and non-digits
        Output: list of tuple (part:str, type:str)
        - part: str: digits, non-word, other string
        - type: "digits_with_unit", "digits_zh_with_unit", "non_word"
        """
        parts = []
        group_names = [
            "dashed_atoz_and_digits",
            "digits_with_unit",
            "digits_zh_with_unit",
            "non_word",
        ]
        sentence = mask_ws_between_atoz(sentence)
        for match in PT_DIGITS_UNITS_AND_NON_WORDS.finditer(sentence):
            for name in group_names:
                if match.group(name):
                    parts.append((match.start(), match.end(), match.group(name), name))
                    break
        res = self.fill_str_parts(parts, sentence)
        return res


class SentencePieceModelTokenizer:
    def __init__(self, model_path: Union[Path, str] = SP_MODEL_PATH):
        self.model_file = str(model_path)
        self.sp = spm.SentencePieceProcessor(model_file=self.model_file)

    def tokenize(self, sentence: str) -> list[str]:
        return self.sp.EncodeAsPieces(sentence)

    def tokenize_nbest(self, sentence: str, nbest_size: int = None) -> list[list[str]]:
        return self.sp.NBestEncodeAsPieces(sentence, nbest_size=nbest_size)

    def tokenize_maxlen(
        self,
        sentence: str,
        max_char_len: int = None,
        level: int = 0,
        max_level: int = 5,
        combine_singles: bool = False,
    ) -> list[str]:
        """Tokenize sentence to tokens with max_char_len,
        which means that, for each CJK token, its char length should be <= max_char_len.
        """
        if max_char_len is None or max_char_len < 1:
            return self.tokenize(sentence)

        if level == 0:
            tokens = self.tokenize(sentence)
        else:
            tokens = self.tokenize_nbest(sentence, nbest_size=2)[-1]
            if len(tokens) == 1 or level >= max_level:
                return tokens

        res = []
        for token in tokens:
            if calc_cjk_char_len(token) <= max_char_len:
                res.append(token)
            else:
                sub_tokens = self.tokenize_maxlen(
                    token,
                    max_char_len=max_char_len,
                    level=level + 1,
                    max_level=max_level,
                    combine_singles=combine_singles,
                )
                res.extend(sub_tokens)
        if combine_singles and all(calc_cjk_char_len(token) <= 1 for token in res):
            res = ["".join(res)]
        return res


class SentencePostTokenizer:
    def is_same_type(self, a: str, b: str) -> tuple[bool, str]:
        ab = f"{a}<SPT>{b}"
        match = PT_CONCAT.match(ab)
        if match:
            for name, value in match.groupdict().items():
                if value:
                    return True, name
        return False, "word"

    def split_atoz_and_digits(self, token: str) -> list[tuple[str, str]]:
        parts: list[tuple[str, str]] = []
        group_names = [
            "atoz",
            "digits_with_unit",
            "digits_number",
            "digits_zh_with_unit",
            "word",
        ]
        for match in PT_ATOZ_DIGITS_WORD.finditer(token):
            for name in group_names:
                if match.group(name):
                    parts.append((match.group(name), name))
        return parts

    def concat_same_types(self, tokens: list[str]) -> list[str]:
        """Examples:
        - [hb,k0,8,是] -> [hbk08,是]
        - [2024lbw,nb] -> [2024lbwnb]
        - [2024lbw, ,nb]-> [2024,lbw, ,nb]
        - [abc100,0,def123] -> [abc1000,def123]
        - [5a10,0d,def123d,?] -> [5a100,ddef123,d,?]
        """
        spt_str = "<SPT>".join(tokens)
        res_str = spt_str
        for match in PT_CONCAT.finditer(spt_str):
            value = match.group()
            new_value = value.replace("<SPT>", "")
            res_str = res_str.replace(value, new_value)
        return res_str.split("<SPT>")

    def get_token_type(self, token: str) -> str:
        for pattern, name in [
            (PT_ATOZ, "atoz"),
            (PT_DIGITS_NUMBER, "digits_number"),
            (PT_ATOZ_DIGITS_NUMBER, "atoz_digits_number"),
            (PT_DIGITS_ZH_WITH_UNIT, "digits_zh_with_unit"),
        ]:
            if pattern.fullmatch(token):
                return name
        return "raw"

    def merge_atoz_and_digits(self, tokens: list[str]) -> list[tuple[str, str]]:
        merges: list[tuple[str, str]] = []
        for token in tokens:
            token_type = self.get_token_type(token)
            if not merges:
                merges.append((token, token_type))
                continue
            last_token, last_token_type = merges[-1]
            if token_type in ["digits_number"] and last_token_type in [
                "atoz",
                "digits_number",
                "atoz_digits_number",
            ]:
                merges[-1] = (last_token + token, "atoz_digits_number")
            else:
                merges.append((token, token_type))
        return merges

    def concat_digits_zh_units_single_chars(
        self, tokens: list[str], model_tokenizer: SentencePieceModelTokenizer
    ) -> list[str]:
        spt_str = "<SPT>".join(tokens)
        res_str = spt_str
        for match in PT_DIGITS_ZH_WITH_UNIT_SINGLE_CHAR.finditer(spt_str):
            value = match.group()
            raw_value = value.replace("<SPT>", "")
            new_tokens = model_tokenizer.tokenize(raw_value)
            if len(new_tokens) == 1:
                new_value = "<SPT>" + "".join(new_tokens) + "<SPT>"
                res_str = res_str.replace(value, new_value)
        concat_tokens = res_str.split("<SPT>")
        return concat_tokens


class SentenceFullTokenizer:
    def __init__(
        self,
        model_path: Union[Path, str] = SP_MODEL_PATH,
        drop_non_word: bool = False,
        drop_whitespace: bool = False,
        simplify: bool = False,
        max_char_len: int = None,
        verbose: bool = False,
    ):
        self.model_path = model_path
        self.drop_non_word = drop_non_word
        self.drop_whitespace = drop_whitespace
        self.simplify = simplify
        self.hans_vocab = {}
        self.max_char_len = max_char_len
        self.verbose = verbose
        self.simplifier = ChineseSimplifier()
        self.pre_tokenizer = SentencePreTokenizer()
        self.post_tokenizer = SentencePostTokenizer()
        self.model_tokenizer = SentencePieceModelTokenizer(model_path)

    def preprocess_sentence(self, sentence: str) -> str:
        """lowercase, simplify"""
        sentence = sentence.lower()
        if self.simplify:
            sentence, self.hans_vocab = self.simplifier.simplify(
                sentence, return_vocab=True
            )
        else:
            self.hans_vocab = {}
        return sentence

    def tokenize_parts(self, parts: list[tuple], max_char_len: int = None) -> list[str]:
        res: list[str] = []
        for token, token_type in parts:
            if token_type == "str":
                max_char_len = max_char_len or self.max_char_len
                if max_char_len:
                    segs = self.model_tokenizer.tokenize_maxlen(token, max_char_len)
                else:
                    segs = self.model_tokenizer.tokenize(token)
                res.extend(segs)
            else:
                res.append(token)
        return res

    def stringify(self, tokens: list[str]) -> str:
        tokens_str = f"{logstr.note('_')}".join(tokens)
        return tokens_str

    def parts_to_tokens(self, parts: list[tuple]) -> list[str]:
        if not self.drop_non_word and not self.drop_whitespace:
            tokens = [part for part, type in parts]
        else:
            tokens = []
            for part, type in parts:
                if self.drop_non_word:
                    token = PT_NON_WORD.sub("", part)
                if self.drop_whitespace:
                    # token = token.strip()
                    token = token.replace(" ", "")
                if token:
                    tokens.append(token)
        return tokens

    def remove_non_words(self, tokens: list[str]):
        res = []
        for token in tokens:
            token = PT_NON_WORD.sub("", token)
            if token:
                res.append(token)
        return res

    def remove_whitespaces(self, tokens: list[str]):
        return [token for token in tokens if token.strip()]

    def clean_tokens(self, tokens: list[str]):
        if self.drop_non_word:
            tokens = self.remove_non_words(tokens)
        if self.drop_whitespace:
            tokens = self.remove_whitespaces(tokens)
        if self.simplify and self.hans_vocab:
            tokens = [
                self.simplifier.convert_back(token, self.hans_vocab) for token in tokens
            ]
        tokens = replace_mask_to_ws(tokens)
        return tokens

    def tokenize(self, sentence: str) -> list[str]:
        sentence = self.preprocess_sentence(sentence)
        parts = self.pre_tokenizer.tokenize(sentence)
        tokens = self.tokenize_parts(parts)
        tokens = self.post_tokenizer.concat_same_types(tokens)
        tokens = self.post_tokenizer.concat_digits_zh_units_single_chars(
            tokens, self.model_tokenizer
        )
        tokens = self.clean_tokens(tokens)
        return tokens

    class TempMaxCharLen:
        def __init__(self, full_tokenizer, max_char_len: int = None):
            self.full_tokenizer = full_tokenizer
            self.old_max_char_len = self.full_tokenizer.max_char_len
            self.max_char_len = max_char_len

        def __enter__(self):
            self.full_tokenizer.max_char_len = self.max_char_len
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.full_tokenizer.max_char_len = self.old_max_char_len

    def temp_max_char_len(self, max_char_len: int = None):
        return self.TempMaxCharLen(self, max_char_len=max_char_len)
