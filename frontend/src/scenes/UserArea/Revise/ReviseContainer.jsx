import React from "react";
import {Table} from 'antd';
import reqwest from 'reqwest';
import AuthService from "../../../services/auth";
import {ALL_TEXTS, LIBRARY_UPLOADS, REVISE_URL, USER, USER_LANGUAGES} from "../../../endpoints";
import {Link} from "react-router-dom";
import Lemmas from "./Lemmas";
import styled from 'styled-components'
import Examples from "./Examples";
import Definition from "./Definition";
import Filter from "./Filter";
import {neutral2, neutral3, neutral4} from "../../../PALETTE";
import UserPreferences from "../../../services/userPreferences";


const PaddedContainer = styled.div`
        padding: 1rem 2rem;
        `

const Header = styled(PaddedContainer)`
          background-color: ${neutral3};
          margin-bottom: .5em;
            color: rgba(0,0,0,.85);
            font-weight: 500;
            font-size: 20px;
            line-height: 1.4;
            border-bottom: thin solid ${neutral4};
            `

class ReviseContainer extends React.Component {
    constructor(props) {
        super(props);
        this.lemmasRef = React.createRef();
        this.changeLemma = this.changeLemma.bind(this)

        this.wordWasClickedEvent = new CustomEvent('wordWasClicked', {
            bubbles: true,
            detail: () => this.state
        })
    }

    state = {
        currentLemma: "",
        currentExamples: [],
        sourceLanguage: 'en',
        supportLanguage: 'en',
        lemmas: [],
        lemmasToExamples: {},
        loading: false,
    };

    componentDidMount() {
        if (this.state.lemmas.length === 0) {
            this.fetchTexts()
        }

    }
    //
    // shouldComponentUpdate(nextProps, nextState, nextContext) {
    //     return this.state.lemmas === ""
    // }


    fetchTexts() {
        UserPreferences.get('revision__minimum_frequency')
            .then(minimum_frequency =>
                AuthService
                    .jwt_post(REVISE_URL, {
                        "minimum_frequency": minimum_frequency,
                    }))
            .then(data => {
                const lemmas = data.data.map(record => {
                    return {
                        _id: record.lemma,
                        sourceLanguage: record.language,
                        frequency: record.examples.length,
                    }
                })
                const lemmasToExamples = {}
                for (let i = 0; i < lemmas.length; i++) {
                    const sourceLanguage = data.data[i].language
                    const lemma = data.data[i].lemma
                    const examples = data.data[i].examples
                    if (!(sourceLanguage in lemmasToExamples)) {
                        lemmasToExamples[sourceLanguage] = {}
                    }
                    lemmasToExamples[sourceLanguage][lemma] = examples
                }
                this.setState({
                    loading: false,
                    data: data.data,
                    lemmas: lemmas,
                    lemmasToExamples: lemmasToExamples
                })
                console.log(this.state.lemmasToExamples)
            })
            .catch(err => console.log('Error fetching texts: ', err))
    }

    changeLemma = (newLemma, newSourceLanguage) => {
        this.setState({
                currentLemma: newLemma,
                sourceLanguage: newSourceLanguage,
                currentExamples: this.state.lemmasToExamples[newSourceLanguage][newLemma],
                supportLanguage: this.state.lemmasToExamples[newSourceLanguage][newLemma][0]['support_language']
            },
            () => document.body.dispatchEvent(this.wordWasClickedEvent)
        )
    }

    render() {

        const Container = styled.div`
            display: flex;
            height: 100vh;
            width: 100vw;
`
        const LemmasContainer = styled.div`
            overflow-y: scroll;
            width: 40%;
`
        const Sidebar = styled.div`
            width: 60%;
`
        const SidebarSection = styled.div`
            width: 100%;
            height: 50%;
`


        return (
            <Container>
                <LemmasContainer>

                    <Header>
                        Revision Items
                    </Header>
                    <Filter style={{marginBottom: '16px'}} fetchTexts={this.fetchTexts}/>
                    <Lemmas
                        key="lemmas"
                        rows={this.state.lemmas}
                        changeLemma={this.changeLemma}
                        ref={this.lemmasRef}
                    />
                </LemmasContainer>
                <Sidebar>
                    <SidebarSection>
                        <Examples key={"examples"}/>
                    </SidebarSection>
                    <SidebarSection>
                        <Definition key={"definition"}/>
                    </SidebarSection>
                </Sidebar>
            </Container>
        );
    }
}

const Info = () => (
    <>
        <Header>How to Revise</Header>
        <PaddedContainer>
            <p>The following words are collected from your reading sessions and ordered with the ones that
                the
                program predicts you will forget earliest first. It is recommended that you revise until
                the <i>probability
                    of recall (PoR) </i>
                is 50% or higher. </p>
            <p>If there are too many words to revise, feel free to filter out the least frequent ones using
                the minimum frequency slider below.
            </p>
            <p>The way to revise is very simple:</p>
            <ul>
                <li>Read through the list and click on any words you don't know.
                    A dictionary entry and lots of examples will appear.
                </li>
                <li>Work through the definition and the examples (possibly copying some of them if the word
                    is
                    very new and unfamiliar).
                </li>
                <li>Words which are not clicked are assumed to be known (they will turn blue once they are
                    no
                    longer in view).
                </li>
            </ul>
        </PaddedContainer>
    </>
)


export default ReviseContainer;