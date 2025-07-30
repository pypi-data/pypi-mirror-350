from bidict import bidict

inuktitut_map = bidict(
    {
        "i": "ᐃ",
        "ii": "ᐄ",
        "u": "ᐅ",
        "uu": "ᐆ",
        "a": "ᐊ",
        "aa": "ᐋ",
        "h": "ᕼ",
        "pi": "ᐱ",
        "pii": "ᐲ",
        "pu": "ᐳ",
        "puu": "ᐴ",
        "pa": "ᐸ",
        "paa": "ᐹ",
        "p": "ᑉ",
        "ti": "ᑎ",
        "tii": "ᑏ",
        "tu": "ᑐ",
        "tuu": "ᑑ",
        "ta": "ᑕ",
        "taa": "ᑖ",
        "t": "ᑦ",
        "ki": "ᑭ",
        "kii": "ᑮ",
        "ku": "ᑯ",
        "kuu": "ᑰ",
        "ka": "ᑲ",
        "kaa": "ᑳ",
        "k": "ᒃ",
        "gi": "ᒋ",
        "gii": "ᒌ",
        "gu": "ᒍ",
        "guu": "ᒎ",
        "ga": "ᒐ",
        "gaa": "ᒑ",
        "g": "ᒡ",
        "mi": "ᒥ",
        "mii": "ᒦ",
        "mu": "ᒧ",
        "muu": "ᒨ",
        "ma": "ᒪ",
        "maa": "ᒫ",
        "m": "ᒻ",
        "ni": "ᓂ",
        "nii": "ᓃ",
        "nu": "ᓄ",
        "nuu": "ᓅ",
        "na": "ᓇ",
        "naa": "ᓈ",
        "n": "ᓐ",
        "si": "ᓯ",
        "sii": "ᓰ",
        "su": "ᓱ",
        "suu": "ᓲ",
        "sa": "ᓴ",
        "saa": "ᓵ",
        "s": "ᔅ",
        "li": "ᓕ",
        "lii": "ᓖ",
        "lu": "ᓗ",
        "luu": "ᓘ",
        "la": "ᓚ",
        "laa": "ᓛ",
        "l": "ᓪ",
        "ji": "ᔨ",
        "jii": "ᔩ",
        "ju": "ᔪ",
        "juu": "ᔫ",
        "ja": "ᔭ",
        "jaa": "ᔮ",
        "j": "ᔾ",
        "vi": "ᕕ",
        "vii": "ᕖ",
        "vu": "ᕗ",
        "vuu": "ᕘ",
        "va": "ᕙ",
        "vaa": "ᕚ",
        "v": "ᕝ",
        "ri": "ᕆ",
        "rii": "ᕇ",
        "ru": "ᕈ",
        "ruu": "ᕉ",
        "ra": "ᕋ",
        "raa": "ᕌ",
        "r": "ᕐ",
        "qi": "ᕿ",
        "qii": "ᖀ",
        "qu": "ᖁ",
        "quu": "ᖂ",
        "qa": "ᖃ",
        "qaa": "ᖄ",
        "q": "ᖅ",
        "ngi": "ᖏ",
        "ngii": "ᖐ",
        "ngu": "ᖑ",
        "nguu": "ᖒ",
        "nga": "ᖓ",
        "ngaa": "ᖔ",
        "ng": "ᖕ",
        "lhi": "ᖠ",
        "lhii": "ᖡ",
        "lhu": "ᖢ",
        "lhuu": "ᖣ",
        "lha": "ᖤ",
        "lhaa": "ᖥ",
        "lh": "ᖦ",
        "nngi": "ᙱ",
        "nngii": "ᙲ",
        "nngu": "ᙳ",
        "nnguu": "ᙴ",
        "nnga": "ᙵ",
        "nngaa": "ᙶ",
        "nng": "ᖖ",
        "qqi": "ᖅᑭ",
        "qqii": "ᖅᑮ",
        "qqu": "ᖅᑯ",
        "qquu": "ᖅᑰ",
        "qqa": "ᖅᑲ",
        "qqaa": "ᖅᑳ",
    }
)

# Reverse map
unicode_to_roman = inuktitut_map.inverse
longest_key_length = max(len(key) for key in inuktitut_map)


def _syllabify(text):
    i = 0
    segment = ""
    output = []
    match = None

    while i < len(text):
        matched = False
        for ln in range(longest_key_length, 1, -1):
            segment = text[i : i + ln]
            if segment[0] == "&":  # handle alternate romanization
                segment = "lh" + segment[1:]
            if segment in inuktitut_map:
                match = inuktitut_map[segment]
                matched = True
                i += ln
                break
        if matched:
            output.append(match)
        else:
            output.append(text[i])
            i += 1
    return "".join(output)


def _romanize(text):
    output = []
    was_bigraph = False
    for syll, next_syll in zip(text, text[1:]):
        if was_bigraph:
            was_bigraph = False
            continue
        elif syll != "ᖅ":
            output.append(unicode_to_roman.get(syll, syll))
        elif syll + next_syll in unicode_to_roman:
            was_bigraph = True
            output.append(unicode_to_roman.get(syll + next_syll))
        else:
            output.append(unicode_to_roman.get(syll, syll))
    if not was_bigraph:
        output.append(unicode_to_roman.get(text[-1], text[-1]))
    return "".join(output)


def syllabify(text):
    """
    Convert a romanized Inuktitut string to its syllabified Unicode equivalent.
    """
    return _syllabify(text)


def romanize(text):
    """
    Convert a Unicode Inuktitut string to its romanized equivalent.
    """
    return _romanize(text)
