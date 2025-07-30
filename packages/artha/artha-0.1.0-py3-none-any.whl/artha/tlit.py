# Copyright © 2024 Yash Bonde
# https://www.unicode.org/charts/PDF/U0900.pdf
# https://www.tug.org/TUGboat/Articles/tb19-4/tb61pand.pdf
# https://gretil.sub.uni-goettingen.de/gretil/gretdias.pdf
# https://gretil.sub.uni-goettingen.de/gretil/gretdiac.pdf
# https://en.wikipedia.org/wiki/International_Alphabet_of_Sanskrit_Transliteration

# IAST to SLP1
IAST2SLPI_duos = {
    "ai": "E",
    "au": "O",
    "kh": "K",
    "gh": "G",
    "ch": "C",
    "jh": "J",
    "ṭh": "W",
    "ḍh": "Q",
    "th": "T",
    "dh": "D",
    "ph": "P",
    "bh": "B",
    "ū̱": "U",  # << added
    "ā̱": "A",  # << added
    "a̱": "a",  # << added
    "u̱": "u",  # << added
    "e̱": "e",  # << added
    "o̱": "o",  # << added
    "ṛ̱": "f",  # << added
    "i̱": "i",  # << added
    "m̐": "~",  # << added
    "ī̱": "I",  # << added
    "ṝ": "F",  # << added, https://en.wikipedia.org/wiki/%E1%B9%9C
    "l̥": "x",  # << added
}
for k in IAST2SLPI_duos:
    assert len(k) == 2, f"IAST2SLPI_duos: {k} is not a duo"

IAST2SLPI_monos = {
    "ā": "A",
    "ī": "I",
    "ū": "U",
    "ṛ": "f",
    "ṝ": "F",
    "ḷ": "x",
    "ḹ": "X",
    "ṃ": "M",
    "ṁ": "~",
    "ḥ": "H",
    "ṅ": "N",
    "ñ": "Y",
    "ṭ": "w",
    "ḍ": "q",
    "ṇ": "R",
    "ś": "S",
    "ṣ": "z",
    "ē": "e",  # << added
    "ō": "o",  # << added
    "ḻ": "L",  # << added
}
for k in IAST2SLPI_monos:
    assert len(k) == 1, f"IAST2SLPI_monos: {k} is not a mono"

# there should be nothing common between IAST and SLP1
_common_keys = set(IAST2SLPI_duos.keys()) & set(IAST2SLPI_monos.keys())
if len(_common_keys) > 0:
    raise ValueError(
        f"IAST2SLPI_duos and IAST2SLPI_monos have common keys: {_common_keys}"
    )

# SLPI to Devanagari
SLPI2DEV_vowels = {
    "a": ["अ", ""],
    "A": ["आ", "ा"],
    "i": ["इ", "ि"],
    "I": ["ई", "ी"],
    "u": ["उ", "ु"],
    "U": ["ऊ", "ू"],
    "f": ["ऋ", "ृ"],
    "F": ["ॠ", "ॄ"],
    "x": ["ऌ", "ॢ"],
    "X": ["ॡ", "ॣ"],
    "e": ["ए", "े"],
    "E": ["ऐ", "ै"],
    # "E̱": "E",  # << added
    "o": ["ओ", "ो"],
    "O": ["औ", "ौ"],
    "'": ["ऽ", ""],  # << added
}
SLPI2DEV_consonants = {
    "k": "क",
    "K": "ख",
    "g": "ग",
    "G": "घ",
    "N": "ङ",
    "c": "च",
    "C": "छ",
    "j": "ज",
    "J": "झ",
    "Y": "ञ",
    "w": "ट",
    "W": "ठ",
    "q": "ड",
    "Q": "ढ",
    "R": "ण",
    "t": "त",
    "T": "थ",
    "d": "द",
    "D": "ध",
    "n": "न",
    "p": "प",
    "P": "फ",
    "b": "ब",
    "B": "भ",
    "m": "म",
    "y": "य",
    "r": "र",
    "l": "ल",
    "v": "व",
    "S": "श",
    "z": "ष",
    "s": "स",
    "h": "ह",
    "L": "ळ",  # << added
}

IAST2SLPI_monos.update({k: k for k in SLPI2DEV_consonants})
for k in IAST2SLPI_monos:
    assert len(k) == 1, f"IAST2SLPI_monos: {k} is not a mono"

SLPI2DEV_others = {"M": "ं", "H": "ः", "~": "ँ", "'": "ऽ"}
SLPI2DEV_digits = {
    "0": "०",
    "1": "१",
    "2": "२",
    "3": "३",
    "4": "४",
    "5": "५",
    "6": "६",
    "7": "७",
    "8": "८",
    "9": "९",
}


