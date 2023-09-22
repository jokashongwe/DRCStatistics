def strim_strip(word: str):
    words = (
        word.replace("et", ",")
        .replace("with", "")
        .replace("regular", "")
        .replace("travel", "")
        .replace("parts", "")
        .replace("Country", "")
        .replace("to", "")
        .replace("other", "")
        .replace("of", "")
        .replace("the", "")
        .replace("ou", ",")
        .replace("(", ",")
        .replace("and", ",")
        .replace("or", ",")
        .replace(")", "")
        .replace(". ", ",")
        .split(",")
    )
    for index in range(len(words)):
        words[index] = words[index].strip()
    return words