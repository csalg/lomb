import React, {useState} from 'react'
import styled from 'styled-components'

export default (props) => {

    const [supportText, setSupportText] = useState("")

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
    if (props.examples.length > 0) {
    return <ExamplesContainer>
        <TranslationViewer>{supportText}</TranslationViewer>
        {props.examples.map(example =>
            <Example onClick={() => setSupportText(JSON.parse(example.support_text))}>
                {example.text}
            </Example>)}
    </ExamplesContainer>
    }
    return <></>
}