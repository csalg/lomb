import AuthService from './auth'
import {LANGS_URL} from "../endpoints";

export default () => (
    AuthService.jwt_get(LANGS_URL).then(data => data.data)
)