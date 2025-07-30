import string

def remove_punctuation(text):
  """Removes all punctuation from a given string."""
  if not isinstance(text, str):
    return "" # Handle non-string input gracefully

  translator = str.maketrans('', '', string.punctuation)
  return text.translate(translator)