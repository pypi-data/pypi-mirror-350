from .constants import CH_MASK, PT_ATOZ_WS
from .categorizer import PT_CATOG


def mask_ws_between_atoz(sentence: str) -> str:
    return PT_ATOZ_WS.sub(CH_MASK, sentence)


def replace_mask_to_ws(tokens: list[str]):
    return [token.replace(CH_MASK, " ") for token in tokens]


def calc_cjk_char_len(sent: str, include_alphanum: bool = True) -> int:
    cjk_char_len = 0
    for match in PT_CATOG.finditer(sent):
        token_text = match.group(0)
        token_type = match.lastgroup
        if token_type == "cjk":
            cjk_char_len += len(token_text)
        elif token_type in ["arab", "atoz"]:
            if include_alphanum:
                cjk_char_len += len(token_text.split())
        else:
            continue
    return cjk_char_len
