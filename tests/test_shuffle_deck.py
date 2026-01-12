from algorithms_files.shuffle_deck import shuffle_deck

def test_shuffle_deck_length():
    deck = shuffle_deck()
    assert len(deck) == 52

def test_shuffle_deck_unique():
    deck = shuffle_deck()
    assert len(set(deck)) == 52

def test_shuffle_deck_contains_cards():
    deck = shuffle_deck()
    assert "A♥" in deck
    assert "2♠" in deck
