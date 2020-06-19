import React from "react";
import { Layout, Menu, Dropdown } from 'antd';
import Library from './Library'
import Upload from "./Upload";
import { DownOutlined } from '@ant-design/icons';
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

export default () => (
    <Layout className="layout" style={{minHeight: '100vh'}}>
        <Header>
            <div className="logo" />
            <Menu theme="dark" mode="horizontal" defaultSelectedKeys={['1']}>
                <Menu.Item key="1">Library</Menu.Item>
                <Menu.Item key="2">Upload</Menu.Item>
                <Menu.Item key="3"><VocabularyDropdown/></Menu.Item>
            </Menu>
        </Header>
        <Content style={{ padding: '0 50px' }}>

            <div className="site-layout-content">
                <Upload/>

            </div>
        </Content>
        <Footer style={{ textAlign: 'center' }}>Ant Design ©2018 Created by Ant UED</Footer>
    </Layout>
);