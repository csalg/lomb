import React from "react";
import { Layout, Menu, Dropdown } from 'antd';
import Library from './Library'
import Upload from "./Upload";
import { DownOutlined } from '@ant-design/icons';
import {Link, Switch, Route, Redirect} from "react-router-dom";
const { Header, Content, Footer } = Layout;

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

const UserAreaContainer = ({match}) => (
    <Layout className="layout" style={{minHeight: '100vh'}}>
        <Header>
            <div className="logo" />
            <Menu
                theme="dark"
                mode="horizontal"
                defaultSelectedKeys={['library']}
                onChange={(e) => console.log(e)}
            >
                <Menu.Item key="library"><Link to={`${match.url}/library`}>Library</Link></Menu.Item>
                <Menu.Item key="upload"><Link to={`${match.url}/upload`}>Upload</Link></Menu.Item>
                <Menu.Item key="vocabulary"><VocabularyDropdown/></Menu.Item>
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

export default UserAreaContainer;