import React, {useState} from 'react';
import {
    Form,
    Input,
    Button,
    Checkbox
} from 'antd';
import AuthService from "../../services/auth";
import User from "./models/User";
import {useHistory} from "react-router-dom";
import parseErrorMessage from "../../services/parseErrorMessage";
import {AuthServerErrorMessage, layout, tailLayout} from "./util";
import {KNOWN_LANGUAGES, LANGUAGE_NAMES, LEARNING_LANGUAGES} from "../../services/languages";

const Register = () => {
    const history = useHistory()
    const [componentSize, setComponentSize] = useState('small');
    const [error, setError] = useState("")

    const onFormLayoutChange = ({size}) => {
        setComponentSize(size);
    };

    const onFinish = values => {
        const user = new User(values.username, values.password, values.learning_languages, values.known_languages)
        AuthService.register(user).then(
            () => {
                history.push('/user');
                window.location.reload();
            })
            .catch(error => {
                    setError(parseErrorMessage(error))
                    }
            )
    };

    const onFinishFailed = errorInfo => {
       setError(errorInfo)
    };

    return (
        <div>
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
                <AuthServerErrorMessage error={error}/>
                <Form.Item label="Username" name='username' rules={[
                    {required: true, message: 'Username is required'}
                ]}>
                    <Input/>
                </Form.Item>

                <Form.Item label="Password" name='password' rules={
                    [
                        {required: true, message: "Please input a password"},
                        {min: 8, message: 'Password is too short. Must be longer than 8 characters.'},
                        {max: 40, message: 'Password is too long! No more than 40 characters, please.'}
                    ]
                }>
                    <Input.Password/>
                </Form.Item>
                <Form.Item label="Repeat password" name='repeat password' rules={[
                    {required: true, message: 'Please write your password again'},
                    ({getFieldValue}) => ({
                        validator(rule, value) {
                            if (!value || getFieldValue('password') === value)
                                return Promise.resolve();
                            return Promise.reject('Does not match the password you previously entered.')
                        }
                    })
                ]
                }>
                    <Input.Password/>
                </Form.Item>
                <Form.Item label="Learning languages" name='learning_languages' rules={[
                    {required: true, message: 'Please select a least one language you are learning.'}
                ]}>
                    <Checkbox.Group>
                        {/*<Checkbox value='dk' label='Danish'>Danish</Checkbox>*/}
                        {sourceLanguages.map(({value, label}) => <Checkbox value={value} label={label}
                                                                           key={value}>{label}</Checkbox>)}
                    </Checkbox.Group>
                </Form.Item>
                <Form.Item label="Known languages" name='known_languages' rules={[
                    {required: true, message: 'Please select a least one language you are learning.'}
                ]}>
                    <Checkbox.Group>
                        {/*<Checkbox value='dk' label='Danish'>Danish</Checkbox>*/}
                        {supportLanguages.map(({value, label}) => <Checkbox value={value} label={label}
                                                                            key={value}>{label}</Checkbox>)}
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

const sourceLanguages = LEARNING_LANGUAGES.map(language => ({label: LANGUAGE_NAMES[language], value: language}))
const supportLanguages = KNOWN_LANGUAGES.map(language => ({label: LANGUAGE_NAMES[language], value: language}))

export default Register