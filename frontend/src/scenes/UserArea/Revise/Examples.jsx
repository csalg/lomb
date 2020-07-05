import React from 'react'
import styled from 'styled-components'

export default (props) => {
    const ExamplesContainer = styled.div`
        overflow-y: scroll;
        padding: 1rem 2rem;
   `

    const Example = styled.div`
        padding-bottom: 1rem;
        `

    const TranslationViewer = styled.div`
        min-height: 5rem;
        padding: 1rem 0;
        position: sticky;
        top:0;
        background-color: ivory;
        `
    return <ExamplesContainer>
        <TranslationViewer/>
        {props.examples.map(example => <Example>{example.text}</Example>)}
    </ExamplesContainer>
}