import React from "react";
import { Upload, message } from 'antd';
import { InboxOutlined } from '@ant-design/icons';

const { Dragger } = Upload;

const props = {
    name: 'file',
    multiple: true,
    action: 'https://www.mocky.io/v2/5cc8019d300000980a055e76',
    onChange(info) {
        const { status } = info.file;
        if (status !== 'uploading') {
            console.log(info.file, info.fileList);
        }
        if (status === 'done') {
            message.success(`${info.file.name} file uploaded successfully.`);
        } else if (status === 'error') {
            message.error(`${info.file.name} file upload failed.`);
        }
    },
};

export default () => (
    <Dragger {...props}>
        <p className="ant-upload-drag-icon">
            <InboxOutlined />
        </p>
        <p className="ant-upload-text">Click or drag file(s) to upload</p>
        <div style={{display:'flex', justifyContent:'center'}}>
        <p className="ant-upload-hint" style={{maxWidth:'24rem', textAlign:'left'}}>
Only .html and .epub files are supported.
Files must have already been pre-processed.
Files which are not pre-processed will be rejected.
        </p>
        </div>

    </Dragger>
);