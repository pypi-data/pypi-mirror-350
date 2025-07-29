import re

"""
GB2312 编码表:
    - https://www.toolhelper.cn/Encoding/GB2312
    - A1A0~A3FE (JP), A6A0~A9FE (ZH)
CJK Unicode Tables:
    - https://www.khngai.com/chinese/charmap/tbluni.php
    - 0x4E00~0x9FFF (ZH)
Unicode Kanji Table:
    - http://www.rikai.com/library/kanjitables/kanji_codes.unicode.shtml
    - 0x3040~0x30FF (JP)
"""

CH_LB = r"\(\[\{"
CH_RB = r"\)\]\}"
CH_CJK = r"\u4E00-\u9FFF\u3040-\u30FF"
CH_AB = r"0-9a-zA-Zα-ωΑ-Ω"
CH_DASH = r"\-\_\."
CH_CON = r"\-\_\.%‰〇"
CH_MASK = r"▂"

RE_SPACE_IN_CJK = rf"(?<=[{CH_CJK}])\s+(?=[{CH_CJK}])"
RE_NOT_DIGIT_DOT = r"\.(?!\d)"
RE_NON_WORD = rf"[^{CH_CJK}{CH_AB}{CH_CON}{CH_MASK}]+|{RE_NOT_DIGIT_DOT}"
RE_ATOZ_WS = r"(?<=[a-zA-Z])\s+(?=[a-zA-Z0-9])"

CH_DIGIT_PREFIX = r"第前这那每"
CH_UNIT_NUM = r"毫厘分个十百千万兆亿"
CH_UNIT_DATE = r"年岁月周日天夜号点分秒"
CH_UNIT_WEIGHT = r"吨斤升两克磅里平米尺寸吋亩"
CH_UNIT_PAPER = r"集章篇部卷节回页张句行词字"
CH_UNIT_OTHRES = r"季阶级系路元块折期课题届次名人份只头种件位艘架辆楼层套间室厅厨卫杀袋包箱台倍星枚连"
RE_UNIT_COMBO = rf"小时|分钟|年代|周[年岁]|世纪|倍[速镜]|平米|平方米|平方公里|[公海英]里|光年|公斤|英[镑尺寸吋]|[美日欧]元|[{CH_UNIT_NUM}][{CH_UNIT_WEIGHT}]"
RE_UNIT_EN = rf"([mck]m|[km]w|h|min|[ukm]g|[nmu]s|[km]hz|kwh)(?<!a-zA-Z)"

RE_UNITS_ALL = rf"({RE_UNIT_COMBO}|{RE_UNIT_EN}|[{CH_UNIT_NUM}{CH_UNIT_DATE}{CH_UNIT_WEIGHT}{CH_UNIT_PAPER}{CH_UNIT_OTHRES}])"
RE_DIGITS_WITH_PREFIX_AND_UNIT = rf"[{CH_DIGIT_PREFIX}]?\d+{RE_UNITS_ALL}"
RE_DIGITS_WITH_BOUND = r"(^|\b)\d+(\b|$)"
RE_DIGITS_ALL = rf"({RE_DIGITS_WITH_PREFIX_AND_UNIT}|{RE_DIGITS_WITH_BOUND})"

PT_ATOZ_WS = re.compile(RE_ATOZ_WS)

# ----- Pre-Tokenizer regex ----- #

CH_DIGIT_ZH = r"〇零一二两三四五六七八九十"
CH_DIGIT_ZH_MUL = r"十百千万亿"

RE_DIGITS_PURE = r"\d+"
RE_DOT_DIGITS = r"\d*(\.\d+)+"
RE_COMMA_DIGITS = r"\d+(\,\d+)+"
RE_DASHED_DIGITS = r"\d+(\-\d+)+"
RE_PERCENT = r"[%‰]*"
RE_DIGITS_AND_DOTS = rf"{RE_DOT_DIGITS}|{RE_DIGITS_PURE}"
RE_DIGITS_NUMBER = rf"(({RE_DOT_DIGITS}|{RE_COMMA_DIGITS}|{RE_DASHED_DIGITS}|{RE_DIGITS_PURE}){RE_PERCENT})"
RE_DIGITS_NUMBER_WITH_PREFIX_AND_UNIT = (
    rf"([{CH_DIGIT_PREFIX}]\s*)?{RE_DIGITS_NUMBER}\s*{RE_UNITS_ALL}"
)
RE_DIGITS_WITH_DOTS_AND_BRS = (
    rf"\[{RE_DIGITS_AND_DOTS}\]|\({RE_DIGITS_AND_DOTS}\)|{{{RE_DIGITS_AND_DOTS}}}"
)
RE_DIGITS_ALL = rf"(?:{RE_DIGITS_NUMBER_WITH_PREFIX_AND_UNIT}|{RE_DIGITS_WITH_DOTS_AND_BRS}|{RE_DIGITS_NUMBER})"

RE_NOT_DIGIT_DOT = r"\.(?!\d)"
RE_NOT_ALPHA_DASH = f"\-(?![a-zA-Z0-9])"
# RE_NON_WORD = rf"[^{CH_CJK}〇{CH_AB}\-\.%‰{CH_LB}{CH_RB}]+|{RE_NOT_DIGIT_DOT}"
RE_NON_WORD = (
    rf"[^{CH_CJK}〇{CH_AB}\-\.%‰{CH_MASK}]+|{RE_NOT_DIGIT_DOT}|{RE_NOT_ALPHA_DASH}"
)
RE_CH_CJK = rf"[{CH_CJK}]"

