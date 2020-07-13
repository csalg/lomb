import React, {useEffect, useRef, useState} from 'react'
import styled from 'styled-components'
import {neutral2} from "../../../PALETTE";

export default () => {
    return (
        <div
            key='container'
            style={{
                overflowY: 'scroll',
                margin: '0rem',
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
        document.body.addEventListener('exampleWasClicked', e => {
            this.setState({supportText: JSON.parse(e.detail())})
        })
    }

    render() {
        return (
            <div style={{
                minHeight: '5rem',
                padding: '1rem',
                position: 'sticky',
                top: 0,
                fontStyle: 'italic',
                backgroundColor: neutral2,
                borderBottom: '1px solid #f0f0f0',
                color: 'hsla(0,0%,0%,0.8)'
            }}>{this.state.supportText}</div>
        )
    }
}

class Examples extends React.Component {
    constructor(props) {
        super(props);
        this.state = {examples: []}
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
        this.__changeExample("\"\"")
    }

    componentWillUpdate(nextProps, nextState, nextContext) {
        this.__changeExample("\"\"")
    }

    render() {
        return (
            <div>
                {this.state.examples.map((example, i) =>
                    <div
                        key={i}
                        style={{
                            padding: '1rem',
                            marginBottom: '1rem',
                            borderBottom: '1px solid #f0f0f0',
                        }}
                        onClick={(e) => {
                            this.__changeExample(example.support_text)
                        }}>
                        {example.text}
                    </div>)}
            </div>
        )
    }
}