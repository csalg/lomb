import React, {Fragment} from 'react';
import './App.css';
import 'antd/dist/antd.css'; // or 'antd/dist/antd.less'

import UserAreaContainer from "./scenes/UserArea/UserAreaContainer";
import {LoginTab, RegisterTab} from "./scenes/Auth/AuthContainer";
import {BrowserRouter, Link, Route, Switch, useHistory} from "react-router-dom";
import AuthService from './services/auth'
import {PrivateRoute} from "./services/auth-routes.lib";
import Reader from "./scenes/UserArea/Reader/Reader";

function App() {
  return (
          <BrowserRouter>
              <Switch>
                  <Route path='/login'>
                      <LoginTab/>
                  </Route>
                  <Route path='/register'>
                      <RegisterTab/>
                  </Route>
                  <PrivateRoute path='/user/reader/:type/:file' component={Reader}/>
                  <PrivateRoute path='/user' component={UserAreaContainer}/>
                  <Route><DecideWhereToGo/></Route>

              </Switch>
          </BrowserRouter>
  )
}

function DecideWhereToGo(){
    const history = useHistory()
    if (AuthService.getCurrentUser())
        history.push('/user')
    else
        history.push('/login')

    return <div>Welcome to Lomb. <Link to='/login'>Click here to login or register</Link></div>
}

export default App;
