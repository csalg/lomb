import React from 'react';
import styled from 'styled-components'

const SupportTextArea = () => {

    const Wrapper = styled.div`
        display: flex;
        justify-content: center;
        height: 20vh;
        padding: 1rem 0;
        border-bottom: thin solid black;
        overflow-y: scroll;
        `
    const ReadableWidthContainer = styled.div`
            max-width: 30rem;
            padding: 0 auto;
    `

    return (
        <Wrapper>
        <ReadableWidthContainer className="readable-width" id="support">
            <span style={{width:'30rem'}} >Some sentence</span>
        </ReadableWidthContainer>
        </Wrapper>
    )
}


export default function(props) {
    const Container = styled.div`
            display: flex;
    `
    const DocumentAndSupportText = styled.div`
            width: 60vw;
            height: 100vh;
    `
    const Definition = styled.div`
            width: 40vw;
            height: 100vh;
            border-left: thin solid black;
    `
    const Document = styled.div`
            display: flex;
            justify-content: center;
            width: 60vw;
            height: 80vh;
    `

        return (
            <Container className="container_">
                <DocumentAndSupportText>
                    <SupportTextArea/>
                    <Document className="text-area">
                        {props.children}
                    </Document>
                </DocumentAndSupportText>
                <Definition className="definition">Definition</Definition>
            </Container>
        )
    }

