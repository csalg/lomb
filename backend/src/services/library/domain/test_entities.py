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

    #
    # # Chunks array must be non-empty
    # with pytest.raises(ValueError, match=r".*chunks array is empty.*"):
    #     params['chunks'] = []
    #     entry = IndexEntry(*params.values())
    #
    # # Frequency cannot be less than the length of the chunks array
    # with pytest.raises(ValueError, match=r".*Frequency.*"):
    #     params['chunks'] = [bson.ObjectId(), bson.ObjectId()]
    #     params['frequency'] = 1
    #     entry = IndexEntry(*params.values())
    #
    # params['chunks'] = [bson.ObjectId()]
    # params['frequency'] = 10
    # entry = IndexEntry(*params.values())
    #
    # # A chunks array with more than MAXIMUM_EXAMPLES_PER_TEXT chunks will be truncated.
    # params['chunks'] = [bson.ObjectId() for i in range(2*MAXIMUM_EXAMPLES_PER_TEXT)]
    # params['frequency'] = len(params['chunks'])
    # entry = IndexEntry(*params.values())
    # assert len(entry.chunks) == MAXIMUM_EXAMPLES_PER_TEXT

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
