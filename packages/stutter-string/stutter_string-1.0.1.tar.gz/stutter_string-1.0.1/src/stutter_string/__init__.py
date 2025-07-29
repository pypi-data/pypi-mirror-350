import string

def stutter(original_sentence: str, amount = 2, sep = " ") -> str:
    """
    Stutters your message
    Args:
        original_sentence (str): The sentence.
        amount (int): Amount of letters to repeat separated with a hyphen at the start of each word.
        sep (str, optional): The separator to use to separate words. Default is whitespace (' ').
    Returns:
        str: The stuttered sentence.
    """
    words = original_sentence.split(sep)
    new_words = []
    if len(words) == 0:
        return original_sentence
    for word in words:
        first_letter = word[0]
        if first_letter in string.ascii_letters:
            new_letter = (first_letter + "-") * max(0, amount - 1) + first_letter
            new_word = new_letter + word[1:]
            new_words.append(new_word)
    return sep.join(new_words)