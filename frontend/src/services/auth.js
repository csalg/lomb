import axios from 'axios';
import {LOGIN, REGISTER} from "../endpoints";


class AuthService {
    static login(username, password) {
        return axios
            .post(LOGIN, {
                username,
                password
            })
            .then(AuthService.__saveAccessTokenInLocalStorage)
    }

    static logout() {
        localStorage.removeItem('user')
    }

    static register(user) {
        return axios
            .post(REGISTER, {...user})
            .then(AuthService.__saveAccessTokenInLocalStorage)
    }

    static __saveAccessTokenInLocalStorage = response => {
        if (response.data.access_token)
            localStorage.setItem('user', JSON.stringify(response.data.access_token))
        return response.data;
    }

    static getCurrentUser() {
        return JSON.parse(localStorage.getItem('user'))
    }

    static jwt_post(url, data) {
        return axios
            .post(url, data, {headers: authHeader()})
    }

    static jwt_get(url, data) {
        return axios
            .get(url, {headers: authHeader()})
    }

    static jwt_delete(url, data) {
        return axios
            .delete(url, {headers: authHeader()})
    }

    static jwt_fetch_document_as_blob = (url) => {
        const xhr = new XMLHttpRequest();
        return new Promise((resolve, reject) => {
            xhr.responseType = 'blob';
            xhr.onreadystatechange = function () {
                if (this.readyState === this.DONE) {
                    if (this.status === 200) {
                        resolve(URL.createObjectURL(this.response))
                    } else {
                        reject(xhr);
                    }
                }
            }
            xhr.open('GET', url);
            xhr.setRequestHeader('Authorization', authHeader().Authorization);
            xhr.send();
        });
    }
}

export function authHeader() {
    const user = JSON.parse(localStorage.getItem('user'))
    if (user)
        return {Authorization: `Bearer ${user}`}
    return {};

}

export default AuthService;
