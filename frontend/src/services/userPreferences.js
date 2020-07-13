export default class UserPreferences {
    static get(key){
        const rawPreferences = window.localStorage.getItem('preferences');
        if (rawPreferences){
            const preferences = JSON.parse(rawPreferences)
            return preferences[key]
        }
    }

    static set(key,value){
        const rawPreferences = window.localStorage.getItem('preferences');
        const preferences = rawPreferences ? JSON.parse(rawPreferences) : {}
        preferences[key] = value
        window.localStorage.setItem('preferences', JSON.stringify(preferences))
    }
}