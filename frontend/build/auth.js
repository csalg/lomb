class AuthService {
    static jwtBearerToken() {
        const user = JSON.parse(localStorage.getItem('user'))
        if (user)
            return `Bearer ${user}`
        return "";
    }



    static async __jwtWithMethod(url, data, method) {
        const response = await fetch(url,
            {
                method: method,
                mode: 'cors',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': AuthService.jwtBearerToken()
                },
                body: JSON.stringify(data)
            })
        return response
    }

    static async jwtPost(url, data) {
        return AuthService.__jwtWithMethod(url,data,'POST')
    }

    static async jwtGet(url, data){
        return AuthService.__jwtWithMethod(url,data,'GET')
    }

}
