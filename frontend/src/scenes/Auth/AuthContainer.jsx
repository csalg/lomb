import React from 'react';
import {Layout, Tabs} from 'antd';
import Login from "./Login";
import Register from "./Register";
const { TabPane } = Tabs;
const { Content } = Layout;


function callback(key) {
    console.log(key);
}

const AuthContainer = tab_number => () => {
    return (
    <Layout className="auth-layout" style={{minHeight: '100vh'}}>
        <Content style={{ padding: '2em 50px' }}>
            <Tabs defaultActiveKey={tab_number} onChange={callback}>
                <TabPane tab="Login" key="login">
                    <Login/>
                </TabPane>
                <TabPane tab="Register" key="register">
                    <Register/>
                </TabPane>
            </Tabs>
        </Content>
    </Layout>
    )
};

export const LoginTab = AuthContainer("login")
export const RegisterTab = AuthContainer("register")
