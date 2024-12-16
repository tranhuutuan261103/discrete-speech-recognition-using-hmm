import os
import json

curent_path = os.path.dirname(os.path.abspath(__file__))
word_path = os.path.join(curent_path, '../words.json')

def get_word_by_id(word_id):
    try:
        with open(word_path, encoding='utf-8') as f:
            data = json.load(f)
        
        # Search for the word and return it
        for entry in data["words"]:
            if entry["id"] == word_id:
                return entry
            
        # If word not found, return None or raise an exception
        return None  # Word not found
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def get_word(word: str) -> None:
    try:
        with open(word_path, encoding='utf-8') as f:
            data = json.load(f)

        # Search for the word and return its ID
        for entry in data["words"]:
            if entry["word"] == word:
                return entry

        # If word not found, return -1 or raise an exception
        return None  # Word not found
    except Exception as e:
        print(f"Error: {e}")
        return None

def get_all_words(tiny=False) -> list:
    try:
        with open(word_path, encoding='utf-8') as f:
            data = json.load(f)
        
        # Return a list of all words
        if tiny:
            return [entry["word"] for entry in data["words"]]
        else:
            return data["words"]
    except Exception as e:
        print(f"Error: {e}")
        return None