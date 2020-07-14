import AuthService from "./auth";
import {USER_PREFERENCES_URL} from "../endpoints";

export default class UserPreferences {
    static async get(key) {
        const rawPreferences = window.localStorage.getItem('preferences');
        if (!rawPreferences) {
            // If there are no preferences in localStorage we populate the whole
            // thing from the server and call ourselves again
            const serverPreferences = await AuthService.jwt_get(USER_PREFERENCES_URL)
            window.localStorage.setItem('preferences', JSON.stringify(serverPreferences))
            return UserPreferences.get(key)
        } else {
            const preferences = JSON.parse(rawPreferences)
            if (!(key in preferences)) {
                // If the key is not in preferences we also try to get it from server
                const serverPreferences = await AuthService.jwt_get(USER_PREFERENCES_URL).then(data => data.data)
                console.log('server preferences are', serverPreferences)
                if (key in serverPreferences) {
                            UserPreferences.set(key, serverPreferences[key])
                    return UserPreferences.get(key)
                } else {
                    // Well if we can't find the key anywhere then something is wrong, so let's notify that...
                    throw new Error(`Key ${key} is not found in user preferences`)
                }
            } else {
                return preferences[key]
            }
        }
    }

    static set(key, value) {
        console.log('Setting', key, value)
        const rawPreferences = window.localStorage.getItem('preferences');
        const preferences = rawPreferences ? JSON.parse(rawPreferences) : {}
        preferences[key] = value
        window.localStorage.setItem('preferences', JSON.stringify(preferences))
    }
}