RE_DIGITS_ZH = (
    rf"(([{CH_DIGIT_ZH}][{CH_DIGIT_ZH_MUL}])+[{CH_DIGIT_ZH}]?|[{CH_DIGIT_ZH}]+)"
)
RE_DIGITS_ZH_WITH_UNIT = rf"[{CH_DIGIT_PREFIX}]?{RE_DIGITS_ZH}{RE_UNITS_ALL}"

RE_DASHED_ATOZ_AND_DIGITS = rf"[a-z0-9]+(\-[a-z0-9]+)+"

RE_DIGITS_UNITS_AND_NON_WORD = rf"(?P<dashed_atoz_and_digits>{RE_DASHED_ATOZ_AND_DIGITS}{RE_UNITS_ALL}?)|(?P<digits_with_unit>{RE_DIGITS_NUMBER_WITH_PREFIX_AND_UNIT})|(?P<digits_zh_with_unit>{RE_DIGITS_ZH_WITH_UNIT})|(?P<non_word>{RE_NON_WORD})"

PT_NON_WORD = re.compile(RE_NON_WORD)
PT_CH_CJK = re.compile(RE_CH_CJK)
PT_DIGITS_ZH_WITH_UNIT = re.compile(RE_DIGITS_ZH_WITH_UNIT)
PT_DIGITS_UNITS_AND_NON_WORDS = re.compile(RE_DIGITS_UNITS_AND_NON_WORD)


# ----- Post-Tokenizer regex ----- #

RE_ATOZ = rf"[a-zA-Z]+"
RE_ATOZ_DIGITS_NUMBER = rf"({RE_ATOZ}|{RE_DIGITS_NUMBER})"

RE_DIGITS_UNITS_TAIL = rf"[{CH_DIGIT_PREFIX}]?{RE_DIGITS_NUMBER}"
RE_DIGITS_UNITS_HEAD = rf"{RE_UNITS_ALL}"
RE_DIGITS_ZH_UNITS_HEAD = (
    rf"({RE_DIGITS_ZH}{RE_UNITS_ALL}|{RE_DIGITS_ZH}|{RE_UNITS_ALL})"
)

RE_WORD_EXCPET_ATOZ_OR_DIGITS = r"[^\da-zA-Z]+"
RE_ATOZ_DIGITS_WORD = rf"(?P<atoz>{RE_ATOZ})|(?P<digits_with_unit>{RE_DIGITS_ALL})|(?P<digits_number>{RE_DIGITS_NUMBER})|(?P<digits_zh_with_unit>{RE_DIGITS_ZH_WITH_UNIT})|(?P<word>{RE_WORD_EXCPET_ATOZ_OR_DIGITS})"

PT_ATOZ = re.compile(RE_ATOZ)
PT_DIGITS_NUMBER = re.compile(RE_DIGITS_NUMBER)
PT_ATOZ_DIGITS_NUMBER = re.compile(RE_ATOZ_DIGITS_NUMBER)
PT_ATOZ_DIGITS_WORD = re.compile(RE_ATOZ_DIGITS_WORD)

RE_ATOZ_CONCAT = rf"{RE_ATOZ}(?:<SPT>{RE_ATOZ})+"
RE_DIGITS_UNITS_CONCAT = rf"{RE_DIGITS_UNITS_TAIL}<SPT>{RE_DIGITS_UNITS_HEAD}"
RE_DIGITS_NUMBER_CONCAT = rf"{RE_DIGITS_NUMBER}(?:<SPT>{RE_DIGITS_NUMBER})+"
RE_DIGITS_ZH_UNITS_CONCAT = rf"{RE_DIGITS_ZH}<SPT>{RE_DIGITS_ZH_UNITS_HEAD}(?:<SPT>|$)"

RE_CONCAT = rf"(?P<atoz>{RE_ATOZ_CONCAT})|(?P<digits_number>{RE_DIGITS_NUMBER_CONCAT})"
PT_CONCAT = re.compile(RE_CONCAT)

RE_SINGLE_CJK_HEAD = rf"(^|<SPT>)[{CH_CJK}]"
RE_SINGLE_CJK_TAIL = rf"[{CH_CJK}](<SPT>|$)"
RE_DIGITS_ZH_WITH_UNIT_SPT = rf"<SPT>{RE_DIGITS_ZH_WITH_UNIT}<SPT>"
RE_DIGITS_ZH_WITH_UNIT_SINGLE_CHAR = rf"{RE_SINGLE_CJK_HEAD}{RE_DIGITS_ZH_WITH_UNIT_SPT}{RE_SINGLE_CJK_TAIL}|{RE_SINGLE_CJK_HEAD}{RE_DIGITS_ZH_WITH_UNIT_SPT}|{RE_DIGITS_ZH_WITH_UNIT_SPT}{RE_SINGLE_CJK_TAIL}"

PT_DIGITS_ZH_WITH_UNIT_SINGLE_CHAR = re.compile(RE_DIGITS_ZH_WITH_UNIT_SINGLE_CHAR)
