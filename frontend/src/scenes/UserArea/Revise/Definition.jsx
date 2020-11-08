import React from 'react'
import {LANGUAGE_NAMES} from "../../../services/languages";
import {USE_LINGUEE_SERVICES} from "../../../config";
import './Definition.css';

export default class extends React.Component {
    constructor(props) {
        super(props);
        this.frame = React.createRef()
        this.state = {
            currentLemma: "",
            sourceLanguage: "en",
            supportLanguage: "en"
        }

        this.__makeDictionaryUrl = this.__makeDictionaryUrl.bind(this)
    }

    shouldComponentUpdate(nextProps, nextState, nextContext) {
        if (this.state.currentLemma !== nextState.currentLemma) {
            console.log(nextState)
            const {sourceLanguage, supportLanguage, currentLemma } = nextState
            if (USE_LINGUEE_SERVICES && sourceLanguage && supportLanguage && currentLemma) {
                console.log(sourceLanguage,supportLanguage,currentLemma)
                this.__updateDefinition(sourceLanguage, supportLanguage, currentLemma)
                return true
            }
        }
        return false
    }

    __updateDefinition(sourceLanguage, supportLanguage, newLemma){
        let el  = document.body.querySelector('#revisionDefinition')
        let url = this.__makeDictionaryUrl(sourceLanguage, supportLanguage, newLemma)
        changeFrameSrcWithoutAffectingBrowserHistory(el,url)
    }

    __makeDictionaryUrl(sourceLanguage_, supportLanguage_, currentLemma) {
        try {
            const sourceLanguage = LANGUAGE_NAMES[sourceLanguage_].toLowerCase()
            const supportLanguage = LANGUAGE_NAMES[supportLanguage_].toLowerCase()
            if (sourceLanguage == "danish")
                return `https://da.bab.la/ordbog/dansk-engelsk/${currentLemma}`
            return `https://android.linguee.com/${sourceLanguage}-${supportLanguage}/translation/${currentLemma}.html`
        } catch {
            console.log(`Exception: ${sourceLanguage_}, ${supportLanguage_} don't seem to be valid language codes.`)
            return ""
        }
    }

    componentDidMount() {
        document.body.addEventListener('wordWasClicked', e => {
                this.setState({...e.detail()})
            }
        )
    }

    render() {
        return <iframe title='revisionDefinition' id='revisionDefinition'/>
    }
}

function changeFrameSrcWithoutAffectingBrowserHistory(iframe, uri) {

    console.log(iframe)
    const clonedFrame = iframe.cloneNode(true)
    const parentNode = iframe.parentNode
    clonedFrame.src = uri
    iframe.remove()
    return parentNode.appendChild(clonedFrame)
}
