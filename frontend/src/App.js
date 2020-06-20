import React, {Fragment} from 'react';
import './App.css';
import 'antd/dist/antd.css'; // or 'antd/dist/antd.less'

import LibraryContainer from "./scenes/UserArea/UserAreaContainer";
import UserAreaContainer from "./scenes/UserArea/UserAreaContainer";
import AuthContainer from "./scenes/Auth/AuthContainer";
import {BrowserRouter, Link, Route, Switch} from "react-router-dom";


function App() {
  return (
      <Fragment>
          <BrowserRouter>
              <Switch>
                  <Route path='/login'>
                      <AuthContainer/>
                  </Route>
                  <Route path='/library'>
                      <LibraryContainer/>
                  </Route>
                  <Route>
                      <Home/>
                  </Route>

              </Switch>
          </BrowserRouter>
      </Fragment>
  )
}

function Home(){
    return <div>Welcome to Lomb. <Link to='/login'>Click here to login or register</Link></div>
}

export default App;
