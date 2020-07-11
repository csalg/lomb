import API_URL from './api_endpoint'

export const LANGS_URL = API_URL + "/langs"

export const AUTH_URL = API_URL + "/auth"
export const LOGIN = AUTH_URL + "/login"
export const REGISTER = AUTH_URL + "/register"
export const USER = AUTH_URL + "/user"

export const LIBRARY_URL = API_URL + "/library"
export const UPLOAD = LIBRARY_URL + "/upload"
export const LIBRARY_UPLOADS = LIBRARY_URL + "/uploads"
export const ALL_TEXTS = LIBRARY_URL + "/"

export const VOCABULARY = API_URL + "/vocabulary"
export const REVISE_URL = VOCABULARY + '/revise'
export const INTERACTION_TRACKING_URL = API_URL+ '/tracking/'
