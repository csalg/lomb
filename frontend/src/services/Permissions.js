import React from 'react';
import {Route, Redirect} from 'react-router-dom';
import AuthService from './auth'
import jwt_decode from 'jwt-decode'


export const PrivateRoute = (props) => {
    const condition = AuthService.getCurrentUser()
    const address = '/login'
    return ConditionalRoute(condition, address, props)
}


export const AdminRoute = (props) => {
    const condition = isAdmin()
    const address = '/'
    return ConditionalRoute(condition, address, props)
}

const ConditionalRoute = (condition, address, {component: Component, ...rest}) => {
    return (
        // Show the component only when the user is logged in
        // Otherwise, redirect the user to /signin page
        <Route {...rest} render={props => (
            condition ?
                <Component {...props} />
                : <Redirect to={address}/>
        )}/>
    );
};

const isAdmin = () => {
    const decoded_token = retrieveAndDecodeToken()
    return decoded_token['role'] === 'admin'
}

const isSameUser = username => {
    const decoded_token = retrieveAndDecodeToken()
    return decoded_token['username'] === username
}

const retrieveAndDecodeToken = () => {
    const token = window.localStorage.getItem('user');
    if (token)
        return jwt_decode(JSON.parse(token))['identity']
    throw Error('Could not retrieve token')
}

export const AdminOnlyContainer = props => isAdmin() ? props.children : <></>

export const AdminOrSameUsernameContainer = props => {
    const {username} = props;
    const shouldDisplayChildren = isAdmin() || isSameUser(username)
    return shouldDisplayChildren ? props.children : <></>
}

