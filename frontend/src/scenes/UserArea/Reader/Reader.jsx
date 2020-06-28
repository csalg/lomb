import React from 'react'
import {authHeader} from "../../../services/auth";
import ReaderWrapper from "./components/ReaderWrapper";
import HTMLDocument from "./components/HTMLDocument";


class HTMLReader extends React.Component {
    render() {
        return (
            <ReaderWrapper component={HTMLDocument} {...this.props}/>
        )
    }
}

export default class extends React.Component {
    render() {
        switch(this.props.match.params.type){
            case 'html':
               return <HTMLReader {...this.props}/>
            default:
                return <div>Wrong filetype</div>
        }
    }
}
