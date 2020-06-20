import axios from 'axios';
import {API_URL, LOGIN, REGISTER} from "../endpoints";


class AuthService {

    login(username, password){
        return axios
            .post(LOGIN, {
                username,
                password
            })
            .then(response => {
                if (response.data.accessToken) {
                    localStorage.setItem('user', JSON.stringify(response.data))
                }
                return response.data;
            })
    }

    logout(){
        localStorage.removeItem('user')
    }

    register(user){
        return axios.post(REGISTER, {...user}
        )
    }

    getCurrentUser(){
        return JSON.parse(localStorage.getItem('user'))
    }
}

export default new AuthService();
