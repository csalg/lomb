import React from 'react';
import {Layout, Tabs} from 'antd';
import Login from "./Login";
import Register from "./Register";
const { TabPane } = Tabs;
const { Header, Content, Footer } = Layout;


function callback(key) {
    console.log(key);
}

const AuthContainer = () => (
    <Layout className="auth-layout">
        <Content style={{ padding: '2em 50px' }}>
            <Tabs defaultActiveKey="1" onChange={callback}>
                <TabPane tab="Login" key="1">
                    <Login></Login>
                </TabPane>
                <TabPane tab="Register" key="2">
                    <Register></Register>
                </TabPane>
            </Tabs>
        </Content>
    </Layout>
);

export default AuthContainer