import React, {useEffect, useRef, useState} from 'react'
import styled from 'styled-components'

export default () => {
    return (
        <div
            key='container'
            style={{
                overflowY: 'scroll',
                margin: '1rem 2rem',
                height: '100%',
            }}
        >
            <TranslationView key='translation'/>
            <Examples key='examples'/>
        </div>
    )
}

class TranslationView extends React.Component {
    state = {
        supportText: ""
    }

    componentDidMount() {
        document.body.addEventListener('exampleWasClicked', e =>{
            this.setState({supportText: JSON.parse(e.detail())})
        })
    }

    render() {
        return (
            <div style={{
                minHeight: '5rem',
                padding: '1rem 0',
                position: 'sticky',
                top: 0,
                backgroundColor: 'ivory'
            }}>{this.state.supportText}</div>
        )
    }
}

class Examples extends React.Component {
    constructor(props) {
        super(props);
        this.state = {examples:[]}
        console.log('Examples constructor called')
        this.exampleWasClickedEvent = new CustomEvent('exampleWasClicked', {
            bubbles: true,
            detail: () => this.state.clickedExample
        })
    }

    __changeExample(clickedExample) {
        const event = new CustomEvent('exampleWasClicked', {
            bubbles: true,
            detail: () => clickedExample
        })
        document.body.dispatchEvent(event)
    }

    componentDidMount() {
        document.body.addEventListener('wordWasClicked', e => {
            this.setState({examples: e.detail().currentExamples})
        })
    }

    render() {
        console.log('Render examples')
        console.log(this.state)
        return (
            <>
                {this.state.examples.map((example, i) =>
                    <div
                        key={i}
                        style={{paddingBottom: '1rem'}}
                        id={`example-${i}`}
                        onClick={(e) => {
                            this.__changeExample(example.support_text)
                        }}>
                        {example.text}
                    </div>)}
            </>
        )
    }
}