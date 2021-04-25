import React, {Fragment} from 'react';
import './App.css';
import 'antd/dist/antd.css'; // or 'antd/dist/antd.less'

import UserAreaContainer from "./scenes/UserArea/UserAreaContainer";
import {LoginTab, RegisterTab} from "./scenes/Auth/AuthContainer";
import {BrowserRouter, Link, Route, Switch, useHistory} from "react-router-dom";
import AuthService from './services/auth'
import {PrivateRoute} from "./services/Permissions";
import ReviseContainer from "./scenes/UserArea/Revise/ReviseContainer";
import {ToastContainer} from "react-toastify";
import 'react-toastify/dist/ReactToastify.css';
import DrillBook from "./scenes/UserArea/Revise/DrillBook";

function App() {
  return (
          <BrowserRouter>
              <ToastContainer
                  position="top-right"
                  autoClose={5000}
                  hideProgressBar={false}
                  newestOnTop={false}
                  closeOnClick
                  rtl={false}
                  pauseOnFocusLoss
                  draggable
                  pauseOnHover
              />
              {/* Same as */}
              <ToastContainer />
              <Switch>
                  <Route path='/login'>
                      <LoginTab/>
                  </Route>
                  <Route path='/register'>
                      <RegisterTab/>
                  </Route>
                  <PrivateRoute path='/revise' component={ReviseContainer}/>
                  <PrivateRoute path='/user' component={UserAreaContainer}/>
                  <PrivateRoute exact path="/drill/:id"  component={DrillBook}/>
                  <Route><DecideWhereToGo/></Route>

              </Switch>
          </BrowserRouter>
  )
}

function DecideWhereToGo(){
    const history = useHistory()
    if (AuthService.getCurrentUser())
        history.push('/user/')
    else
        history.push('/login')

    return <div>Welcome to Lomb. <Link to='/login'>Click here to login or register</Link></div>
}

export default App;
