import React from 'react'
import {authHeader} from "../../services/auth";

const fetch_document = (URL) => {
    const xhr = new XMLHttpRequest();

    xhr.open('GET', 'some.pdf');
    xhr.onreadystatechange = handler;
    xhr.responseType = 'blob';
    xhr.setRequestHeader('Authorization', authHeader().Authorization );
    xhr.send();

    function handler() {
        if (this.readyState === this.DONE) {
            if (this.status === 200) {
                // this.response is a Blob, because we set responseType above
                return URL.createObjectURL(this.response);
            } else {
                // eslint-disable-next-line no-throw-literal
                throw 'File not found!'
            }
        }
    }
}

class ReaderWrapper extends React.Component {
    render(){
        return (<div>
            {this.props.children}
        </div>)
    }
}

class HTMLDocument extends React.Component {

    render() {
        return (
            <div>
                <h2>{this.props.match.params.type}</h2>
                <h2>{this.props.match.params.file}</h2>
            </div>
        )
    }
}

class HTMLReader extends React.Component {
    render() {
        return (
            <ReaderWrapper>
                <HTMLDocument {...this.props} />
            </ReaderWrapper>
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
