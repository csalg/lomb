import React, { useState } from 'react';
import {
    Form,
    Input,
    Button,
    Checkbox
} from 'antd';
import AuthService from "../../services/auth";
import User from "./models/User";
import {layout, tailLayout} from "./util";

const Register = () => {
    const [componentSize, setComponentSize] = useState('small');
    const [error, setError] = useState("")

    const onFormLayoutChange = ({ size }) => {
        setComponentSize(size);
    };

    const onFinish = values => {
        const user = new User(values.username, values.password, values.learning_languages, values.known_languages)
        console.log('Success:', JSON.stringify(user));
        AuthService.register(user).then(
            () => {
                this.props.history.push('/library');
                window.location.reload();
            },
            error => {
                console.log(error, error.response, error.response.data);
                setError(JSON.stringify(error.response.data, undefined, 2))
            }
        )
    };

    const onFinishFailed = errorInfo => {
        console.log('Failed:', errorInfo);
    };

    return (
        <div>
            <p>
                {error}
            </p>
            <Form
                layout="horizontal"
                {...layout}
                initialValues={{
                    size: componentSize,
                }}
                onValuesChange={onFormLayoutChange}
                onFinish={onFinish}
                onFinishFailed={onFinishFailed}
                size={componentSize}
            >
                <Form.Item label="Username" name='username' rules={[
                    {required:true, message: 'Username is required'}
                    ]}>
                    <Input />
                </Form.Item>

                <Form.Item label="Password" name='password' rules={
                    [
                        {required:true, message:"Please input a password"},
                        {min:8, message:'Password is too short. Must be longer than 8 characters.'},
                        {max:40, message:'Password is too long! No more than 40 characters, please.'}
                    ]
                }>
                    <Input.Password />
                </Form.Item>
                <Form.Item label="Repeat password" name='repeat password' rules={[
                    {required:true, message:'Please write your password again'},
                    ({getFieldValue}) => ({
                        validator(rule,value){
                            if (!value || getFieldValue('password') === value)
                                return Promise.resolve();
                            return Promise.reject('Does not match the password you previously entered.')
                        }
                })
                ]
                }>
                    <Input.Password />
                </Form.Item>
                <Form.Item label="Learning languages" name='learning_languages' rules={[
                    {required:true, message:'Please select a least one language you are learning.'}
                ]}>
                    <Checkbox.Group>
                    {/*<Checkbox value='dk' label='Danish'>Danish</Checkbox>*/}
                        {sourceLanguages.map(({value, label}) => <Checkbox value={value} label={label} key={value}>{label}</Checkbox> )}
                    </Checkbox.Group>
                </Form.Item>
                <Form.Item label="Known languages" name='known_languages' rules={[
                    {required:true, message:'Please select a least one language you are learning.'}
                ]}>
                    <Checkbox.Group>
                        {/*<Checkbox value='dk' label='Danish'>Danish</Checkbox>*/}
                        {supportLanguages.map(({value, label}) => <Checkbox value={value} label={label} key={value}>{label}</Checkbox> )}
                    </Checkbox.Group>
                </Form.Item>
                <Form.Item {...tailLayout}>
                    <Button type="primary" htmlType="submit">
                        Register
                    </Button>
                </Form.Item>
            </Form>
        </div>
    );
};

const sourceLanguages = [
    { label: 'Spanish', value: 'es' },
    { label: 'English', value: 'en' },
    { label: 'German', value: 'de'},
];

const supportLanguages = [
    { label: 'Spanish', value: 'es' },
    { label: 'English', value: 'en' },
    { label: 'German', value: 'de'},
    { label: 'Chinese', value: 'zh'},
];

// const SelectLanguages = () => <div>
//     <p>I am learning:</p>
//
//         <Checkbox.Group options={sourceLanguages} onChange={onChange} />
//         <br />
//         <br />
//         <p>I can speak:</p>
//         <Checkbox.Group options={supportLanguages} onChange={onChange} />
//         <br />
//     </div>

export default Register