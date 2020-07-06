import React from "react";
import { Layout, Menu, Dropdown } from 'antd';
import Library from './Library'
import Upload from "./Upload";
import { DownOutlined } from '@ant-design/icons';
import {Link, Switch, Route, Redirect, useHistory, withRouter} from "react-router-dom";
import styled from 'styled-components';
import { LogOut } from '@styled-icons/feather/LogOut'
import AuthService from '../../services/auth'
const { Header, Content, Footer } = Layout;

const Logo = styled.div`
  font-family: Fernynda, sans-serif;
  width: 120px;
  height: 31px;
  float:left;
  color: hsla(209, 50%, 55%, 0.8);
  font-size: 3em;
`

const Right = styled.div`  
  font-family: Fernynda, sans-serif;
  float:right;
`

const LogoutIcon = styled(LogOut)`
    height: 1em;
`

const menu = (
    <Menu>
        <Menu.Item>
            <a target="_blank" rel="noopener noreferrer" href="#">
                Revise
            </a>
        </Menu.Item>
        <Menu.Item>
            <a target="_blank" rel="noopener noreferrer" href="#">
                Manage known/ignore list
            </a>
        </Menu.Item>
    </Menu>
);

const VocabularyDropdown = () =>
    <Dropdown overlay={menu}>
        <a className="ant-dropdown-link" onClick={e => e.preventDefault()}>
            Vocabulary <DownOutlined />
        </a>
    </Dropdown>

const UserAreaContainer = ({match, history}) => (
    <Layout className="layout" style={{minHeight: '100vh'}}>
        <Header>
           <Logo>
                Lomb
           </Logo>
            <Menu
                theme="dark"
                mode="horizontal"
                defaultSelectedKeys={['library']}
                onChange={(e) => console.log(e)}
            >
                <Menu.Item key="library"><Link to={`${match.url}/library`}>Library</Link></Menu.Item>
                <Menu.Item key="upload"><Link to={`${match.url}/upload`}>Upload</Link></Menu.Item>
                <Menu.Item key="revise"><Link to={`/revise`}>Revise</Link></Menu.Item>
                {/*<Menu.Item key="vocabulary"><VocabularyDropdown/></Menu.Item>*/}
                <Right>
                    <LogoutIcon onClick={_ => {
                        AuthService.logout();
                        history.push('/')
                    }}/>
                </Right>
            </Menu>
        </Header>
        <Content style={{ padding: '0 50px' }}>

            <div className="site-layout-content">
                <Switch>
                    <Route path={`${match.url}/upload`}>
                        <Upload/>
                    </Route>
                    <Route path={`${match.url}/library`}>
                        <Library/>
                    </Route>
                    <Route>
                       <Redirect to={`${match.url}/library`}/>
                    </Route>
                </Switch>

            </div>
        </Content>
        <Footer style={{ textAlign: 'center' }}>GPL License. You may do whatever you want with this software except make money off it.</Footer>
    </Layout>
);

export default withRouter(UserAreaContainer);