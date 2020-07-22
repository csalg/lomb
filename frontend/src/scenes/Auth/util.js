import {Alert, Form} from "antd";
import React from "react";

export const layout = {
    labelCol: {
        span: 8,
    },
    wrapperCol: {
        span: 16,
    },
};
export const tailLayout = {
    wrapperCol: {
        offset: 8,
        span: 16,
    },
};

export const ServerErrorMessage = ({error}) => {
    if (error) {
        return (
            <Form.Item {...tailLayout}>
                <Alert
                    description={error}
                    type="error"
                    showIcon
                />
            </Form.Item>)
    }
    return <div/>
}


