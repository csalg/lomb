import axios from 'axios';
import {LOGIN, REGISTER} from "../endpoints";


class AuthService {
    static login(username, password){
        return axios
            .post(LOGIN, {
                username,
                password
            })
            .then(response => {
                if (response.data.access_token)
                    localStorage.setItem('user', JSON.stringify(response.data.access_token))
                return response.data;
            })
    }
    static logout(){
        localStorage.removeItem('user')
    }

    static register(user){
        return axios.post(REGISTER, {...user}
        )
    }

    static getCurrentUser(){
        return JSON.parse(localStorage.getItem('user'))
    }

    static jwt_post(url, data){
        return axios
            .post(url,data, {headers: authHeader()})
            .then(data => {
                console.log(data)
                return data
            })
    }

    static jwt_get(url,data){
        return axios
            .get(url,{headers: authHeader()})
            .then(data => {
                console.log(data)
                return data
            })

    }
}

export function authHeader() {
    const user = JSON.parse(localStorage.getItem('user'))
    console.log('authHeader', user)

    if (user && user.accessToken)
        console.log(user)
        return { Authorization: `Bearer ${user}`}

    return {};

}

export default AuthService;
