import React from "react";
import AuthService from "../../../services/auth";
import Lemmas from "./Lemmas";
import styled from 'styled-components'
import Examples from "./Examples";
import Definition from "./Definition";
import Filter from "./Filter";
import {neutral3, neutral4} from "../../../PALETTE";
import UserPreferences from "../../../services/userPreferences";
import {BOOK_DRILL_URL, REVISE_URL} from "../../../endpoints";
import {EVENT_TYPES, LEMMAS_TO_FETCH_ON_SMART_FETCH, MINIMUM_LEMMAS_LEFT_FOR_SMART_FETCH_RELOAD} from "../../../config";


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
        this.textfileId = props.match.params.id
        this.click_event_type = EVENT_TYPES.BOOK_DRILL_CLICK
        this.scroll_event_type = EVENT_TYPES.BOOK_DRILL_SCROLL
        this.lemmasRef = React.createRef();
        this.changeLemma = this.changeLemma.bind(this)
        this.fetchTexts = this.fetchTexts.bind(this)
        this.notifyInfiniteScroll = this.notifyInfiniteScroll.bind(this)

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

    shouldComponentUpdate(nextProps, nextState, nextContext) {
        return this.state.currentExamples.length === nextState.currentExamples.length
    }

    async fetchTexts() {
        if (this.state.loading) {
            return
        }
        try {
            await this.setState({loading:true})
            const data = await AuthService.jwt_get(BOOK_DRILL_URL(this.textfileId))
            console.log(data)
            const {source_language, support_language} = data.data
            await this.setState({supportLanguage: support_language})
            const lemmas = data.data.lemmas.map(record => {
                return {
                    _id: record.lemma,
                    frequency: record.frequency,
                    sourceLanguage: source_language,
                    probability: record.probability_of_recall,
                }
            })
            const lemmasToExamples = {}
            for (let i = 0; i < lemmas.length; i++) {
                const sourceLanguage = source_language
                const lemma = data.data.lemmas[i].lemma
                const examples = data.data.lemmas[i].examples
                if (!(sourceLanguage in lemmasToExamples)) {
                    lemmasToExamples[sourceLanguage] = {}
                }
                lemmasToExamples[sourceLanguage][lemma] = examples
            }
            await this.setState({
                loading: false,
                data: data.data,
                lemmas: lemmas,
                lemmasToExamples: lemmasToExamples
            })
            console.log(this.state.lemmasToExamples)
        } catch
            (error) {
            console.log('Error fetching texts: ', error)
        }
    }

    changeLemma = (newLemma, newSourceLanguage) => {

        document.body.dispatchEvent(new CustomEvent('wordWasClicked', {
                bubbles: true,
                detail: () => ({
                    currentLemma: newLemma,
                    sourceLanguage: newSourceLanguage,
                    currentExamples: this.state.lemmasToExamples[newSourceLanguage][newLemma],
                    supportLanguage: this.state.lemmasToExamples[newSourceLanguage][newLemma][0]['support_language']
                })
            })
        )
    }

    async notifyInfiniteScroll(key){

        const amountOfLemmasBeingRevised = this.state.lemmas.length;
        if (amountOfLemmasBeingRevised < MINIMUM_LEMMAS_LEFT_FOR_SMART_FETCH_RELOAD*2){
            return
        }

        let locationInScroll = 1;
        for( let i=0; i!==this.state.lemmas.length; i++){
            const lemma_id = this.state.lemmas[i]._id
            if (lemma_id === key){
                locationInScroll = i+1
            }
        }
        const lemmasLeft = amountOfLemmasBeingRevised - locationInScroll
        if (lemmasLeft < MINIMUM_LEMMAS_LEFT_FOR_SMART_FETCH_RELOAD){
            return this.fetchTexts()
        }

    }

    render() {

        const Container = styled.div`
            display: flex;
            height: 100vh;
            width: 100vw;
          @media (max-width: 768px) {
            flex-direction: column;
          }
`
        const LemmasContainer = styled.div`
            overflow-y: scroll;
            width: 40%;
          @media (max-width: 768px) {
            width: 100%;
            height: 40vh;
          }
`
        const Sidebar = styled.div`
            width: 60%;
          @media (max-width: 768px) {
            width: 100%;
          }
`
        const SidebarSection = styled.div`
            width: 100%;
            height: 50%;
          @media (max-width: 768px) {
            height: 30vh;
          }
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
                        notifyInfiniteScroll={this.notifyInfiniteScroll}
                        scrollEventType={this.scroll_event_type}
                        clickEventType={this.click_event_type}
                        supportLanguage={this.state.supportLanguage}
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