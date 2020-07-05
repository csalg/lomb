
import React from "react";
import { Table } from 'antd';
import reqwest from 'reqwest';
import AuthService from "../../../services/auth";
import {ALL_TEXTS, LIBRARY_UPLOADS, REVISE_URL} from "../../../endpoints";
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
        currentLemma: "a lemma",
        currentExamples: [],
        lemmas: [],
        lemmasToExamples: {},
        loading: false,
    };

    componentDidMount() {
        this.fetchTexts()
    }

    fetchTexts(){
        AuthService
            .jwt_get(REVISE_URL, {
                "minimum_frequency": 4,
            })
            .then(data => {
                console.log(data)
                const lemmas = data.data.map(record =>{return {_id: record._id}})
                const lemmasToExamples = {}
                for (let i=0; i<lemmas.length; i++){
                    const lemma = data.data[i]._id
                    const examples =  data.data[i].examples
                    lemmasToExamples[lemma] = examples
                }
                console.log(lemmasToExamples)
                this.setState({
                    loading:false,
                    data: data.data,
                    lemmas: lemmas,
                    lemmasToExamples: lemmasToExamples
                })
            })
            .catch(err => console.log('Error fetching texts: ', err))
    }

    changeLemma=(newLemma) => {
        console.log('changing lemma')
        this.setState({
            currentLemma: newLemma,
            currentExamples: this.state.lemmasToExamples[newLemma]
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
                        <Definition lemma={this.state.currentLemma}/>
                    </SidebarSection>
                </Sidebar>
            </Container>
        );
    }
}

export default ReviseContainer;