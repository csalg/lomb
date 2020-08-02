import React, {useState} from 'react';
import 'antd/dist/antd.css';
import {
    Form,
    Select,
    Input,
    Radio,
    Button, Alert,
} from 'antd';
import Tags from './Tags'
import {UPLOAD} from "../../../endpoints";
import AuthService from "../../../services/auth";
import ServerErrorMessage from '../../../lib/SharedComponents/ServerErrorMessage'
import parseErrorMessage from "../../../services/parseErrorMessage";
import {toast} from "react-toastify";
import {useHistory} from 'react-router-dom'
import {KNOWN_LANGUAGES, LANGUAGE_NAMES, LEARNING_LANGUAGES} from "../../../services/languages";

const {Option} = Select;
const formItemLayout = {
    labelCol: {
        span: 6,
    },
    wrapperCol: {
        span: 14,
    },
};

const normFile = e => {
    console.log('Upload event:', e);

    if (Array.isArray(e)) {
        return e;
    }

    return e && e.fileList;
};

export default () => {
    const [err, setError] = useState("")
    const history = useHistory()

    const onFinish = values => {
        const data = new FormData()
        Object.entries(values).forEach(entry => {
            let [key, value] = entry
            if (key === 'tags' && !value){
                value = []
            }
            data.append(key, value)
        })
        AuthService
            .jwt_post(UPLOAD, data)
            .then(response => {
                toast(response.data)
                history.push('/user/library')
            })
            .catch(e => {
                console.log(e.response);
                setError(parseErrorMessage(e));
            })
    };

    const [form] = Form.useForm();

    const onTagsChange = tags => {
        form.setFieldsValue({tags: tags})
    }

    const onFileUploaded = event => {
        const file = event.target.files[0]
        form.setFieldsValue({file: file})
    }

    return (
        <Form
            style={{margin: '1em 0'}}
            name="validate_other"
            {...formItemLayout}
            onFinish={onFinish}
            form={form}
            initialValues={{
                'input-number': 3,
                'checkbox-group': ['A', 'B'],
                rate: 3.5,
            }}
        >

            <Form.Item
                name="title"
                style={{marginBottom: '1em'}}
                label="Title"
                help={'What is this text called?'}
                hasFeedback
                rules={[
                    {
                        required: true,
                        message: 'Please provide a title for the text.',
                    },
                ]}
            >
                <Input/>
            </Form.Item>

            <Form.Item
                style={{marginBottom: '1em'}}
                name="source_language"
                label="Language"
                help={'In which language is the text written?'}
                hasFeedback
                rules={[
                    {
                        required: true,
                        message: 'We need to know the language in which the text is written.',
                    },
                ]}
            >
                <Select placeholder="Please select a language">
                    {
                        LEARNING_LANGUAGES.map(language => <Option value={language}>{LANGUAGE_NAMES[language]}</Option>)
                    }
                </Select>
            </Form.Item>
            <Form.Item
                style={{marginBottom: '1em'}}
                name="support_language"
                label="Support language"
                help={'What language should we use for definitions and translations? Can be blank for native texts.'}
            >
                <Select placeholder="Please select a language">
                    {
                        KNOWN_LANGUAGES.map(language => <Option value={language}>{LANGUAGE_NAMES[language]}</Option>)
                    }

                </Select>
            </Form.Item>
            <Form.Item
                style={{marginBottom: '1em'}}
                name="tags"
                label="Tags"
                help={'You may optionally write some tags to make the text easier to find'}
            >
                <Tags onChange={onTagsChange}/>

            </Form.Item>


            <Form.Item
                style={{marginBottom: '1em'}}
                name="file"
                label="File"
                valuePropName="fileList"
                getValueFromEvent={normFile}
                rules={[
                    {
                        required: true,
                        message: 'Please upload a file.',
                    },
                ]}
            >
                <Input type={'file'} onChange={onFileUploaded}/>
            </Form.Item>

            <Form.Item
                style={{marginBottom: '1em'}}
                name="permission"
                label="Permission"
                help={'Who should be allowed to read the file?'}
                rules={[
                    {
                        required: true,
                        message: 'Please tell us who should be allowed access to the file.',
                    },
                ]}
                hasFeedback
            >
                <Radio.Group>
                    <Radio value="public">Public (Everyone can read this text)</Radio>
                    <Radio value="private">Private (Only I can read this text)</Radio>
                </Radio.Group>

            </Form.Item>

            <UploadServerErrorMessage error={err}/>
            <Form.Item
                wrapperCol={{
                    span: 12,
                    offset: 6,
                }}
            >
                <Button type="primary" htmlType="submit">
                    Submit
                </Button>
                <Button type="primary" onClick={_ => {
                    history.push('/user/library');
                    toast('Toast');

                }}>
                    Toast
                </Button>
            </Form.Item>
        </Form>
    );
};


export const tailLayout = {
    wrapperCol: {
        offset: 6,
        span: 14,
    },
};

const UploadServerErrorMessage = props => <ServerErrorMessage {...props} {...tailLayout}/>