import React, {useState} from 'react';
import 'antd/dist/antd.css'; // or 'antd/dist/antd.less'
import { Form, Input, Button, Checkbox } from 'antd';
import AuthService from '../../services/auth.js'
import {layout, tailLayout} from "./util";
import {useHistory} from 'react-router-dom'

const Login = () => {

    const history = useHistory()
    const [error, setError] = useState("")

    const onFinish = values => {
    AuthService.login(values.username, values.password).then(
        () => {
            history.push('/library');
            window.location.reload();
        },
        error => {
            if (error.response)
                setError(error.response.data.error);
            setError('Could not connect to backend')
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
          <p>
              {error}
          </p>
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
          <Input />
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
          <Input.Password />
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
