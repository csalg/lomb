import React, {useState} from 'react';
import 'antd/dist/antd.css'; // or 'antd/dist/antd.less'
import {Form, Input, Button, Checkbox, Alert} from 'antd';
import AuthService from '../../services/auth.js'
import {layout, ServerErrorMessage, tailLayout} from "./util";
import {useHistory} from 'react-router-dom'
import isBoolean from "validator/es/lib/isBoolean";
import parseErrorMessage from "../../services/parseErrorMessage";

const Login = () => {

    const history = useHistory()
    const [error, setError] = useState("")

    const onFinish = values => {
        AuthService
            .login(values.username, values.password)
            .then(
            () => {
                history.push('/user');
                window.location.reload();
            })
            .catch(
            error => {
                setError(parseErrorMessage(error));
            }
        )
    };

    const onFinishFailed = errorInfo => {
        console.log('Failed:', errorInfo);
    };

    return (
        <Form
            {...layout}
            name="basic"
            initialValues={{
                remember: true,
            }}
            onFinish={onFinish}
            onFinishFailed={onFinishFailed}
        >
            <ServerErrorMessage error={error}/>

            <Form.Item
                label="Username"
                name="username"
                rules={[
                    {
                        required: true,
                        message: 'Please input your username!',
                    },
                ]}
            >
                <Input/>
            </Form.Item>

            <Form.Item
                label="Password"
                name="password"
                rules={[
                    {
                        required: true,
                        message: 'Please input your password!',
                    },
                ]}
            >
                <Input.Password/>
            </Form.Item>

            <Form.Item {...tailLayout} name="remember" valuePropName="checked">
                <Checkbox>Remember me</Checkbox>
            </Form.Item>

            <Form.Item {...tailLayout}>
                <Button type="primary" htmlType="submit">
                    Submit
                </Button>
            </Form.Item>
        </Form>
    );
};

export default Login;
