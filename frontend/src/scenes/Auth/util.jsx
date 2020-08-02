import ServerErrorMessage from "../../lib/SharedComponents/ServerErrorMessage";
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
export const AuthServerErrorMessage = props =>  <ServerErrorMessage {...props} {...tailLayout}/>
