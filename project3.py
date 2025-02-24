import requests


def get_shortest_shorter_synonym(word):
    """Fetches the shortest synonym for a given word using the Datamuse API."""
    url = f"https://api.datamuse.com/words?rel_syn={word}&max=20"
    try:
        response = requests.get(url)
        response.raise_for_status()
        synonyms = response.json()

        # Exclude synonyms containing spaces and those longer than the original word
        shorter_single_word_synonyms = [syn for syn in synonyms if
                                        ' ' not in syn['word'] and len(syn['word']) < len(word)]

        if not shorter_single_word_synonyms:
            return word
        shortest_synonym = min(shorter_single_word_synonyms, key=lambda syn: len(syn['word']))['word']
        return shortest_synonym
    except requests.RequestException as e:
        print(f"Error fetching synonyms for '{word}': {e}")
        return word


def compress_text(text):
    """Compresses text by replacing words with their shortest synonyms."""
    words = text.split()
    compressed_words = []
    metadata = {}
    for word in words:
        shortened_word = get_shortest_shorter_synonym(word)
        if shortened_word != word:
            compressed_words.append(shortened_word)
            # Store the hash of the original word in metadata
            metadata[shortened_word] = hash(word) % 16
        else:
            compressed_words.append(word)
    compressed_text = ' '.join(compressed_words)
    return compressed_text, metadata


def restore_text(compressed_text, metadata):
    """Attempts to restore the original text using the provided metadata."""
    words = compressed_text.split()
    restored_words = []
    for word in words:
        if word in metadata:
            hash_to_restore = metadata[word]

            # Fetch synonyms and try to match their hashes with the saved hash.
            url = f"https://api.datamuse.com/words?rel_syn={word}&max=30"
            try:
                response = requests.get(url)
                response.raise_for_status()
                synonyms = response.json()

                # Look for a synonym with a matching hash.
                for syn in synonyms:
                    if (hash(syn['word']) % 16 ) == hash_to_restore:
                        restored_words.append(syn['word'])
                        break
                else:
                    # If no match is found, append the word as is.
                    restored_words.append(word)

            except requests.RequestException as e:
                print(f"Error fetching synonyms for '{word}': {e}")
                restored_words.append(word)

        else:
            restored_words.append(word)
    restored_text = ' '.join(restored_words)
    return restored_text


if __name__ == '__main__':
    original_text = "This is an example paragraph where we demonstrate how longer words can be effectively compressed using synonyms."
    print("Original Text:", original_text)
    compressed_text, metadata = compress_text(original_text)
    print("Compressed Text:", compressed_text)
    restored_text = restore_text(compressed_text, metadata)
    print("Restored Text:", restored_text)
