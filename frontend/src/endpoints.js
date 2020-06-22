export const API_URL = process.env.API_URL || 'http://localhost:5000'

export const AUTH_URL = API_URL + "/auth"
export const LOGIN = AUTH_URL + "/login"
export const REGISTER = AUTH_URL + "/register"

export const LIBRARY_URL = API_URL + "/library"
export const UPLOAD = LIBRARY_URL + "/upload"
export const ALL_TEXTS = LIBRARY_URL + "/"
