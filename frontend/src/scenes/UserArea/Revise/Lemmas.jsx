import React from "react";
import AuthService from "../../../services/auth";
import {DELETE_URL, INTERACTION_TRACKING_URL} from "../../../endpoints";
import './Lemmas.css'
import {neutral2, neutral3} from "../../../PALETTE";
import styled from 'styled-components'
import DeleteOutlined from "@ant-design/icons/lib/icons/DeleteOutlined";
import {Tooltip} from "antd";

export default class Lemmas extends React.Component {
    constructor(props) {
        super(props)

        this.__createObserver = this.__createObserver.bind(this)
        this.__outOfViewCallback = this.__outOfViewCallback.bind(this)
        this.clickCallback = this.clickCallback.bind(this)

        this.__createObserver()
    }

    __createObserver() {
        const options = {
            root: null,
            rootMargin: '0px 0px -100%',
            threshold: 0
        }
        this.firstRun = true
        this.observer = new IntersectionObserver(this.__outOfViewCallback, options)
    }

    __outOfViewCallback(entries) {
        if (this.firstRun) {
            this.firstRun = false;
            return
        }
        if (entries.length > 20) {
            return
        }
        entries.forEach(entry => {
            const lemma = entry.target.childNodes[0].innerText
            if (!this.__isLemmaSeen(entry.target)) {
                    entry.target.classList.add('exposed');
                    const sourceLanguage = entry.target.dataset.sourceLanguage
                    AuthService
                        .jwt_post(
                            INTERACTION_TRACKING_URL,
                            this.__lemma_was_not_clicked_message(lemma, sourceLanguage)
                        )
                }
            this.props.notifyInfiniteScroll(lemma)
            }
        )
    }

    __lemma_was_not_clicked_message(lemma, sourceLanguage) {
        console.log(lemma)
        return {
            message: this.props.scrollEventType,
            lemmas: new Array(lemma,),
            source_language: sourceLanguage,
            support_language: this.props.supportLanguage || 'en',
        }
    }

    clickCallback(target, lemma, sourceLanguage) {
        console.log(`clickCallback: ${target}, ${lemma}, ${sourceLanguage}`)
        if (!this.__isLemmaSeen(target)) {
            target.classList.add('looked-up');
            AuthService
                .jwt_post(
                    INTERACTION_TRACKING_URL,
                    this.__lemma_was_clicked_message(lemma, sourceLanguage)
                )
        }
        this.props.changeLemma(lemma, sourceLanguage)
    }

    __lemma_was_clicked_message(lemma, sourceLanguage) {
        console.log(lemma)
        return {
            message: this.props.clickEventType,
            lemmas: new Array(lemma,),
            source_language: sourceLanguage,
            support_language: this.props.supportLanguage || 'en',
        }
    }

    __isLemmaSeen(target) {
        return target.classList.contains('exposed') || target.classList.contains('looked-up');
    }

    render() {
        const Wrapper = styled.div`
        margin: 0rem;
`
        return (
            <Wrapper>

                <table
                    style={{
                        width: '100%',
                        border: `thin solid ${neutral3}`
                    }}
                >
                    <thead style={{
                        background: neutral2,
                        padding: '1rem',
                        position: 'sticky',
                        top: 0
                    }}>
                    <th>Word</th>
                    <th>Freq.</th>
                    <th>PoR</th>
                    <th>Actions</th>
                    </thead>
                    <tbody>
                    {this.props.rows.map((row) => <Lemma clickCallback={this.clickCallback}
                                                            key={row.id_} row={row}
                                                            observer={this.observer}/>)}
                    </tbody>
                </table>
                <div style={{height: '105vh'}}/>
            </Wrapper>
        )
    }
}

class Lemma extends React.Component {
    componentDidMount() {
        this.props.observer.observe(this.element)
    }

    state = {
        isVisible: true
    }

    render() {
        const {_id: lemma_, sourceLanguage, frequency, probability} = this.props.row
        console.log(`rendering lemma: ${lemma_}`)
        console.log(this.props.row)
        if (this.state.isVisible) {
            return (
                <tr
                    ref={element => (this.element = element)}
                    data-source-language={sourceLanguage}
                    data-something='bar'
                    onClick={(e) => this.props.clickCallback(this.element, lemma_, sourceLanguage)}
                >
                    <td>{lemma_}</td>
                    <td>{frequency}</td>
                    <td>{probability.toFixed(3)}</td>
                    <td>
                        <Tooltip title={`Remove ${lemma_} from my revision items`}>
                            <a onClick={_ => {
                                this.setState({isVisible:false})
                                AuthService.jwt_post(DELETE_URL, {
                                    lemma : lemma_,
                                    source_language:sourceLanguage
                                })}
                            }>
                                <DeleteOutlined/>
                            </a>
                        </Tooltip>
                    </td>
                </tr>
            )
        } else {
            return <tr/>
        }
    }
}
