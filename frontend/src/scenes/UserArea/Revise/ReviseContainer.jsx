
import React from "react";
import { Table } from 'antd';
import reqwest from 'reqwest';
import AuthService from "../../../services/auth";
import {ALL_TEXTS, LIBRARY_UPLOADS, REVISE_URL, USER, USER_LANGUAGES} from "../../../endpoints";
import {Link} from "react-router-dom";
import Lemmas from "./Lemmas";
import styled from 'styled-components'
import Examples from "./Examples";
import Definition from "./Definition";


class ReviseContainer extends React.Component {
    constructor(props) {
        super(props);
        this.changeLemma = this.changeLemma.bind(this)
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
        this.fetchTexts()
        this.fetchLanguages()
    }

    fetchTexts(){
        AuthService
            .jwt_get(REVISE_URL, {
                "minimum_frequency": 4,
            })
            .then(data => {
               console.log(data.data)
                const lemmas = data.data.map(record =>{
                    return {
                        _id: record.lemma,
                        sourceLanguage: record.language,
                    }})
                const lemmasToExamples = {}
                for (let i=0; i<lemmas.length; i++){
                    const sourceLanguage = data.data[i].language
                    const lemma = data.data[i].lemma
                    const examples =  data.data[i].examples
                    if (!(sourceLanguage in lemmasToExamples)){
                        lemmasToExamples[sourceLanguage] = {}
                    }
                    lemmasToExamples[sourceLanguage][lemma] = examples
                }
                this.setState({
                    loading:false,
                    data: data.data,
                    lemmas: lemmas,
                    lemmasToExamples: lemmasToExamples
                })
                console.log(this.state.lemmasToExamples)
            })
            .catch(err => console.log('Error fetching texts: ', err))
    }
    fetchLanguages(){
        AuthService
            .jwt_get(USER)
            .then(data => {
                this.setState({
                    'supportLanguage':data.data.known_languages[0],
                })
            })
    }

    changeLemma=(newLemma, newSourceLanguage) => {
        this.setState({
            currentLemma: newLemma,
            sourceLanguage: newSourceLanguage,
            currentExamples: this.state.lemmasToExamples[newSourceLanguage][newLemma],
            supportLanguage: this.state.lemmasToExamples[newSourceLanguage][newLemma][0]['support_language']
        })
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
            padding: 1rem 2rem;
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
            <Lemmas rows={this.state.lemmas} changeLemma={this.changeLemma}/>
                </LemmasContainer>
                <Sidebar>
                    <SidebarSection>
                        <Examples examples={this.state.currentExamples}/>
                    </SidebarSection>
                    <SidebarSection>
                        <Definition lemma={this.state.currentLemma} sourceLanguage={this.state.sourceLanguage} supportLanguage={this.state.supportLanguage}/>
                    </SidebarSection>
                </Sidebar>
            </Container>
        );
    }
}

export default ReviseContainer;