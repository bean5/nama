from src.data.prepare import (
    normalize,
    merge_surname_prefixes,
    remove_noise_words,
    match_name_pairs,
    levenshtein_similarity,
)


test_normalize_data = [
    {"input": "john's", "is_surname": False, "result": ["john"]},
    {"input": "1st john", "is_surname": False, "result": ["john"]},
    {"input": "j0hn", "is_surname": False, "result": ["jhn"]},
    {"input": "a'lo`ha", "is_surname": False, "result": ["aloha"]},
    {"input": "ui li", "is_surname": False, "result": ["ui", "li"]},
    {"input": "ui li", "is_surname": True, "result": ["li"]},
    {"input": "ui", "is_surname": True, "result": ["ui"]},
    {"input": "John Paul", "is_surname": False, "result": ["john", "paul"]},
    {"input": "John-Paul", "is_surname": False, "result": ["john", "paul"]},
    {"input": "Василий", "is_surname": False, "result": ["vasilii"]},
    {"input": "王李", "is_surname": False, "result": ["wang", "li"]},
    {"input": "Смирнов", "is_surname": True, "result": ["smirnov"]},
    {"input": "Quitéria Da Conceição", "is_surname": True, "result": ["quiteria", "daconceicao"]},
    {"input": "Garcia O Ochoa", "is_surname": True, "result": ["garcia", "ochoa"]},
    {"input": "O Ochoa", "is_surname": True, "result": ["oochoa"]},
    {"input": "de Ochoa de Gutierrez", "is_surname": True, "result": ["deochoa", "degutierrez"]},
    {"input": "Sir King", "is_surname": True, "result": ["king"]},
    {"input": "Sir Jones King", "is_surname": True, "result": ["jones"]},
    {"input": "Sir Jones", "is_surname": True, "result": ["jones"]},
    {"input": "D R Jones", "is_surname": True, "result": ["jones"]},
    {"input": "D X Jones", "is_surname": True, "result": ["dx", "jones"]},
    {"input": "d r john", "is_surname": False, "result": ["d", "r", "john"]},
    {"input": "d gutierres", "is_surname": False, "result": ["d", "gutierres"]},
    {"input": "d gutierres", "is_surname": True, "result": ["dgutierres"]},
    {"input": "d gutierres", "is_surname": True, "result": ["dgutierres"]},
    {"input": "mendoza y gutierres", "is_surname": False, "result": ["mendoza", "gutierres"]},
    {"input": "mendoza j gutierres", "is_surname": False, "result": ["mendoza", "j", "gutierres"]},
    {"input": "mendoza y gutierres", "is_surname": True, "result": ["mendoza", "gutierres"]},
    {"input": "J", "is_surname": True, "result": ["j"]},
    {"input": "J", "is_surname": False, "result": ["j"]},
    {"input": "0 1 2 3", "is_surname": False, "result": ["0123"]},
    {"input": "0 1 2 3John@", "is_surname": False, "result": ["john"]},
    {"input": "Jo?n* Sm?th", "is_surname": False, "preserve_wildcards": True, "result": ["jo?n*", "sm?th"]},
]


def test_normalize():
    for test_data in test_normalize_data:
        result = normalize(
            test_data["input"], test_data["is_surname"], preserve_wildcards="preserve_wildcards" in test_data
        )
        assert result == test_data["result"], f"unexpected result {result} for {test_data['input']}"


test_merge_surname_prefixes_data = [
    {"input": ["mendoza", "y", "gutierres"], "result": ["mendoza", "y", "gutierres"]},
    {"input": ["mendoza", "de", "la", "gutierres"], "result": ["mendoza", "delagutierres"]},
    {"input": ["della", "mendoza", "gutierres"], "result": ["dellamendoza", "gutierres"]},
    {"input": ["mendoza", "gutierres", "de", "la"], "result": ["mendoza", "gutierres", "dela"]},
    {"input": ["van", "der", "leek"], "result": ["vanderleek"]},
    {"input": ["vander", "leek"], "result": ["vanderleek"]},
]


def test_merge_surname_prefixes():
    for test_data in test_merge_surname_prefixes_data:
        result = merge_surname_prefixes(test_data["input"])
        assert result == test_data["result"], f"unexpected result {result} for {test_data['input']}"


test_remove_noise_words_data = [
    {"input": ["mendoza", "y", "gutierres"], "is_surname": False, "result": ["mendoza", "gutierres"]},
    {"input": ["major", "mendoza"], "is_surname": False, "result": ["mendoza"]},
    {"input": ["major"], "is_surname": False, "result": ["major"]},
    {"input": ["sir", "smith"], "is_surname": False, "result": ["smith"]},
    {"input": ["sir", "king"], "is_surname": False, "result": ["king"]},
    {"input": ["smith", "king"], "is_surname": False, "result": ["smith"]},
    {"input": ["king", "smith"], "is_surname": False, "result": ["smith"]},
]


def test_remove_noise_words():
    for test_data in test_remove_noise_words_data:
        result = remove_noise_words(test_data["input"], test_data["is_surname"])
        assert result == test_data["result"], f"unexpected result {result} for {test_data['input']}"


test_match_name_pairs_data = [
    {
        "input": {"name_pieces": ["john", "smith"], "alt_name_pieces": ["jan", "smythe", "brown"]},
        "result": [("smith", "smythe"), ("john", "jan")],
    }
]


def test_match_name_pairs():
    for test_data in test_match_name_pairs_data:
        result = match_name_pairs(test_data["input"])
        assert result == test_data["result"], f"unexpected result {result} for {test_data['input']}"


test_levenshtein_similarity_data = [
    {"name1": "john", "name2": "jan", "result": 0.5},
    {"name1": "smith", "name2": "smyth", "result": 0.8},
]


def test_levenshtein_similarity():
    for test_data in test_levenshtein_similarity_data:
        result = levenshtein_similarity(test_data["name1"], test_data["name2"])
        assert (
            result == test_data["result"]
        ), f"unexpected result {result} for {test_data['name1']}, {test_data['name2']}"
