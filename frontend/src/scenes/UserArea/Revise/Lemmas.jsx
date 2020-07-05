import React from "react";
import AuthService from "../../../services/auth";
import {INTERACTION_TRACKING_URL} from "../../../endpoints";

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
        console.log()
        entries.forEach(entry => {
                const lemma = entry.target.innerText
                const sourceLanguage =  entry.target.dataset.sourceLanguage
                AuthService
                    .jwt_post(
                        INTERACTION_TRACKING_URL,
                        this.__lemma_was_not_clicked_message(lemma, sourceLanguage)
                    )
            }
        )
    }

    __lemma_was_not_clicked_message(lemma, sourceLanguage) {
        return {
            message: 'REVISION__NOT_CLICKED',
            lemmas: [lemma],
            source_language: sourceLanguage,
            support_language: "",
        }
    }

    clickCallback(lemma,sourceLanguage){
        AuthService
            .jwt_post(
                INTERACTION_TRACKING_URL,
                this.__lemma_was_clicked_message(lemma, sourceLanguage)
            )
    }

    __lemma_was_clicked_message(lemma, sourceLanguage) {
        return {
            message: 'REVISION__CLICKED',
            lemmas: [lemma],
            source_language: sourceLanguage,
            support_language: "",
        }
    }

    render() {
        return (
            <>
                <table>
                    <tbody>
                    {this.props.rows.map(row => <Lemma clickCallback={this.clickCallback} key={row._id} row={row} observer={this.observer}/>)}
                    </tbody>
                </table>
                <div style={{height: '105vh'}}/>
            </>
        )
    }
}

class Lemma extends React.Component {
    componentDidMount() {
        this.props.observer.observe(this.element)
    }

    render() {
        const lemma = this.props.row._id
        const sourceLanguage = this.props.row.sourceLanguage
        return (
            <tr
                ref={element => (this.element = element)}
                data-source-language={sourceLanguage}
                data-something='bar'
                onClick={() => this.props.clickCallback(lemma, sourceLanguage)}
            >
                <td>{lemma}</td>
            </tr>
        )
    }
}
