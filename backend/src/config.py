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
MAXIMUM_EXAMPLES_PER_LEMMA = 35
MINIMUM_LEMMA_RANK = 0 # Minimum rank to count for average lemma rank count
MAXIMUM_LEMMA_RANK = 20000
TRANSLATABLE_EXTENSIONS = ['txt','epub']

MINIMUM_PASSWORD_LENGTH = 8
MAXIMUM_PASSWORD_LENGTH = 40

MINIMUM_LEARNING_LEMMA_FREQUENCY_ALLOWED_FOR_REVISION = 3

UPLOADS_FOLDER = '/uploads'
SMART_FETCH_BATCH_SIZE = 20

# Memory tracing algorithm parameters
EMA_SMOOTHING_COEFFICIENT = 0.5
TIME_WINDOW = 24*60*60

# Max time elapsed: elapsed values which are
# greater than this will be trunctated.
MAX_ELAPSED = 24*30*24*60*60 # 2 years in seconds

########################
#   COLLECTION NAMES   #
########################

# Tracking
TRACKING_LOGS                           = 'vocabulary_logs'
IGNORED_LEMMAS_SET                      = 'vocabulary_ignore'
LEARNING_LEMMAS_SET                     = 'learning_lemmas'

# Examples
CHUNKS_COLLECTION                       = 'library_chunks'
EXAMPLES_CACHE                          = 'examples_cache'
BOOK_DRILLS_CACHE                       = 'book_drills'

# Memory tracing
DATAPOINTS                              = 'datapoints' # deprecated
DATA_INTERPRETATIONS                    = 'dataset_interpretations'
DATA_CURRENT_FEATURES                   = 'dataset_current_features'
DATA_PAST_DATAPOINTS                    = 'dataset_past_datapoints'

# Users
USERS_COLLECTION_NAME                   = 'users'
USER_CREDENTIALS_COLLECTION_NAME        = 'user_credentials'
USER_PREFERENCES_COLLECTION_NAME        = 'user_preferences'

# Texts
TEXTFILE_COLLECTION                     = 'library_textfiles'

# Deprecated
EXAMPLES_CACHE_DEPRECATED                           = 'lemmas__learning'
LIBRARY_FREQUENCY_LIST_COLLECTION_NAME_DEPRECATED   = 'library_frequency_lists'
LIBRARY_LEMMA_RANK_COLLECTION_NAME_DEPRECATED       = 'library_lemma_ranks'
