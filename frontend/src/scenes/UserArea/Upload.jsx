import React from "react";
import {UPLOAD} from "../../endpoints";
import AuthService, {authHeader} from "../../services/auth";
import axios from 'axios';

import {  Upload, message, Button  } from 'antd';
import {  UploadOutlined  } from '@ant-design/icons'

const props = {
    name: 'file',
    action: UPLOAD,
    headers: authHeader(),
    onChange(info) {
        if (info.file.status !== 'uploading') {
            console.log(info.file, info.fileList);
        }
        if (info.file.status === 'done') {
            message.success(`${info.file.name} file uploaded successfully`);
        } else if (info.file.status === 'error') {
            message.error(`${info.file.name} file upload failed.`);
        }
    },
};

export default () => (
    <Upload {...props}>
        <Button>
            <UploadOutlined /> Click to Upload
        </Button>
    </Upload>
);

