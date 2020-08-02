import bson
import pytest

from config import MAXIMUM_EXAMPLES_PER_TEXT
from services.library.domain.entities import Textfile, IndexEntry, LemmaRank


def test_Textfile():
    params = {
        '_id': bson.ObjectId(),
        'title': 'Some title',
        'source_language': 'en',
        'support_language': 'de',
        'filename': 'somefile.html',
    }

    # Sanity check
    textfile = Textfile(*params.values())

    # Can't create Textfile with unsupported languages
    with pytest.raises(ValueError, match=r".*not supported.*"):
        params['source_language'] = "xyz123"
        textfile = Textfile(*params.values())

    with pytest.raises(ValueError, match=r".*not supported.*"):
        params['source_language'] = "en"
        params['support_language'] = "xyz123"
        textfile = Textfile(*params.values())
    params['support_language'] = 'en'

    # Can only add permissions in accepted permissions.
    with pytest.raises(ValueError, match=r".*permission.*"):
        textfile= Textfile(*params.values(), permission='unsupported_permission_type')

def test_IndexEntry():

    # Sanity check
    params = {
        'lemma': 'run',
        'frequency': 20,
    }
    entry = IndexEntry(*params.values())

    # This should be picked up by the enforce-typing library decorator
    with pytest.raises(TypeError):
        params['frequency'] = 0.1
        entry = IndexEntry(*params.values())

    # Frequency must be a non-zero positive integer.
    with pytest.raises(ValueError, match=r".non-zero positive.*"):
        params['frequency'] = 0
        entry = IndexEntry(*params.values())


def test_LemmaRank():

    # Sanity check
    params = {
        'lemma': 'run',
        "language": 'en',
        'frequency': 20,
        "rank": 100
    }
    entry = LemmaRank(*params.values())

    # Language must be in LEARNING_LANGUAGES
    with pytest.raises(ValueError, match=r".*Language.*"):
        params['language'] = 'xyz123'
        entry = LemmaRank(*params.values())

    # Frequency must be a non-zero positive integer.
    with pytest.raises(ValueError, match=r".frequency.*non-zero positive.*"):
        params['language'] = 'en'
        params['frequency'] = 0
        entry = LemmaRank(*params.values())

    # Rank must be non-zero positive integer.
    with pytest.raises(ValueError, match=r".rank.*non-zero positive.*"):
        params['frequency'] = 10
        params['rank'] = 0
        entry = LemmaRank(*params.values())
