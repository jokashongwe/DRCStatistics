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
        .replace("le", ",")
        .replace("dans", ",")
        .replace("tout", ",")
        .replace("tous", ",")
        .replace("type", ",")
        .replace("activité", ",")
        .replace("d'", ",")
        .replace("où", ",")
        .replace("par", ",")
        .replace(" comme ", ",")
        .replace("avec", ",")
        .replace(")", "")
        .replace(". ", ",")
        .split(",")
    )
    for index in range(len(words)):
        words[index] = words[index].strip()
    return words