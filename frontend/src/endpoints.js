import API_URL from './api_endpoint'

export const LANGS_URL = API_URL + "/langs"

export const AUTH_URL = API_URL + "/user"
export const LOGIN = AUTH_URL + "/login"
export const REGISTER = AUTH_URL + "/register"
export const USER_PREFERENCES_URL = AUTH_URL + "/"

export const LIBRARY_URL = API_URL + "/library"
export const UPLOAD = LIBRARY_URL + "/upload"
export const LIBRARY_UPLOADS = LIBRARY_URL + "/uploads"
export const LIBRARY_TEXT = LIBRARY_URL + "/text"
export const ALL_TEXTS = LIBRARY_URL + "/"

export const LIBRARY_ADMIN = LIBRARY_URL + '/admin'
export const UPDATE_LEMMA_RANKS_URL = LIBRARY_ADMIN + '/update_lemma_ranks'
export const UPDATE_TEXT_DIFFICULTIES = LIBRARY_ADMIN + '/update_text_difficulty'

export const VOCABULARY = API_URL + "/vocabulary"
export const REVISE_URL = VOCABULARY + '/revise'
export const DELETE_URL = VOCABULARY + '/delete_word'
export const INTERACTION_TRACKING_URL = API_URL+ '/tracking/'

export const BOOK_DRILL_URL = textfileId => API_URL + "/slices/drill_book/" + textfileId
export const STATS_URL = API_URL + "/slices/stats"
export const ETL_FROM_SCRATCH_URL = API_URL + "/slices/etl_from_scratch"
export const ADD_METADATA_URL = API_URL + "/slices/add_frequency_and_support_language_to_datapoints"
export const REMOVE_IGNORED_DATASET = API_URL + "/slice/remove_ignored_datapoints"
export const GET_DATASET_URL = API_URL + "/slices/data.csv"
