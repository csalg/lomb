DEBUG=True
MAXIMUM_SECONDS = 150*24*60*60 # Otherwise difficult to scale.
LANGUAGE_NAMES = {
    'en': 'English',
    'de': 'German',
    'es': 'Spanish',
    'fr': 'French',
    'it': 'Italian',
    'nl': 'Dutch',
    'pl': 'Polish',
    'ru': 'Russian',
    'jp': 'Japanese',
    'zh': 'Chinese',
    'da': 'Danish'
}
LEARNING_LANGUAGES = ['en', 'de', 'es', 'fr', 'it', 'nl', 'pl', 'ru', 'da']
KNOWN_LANGUAGES = ['en', 'de', 'es', 'fr', 'it', 'nl', 'pl', 'ru', 'jp', 'zh', 'da']
MAXIMUM_EXAMPLES_PER_LEMMA = 100
MINIMUM_LEMMA_RANK = 0 # Minimum rank to count for average lemma rank count
MAXIMUM_LEMMA_RANK = 20000
TRANSLATABLE_EXTENSIONS = ['txt','epub']

MINIMUM_PASSWORD_LENGTH = 8
MAXIMUM_PASSWORD_LENGTH = 40

MINIMUM_LEARNING_LEMMA_FREQUENCY_ALLOWED_FOR_REVISION = 3

UPLOADS_FOLDER = '/uploads'

# COLLECTION NAMES
LIBRARY_CHUNKS_COLLECTION_NAME      = 'library_chunks'
LIBRARY_TEXTFILE_COLLECTION_NAME    = 'library_textfiles'
LIBRARY_FREQUENCY_LIST_COLLECTION_NAME = 'library_frequency_lists'
LIBRARY_LEMMA_RANK_COLLECTION_NAME = 'library_lemma_ranks'
VOCABULARY_LOGS_COLLECTION_NAME     = 'vocabulary_logs'
IGNORE_LEMMAS_COLLECTION_NAME       = 'vocabulary_ignore'
LEARNING_LEMMAS_COLLECTION_NAME     = 'learning_lemmas'
LEARNING_LEMMAS_EXAMPLES_CACHE = 'lemmas__learning'
EXAMPLES_CACHE = 'examples_cache'

BOOK_DRILLS_CACHE = 'book_drills'

DATAPOINTS = 'datapoints'

USERS_COLLECTION_NAME = 'users'
USER_CREDENTIALS_COLLECTION_NAME = 'user_credentials'
USER_PREFERENCES_COLLECTION_NAME = 'user_preferences'

SMART_FETCH_BATCH_SIZE = 20

# PoR prediction parameters
EMA_SMOOTHING_COEFFICIENT = 0.5
TIME_WINDOW = 24*60*60

# Max allowed time elapsed
MAX_ELAPSED = 24*30*24*60*60 # 2 years in seconds
