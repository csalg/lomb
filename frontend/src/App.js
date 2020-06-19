import React from 'react';
import './App.css';
import 'antd/dist/antd.css'; // or 'antd/dist/antd.less'

import LibraryContainer from "./scenes/UserArea/UserAreaContainer";
import UserAreaContainer from "./scenes/UserArea/UserAreaContainer";
import AuthContainer from "./scenes/Auth/AuthContainer";


function App() {
  return <AuthContainer/>
}

export default App;
