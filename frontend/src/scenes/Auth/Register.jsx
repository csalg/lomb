import React, { useState } from 'react';
import {
    Form,
    Input,
    Button,
    Radio,
    Select,
    Cascader,
    DatePicker,
    InputNumber,
    TreeSelect,
    Switch,
    Checkbox
} from 'antd';
import {tailLayout} from "./Login";

const Register = () => {
    const [componentSize, setComponentSize] = useState('small');

    const onFormLayoutChange = ({ size }) => {
        setComponentSize(size);
    };

    return (
        <div>
            <Form
                labelCol={{
                    span: 4,
                }}
                wrapperCol={{
                    span: 14,
                }}
                layout="horizontal"
                initialValues={{
                    size: componentSize,
                }}
                onValuesChange={onFormLayoutChange}
                size={componentSize}
            >
                <Form.Item label="Username">
                    <Input />
                </Form.Item>

                <Form.Item label="Password">
                    <Input />
                </Form.Item>
                <Form.Item label="Repeat password">
                    <Input />
                </Form.Item>
                <Form.Item label="Select languages">
                    <SelectLanguages/>
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



function onChange(checkedValues) {
    console.log('checked = ', checkedValues);
}

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

const SelectLanguages = () => <div>
    <p>I am learning:</p>

        <Checkbox.Group options={sourceLanguages} onChange={onChange} />
        <br />
        <br />
        <p>I can speak:</p>
        <Checkbox.Group options={supportLanguages} onChange={onChange} />
        <br />
    </div>

export default Register