import React, {useEffect, useState} from "react";
import AuthService, {authHeader} from "../../../../services/auth";
import {API_URL, LIBRARY_URL} from "../../../../endpoints";
import styled from 'styled-components'



export default class extends React.Component {
    constructor() {
        super();
        this.state = {
            blob:"",
        }
        this.handler = new HTMLInteractionHandler()
        this.setNewInteractionHandler = this.setNewInteractionHandler.bind(this)
    }

    componentDidMount() {
        let url = LIBRARY_URL + '/uploads/' + this.props.match.params.file
        AuthService
            .jwt_fetch_document_as_blob(url)
            .then(data => {
                console.log(data)
                this.setState((state, props)=>{
                    return {blob:data}
                    })
            }
            )
    }

    setNewInteractionHandler (e) {
        console.log('was loaded', e)
        this.handler = new HTMLInteractionHandler(
                        this.state.blob,
                        this.props.setSupportSentence)
        this.__add_stylesheet()
    }

    __add_stylesheet(){
        const doc = document.querySelector('iframe').contentDocument;
        const cssLink = document.createElement("link");
        cssLink.href = `http://localhost:3000/reader.css`;
        console.log(cssLink.href)
        cssLink.rel = "stylesheet";
        cssLink.type = "text/css";
        doc.head.appendChild(cssLink);
        console.log(doc.head)
    }

    render() {
        return <iframe
            style={{width: '100%'}}
            src={this.state.blob}
            onLoad={this.setNewInteractionHandler}
            frameborder="0"
            className='document-frame'
        >
            {/*<link rel="stylesheet" href={`${process.env.PUBLIC_URL}/reader.css`}/>*/}
        </iframe>
    }
}

class HTMLInteractionHandler extends React.Component {
    constructor(blob, setSupportSentence) {
        super();
        if (!blob) return;
        console.log('Inside constructor ')
        this.document = document.querySelector('iframe');
        this.contentDocument = this.document.contentDocument
        this.setSupportSentence = setSupportSentence
        this.__setupClickListeners()
        this.__setup_intersection_observer()
        // this.__add_stylesheet()
    }



    __setupClickListeners(){
        const rawChunks = this.__get_chunks()
        rawChunks.forEach(sentence => sentence.addEventListener('click',
                e => {
                        const chunk = this.__process_chunk(e.target);
                        console.log(chunk)
                        // e.preventDefault()
                        this.setSupportSentence(chunk.supportText)
        }))
    }
    
    __get_chunks(){
        return this.contentDocument.querySelectorAll('span')
    }

    __process_chunk(rawChunk){
        return {
            supportText: JSON.parse(rawChunk.dataset.supportText),
            tokensToLemmas: JSON.parse(rawChunk.dataset.tokensToLemmas)
        }
    }

    __setup_intersection_observer(){

    }

}


const iframe_script = () => {
    const doc = document.querySelector('iframe')
    doc.onload = (() => {
    console.log(doc)
    console.log(doc.contentDocument.querySelectorAll('span'))
    })
}