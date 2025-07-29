def word_count(text):
    return len(text.split())

def is_palindrome(word):
    word = word.lower().replace(" ", "")
    return word == word[::-1]

def capitalize_sentences(text):
    sentences = text.split('. ')
    return '. '.join(sentence.capitalize() for sentence in sentences)