def iast2dev(
    src,
    lower=False,
    clean_perc: bool = True,
    verbose=False,
    convert_numbers=True,
):
    # STEP 1: IAST to SLP1
    # process string
    if lower:
        src = src.lower()
    if clean_perc:
        src = src.replace("%", "")
    src = src.replace("3̱̍", "")
    src = src.replace(chr(781), "")
    if verbose:
        print(src)

    tgt_spli = ""
    inc = 0
    while inc < len(src):
        now = src[inc]
        nxt = src[inc + 1] if inc < len(src) - 1 else ""
        if now + nxt in IAST2SLPI_duos:
            tgt_spli += IAST2SLPI_duos[now + nxt]
            inc += 1
        elif now in IAST2SLPI_monos:
            tgt_spli += IAST2SLPI_monos[now]
        else:
            tgt_spli += now
        inc += 1

    if verbose:
        print(">>>", tgt_spli)

    # STEP 2: SLP1 to Devanagari
    tgt_dev = ""
    boo = False
    inc = 0
    while inc < len(tgt_spli):
        pre = tgt_spli[inc - 1] if inc > 1 else ""
        now = tgt_spli[inc]
        if now == chr(817):
            inc += 1
            continue
        nxt = tgt_spli[inc + 1] if inc < len(tgt_spli) - 1 else ""
        if now in SLPI2DEV_consonants:
            tgt_dev += SLPI2DEV_consonants[now]
            if nxt == "a":
                inc += 1
            elif nxt in SLPI2DEV_vowels:
                boo = True
            else:
                tgt_dev += "्"
        elif now in SLPI2DEV_vowels:
            vowel = SLPI2DEV_vowels[now]
            if type(vowel) == str:
                # print("SADFASDFADSFASDFASDFASDFA", now, vowel, SLPI2DEV_vowels[vowel])
                vowel = SLPI2DEV_vowels[vowel]
            if boo:
                tgt_dev += vowel[1]
                boo = False
            else:
                tgt_dev += vowel[0]
        elif now == "'":
            if not pre or not nxt:
                tgt_dev += now
            elif ord(pre) in range(65, 123) and ord(nxt) in range(65, 123):
                tgt_dev += "ऽ"
            else:
                tgt_dev += now
        elif now in SLPI2DEV_others:
            tgt_dev += SLPI2DEV_others[now]
        elif now in SLPI2DEV_digits:
            if convert_numbers:
                tgt_dev += SLPI2DEV_digits[now]
            else:
                tgt_dev += now
        elif now == ".":
            if nxt == ".":
                tgt_dev += "॥"
                inc += 1
            else:
                tgt_dev += "।"
        else:
            tgt_dev += now
        inc += 1
    return tgt_dev


# Reverse dictionaries for devanagari to SLP1 and SLP1 to IAST
DEV2SLPI_consonants = {v: k for k, v in SLPI2DEV_consonants.items()}
DEV2SLPI_vowels = {
    v[0]: k for k, v in SLPI2DEV_vowels.items()
}  # Only taking the standalone vowel
DEV2SLPI_vowel_marks = {
    v[1]: k for k, v in SLPI2DEV_vowels.items() if v[1]
}  # Vowel marks
DEV2SLPI_others = {v: k for k, v in SLPI2DEV_others.items()}
SLPI2IAST_monos = {v: k for k, v in IAST2SLPI_monos.items()}
SLPI2IAST_duos = {v: k for k, v in IAST2SLPI_duos.items()}


def dev2slpi(src: str, verbose: bool = False) -> str:
    """Converts Devanagari to SLP1."""
    tgt_slpi = ""
    i = 0
    while i < len(src):
        char = src[i]
        next_char = src[i + 1] if i + 1 < len(src) else None

        if char in DEV2SLPI_consonants:
            tgt_slpi += DEV2SLPI_consonants[char]
            if next_char == "्":  # Halant
                i += 1  # Skip halant
            elif next_char in DEV2SLPI_vowel_marks:
                tgt_slpi += "a"
        elif char in DEV2SLPI_vowels:
            tgt_slpi += DEV2SLPI_vowels[char]
        elif char in DEV2SLPI_vowel_marks:
            tgt_slpi += DEV2SLPI_vowel_marks[char]
        elif char in DEV2SLPI_others:
            tgt_slpi += DEV2SLPI_others[char]
        elif char in SLPI2DEV_digits.values():
            # Find the key in SLPI2DEV_digits where the value is char
            tgt_slpi += next(k for k, v in SLPI2DEV_digits.items() if v == char)
        elif char == "॥":
            tgt_slpi += ".."
            # already incremented.
        elif char == "।":
            tgt_slpi += "."
        else:
            tgt_slpi += char  # Keep unknown characters

        i += 1
    if verbose:
        print(f"Devanagari to SLP1: {src} -> {tgt_slpi}")
    return tgt_slpi


def slpi2iast(src: str, verbose: bool = False) -> str:
    """Converts SLP1 to IAST."""
    tgt_iast = ""
    i = 0
    while i < len(src):
        char = src[i]
        next_char = src[i + 1] if i + 1 < len(src) else None

        if next_char:
            if char + next_char in SLPI2IAST_duos:
                tgt_iast += SLPI2IAST_duos[char + next_char]
                i += 1  # Consume the next character
            elif char in SLPI2IAST_monos:
                tgt_iast += SLPI2IAST_monos[char]
            else:
                tgt_iast += char  # Keep unknown characters
        i += 1
    if verbose:
        print(f"SLP1 to IAST: {src} -> {tgt_iast}")
    return tgt_iast


def dev2iast(src: str, verbose: bool = False) -> str:
    """Converts Devanagari to IAST."""
    slpi_text = dev2slpi(src, verbose)
    iast_text = slpi2iast(slpi_text, verbose)
    return iast_text
