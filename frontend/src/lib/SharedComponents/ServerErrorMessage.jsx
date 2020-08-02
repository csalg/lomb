import {Alert, Form} from "antd";
import React from "react";


export default props => {
    const { error } = props
    if (error) {
        return (
            <Form.Item {...props}>
                <Alert
                    description={error}
                    type="error"
                    showIcon
                />
            </Form.Item>)
    }
    return <div/>
}


