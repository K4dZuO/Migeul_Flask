from better_profanity import profanity


def check_profanity(text: str) -> bool:
    return profanity.contains_profanity(text)
