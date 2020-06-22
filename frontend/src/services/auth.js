import axios from 'axios';
import {LOGIN, REGISTER} from "../endpoints";


class AuthService {

    login(username, password){
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
