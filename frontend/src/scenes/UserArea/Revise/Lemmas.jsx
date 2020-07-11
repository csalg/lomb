import React from "react";
import AuthService from "../../../services/auth";
import {INTERACTION_TRACKING_URL} from "../../../endpoints";
import './Lemmas.css'

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
                if (!this.__isLemmaSeen(entry.target)) {
                    entry.target.classList.add('exposed');
                    const lemma = entry.target.innerText
                    const sourceLanguage = entry.target.dataset.sourceLanguage
                    AuthService
                        .jwt_post(
                            INTERACTION_TRACKING_URL,
                            this.__lemma_was_not_clicked_message(lemma, sourceLanguage)
                        )
                }
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

    clickCallback(target, lemma, sourceLanguage) {
        if (!this.__isLemmaSeen(target)) {
            target.classList.add('looked-up');
            this.props.changeLemma(lemma, sourceLanguage)
            AuthService
                .jwt_post(
                    INTERACTION_TRACKING_URL,
                    this.__lemma_was_clicked_message(lemma, sourceLanguage)
                )
        }
    }

    __lemma_was_clicked_message(lemma, sourceLanguage) {
        return {
            message: 'REVISION__CLICKED',
            lemmas: [lemma],
            source_language: sourceLanguage,
            support_language: "",
        }
    }

    // shouldComponentUpdate(nextProps, nextState, nextContext) {
    //     console.log('shouldComponentUpdate Lemmas')
    //     console.log(nextProps)
    //     console.log(nextState)
    //     // if (nextProps.rows.length === this.props.rows.length){
    //     //     return false
    //     // }
    //
    //     return false
    // }

    render() {
        return (
            <>
                <table>
                    <tbody>
                    {this.props.rows.map((row, i) => <Lemma clickCallback={this.clickCallback}
                                                       key={i} row={row}
                                                       observer={this.observer}/>)}
                    </tbody>
                </table>
                <div style={{height: '105vh'}}/>
            </>
        )
    }

    __isLemmaSeen(target) {
        return target.classList.contains('exposed') || target.classList.contains('looked-up');
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
                onClick={(e) => this.props.clickCallback(this.element,lemma, sourceLanguage)}
            >
                <td>{lemma}</td>
            </tr>
        )
    }
}
