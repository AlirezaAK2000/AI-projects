"""
app constants
"""

UNK_TAG = '<UNK>'
DIGIT_TAG = '<NUM>'
WEB_TAG = '<WEB>'
MOST_COMMON = {
    # "the", "be", "to", "of", "and", "a", "that", "have", "i"
    # , "it", "for", "not", "on", "he", "as", "you", "do", "at", "this", "but"
    # , "his", "by", "from", "they", "we", "her", "she", "or", "an", "will", "my", "would"
    # , "all", "me", "when", "no", "just", "him", "e" "<num>", "d",
    UNK_TAG, DIGIT_TAG, WEB_TAG, ".", "<num>"}
LANDAS = [0.192, 0.128, 0.68]
