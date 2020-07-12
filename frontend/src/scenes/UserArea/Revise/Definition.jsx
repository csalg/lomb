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
            const {sourceLanguage, supportLanguage, currentLemma } = nextState
            this.__updateDefinition(sourceLanguage, supportLanguage, currentLemma)
            return true
        }
        return false
    }

    __updateDefinition(newLemma){
        let el  = document.body.querySelector('#revisionDefinition')
        let url = this.__makeDictionaryUrl(newLemma)
        changeFrameSrcWithoutAffectingBrowserHistory(el,url)
    }

    __makeDictionaryUrl(sourceLanguage, supportLanguage, currentLemma) {
        sourceLanguage = LANGUAGE_NAMES[sourceLanguage].toLowerCase()
        supportLanguage = LANGUAGE_NAMES[supportLanguage].toLowerCase()
        return `https://android.linguee.com/${sourceLanguage}-${supportLanguage}/translation/${currentLemma}.html`
    }

    componentDidMount() {
        document.body.addEventListener('wordWasClicked', e => {
                this.setState({...e.detail()})
            }
        )
    }

    render() {
        let {currentLemma, sourceLanguage, supportLanguage} = this.state
        sourceLanguage = LANGUAGE_NAMES[sourceLanguage].toLowerCase()
        supportLanguage = LANGUAGE_NAMES[supportLanguage].toLowerCase()
        console.log(currentLemma, USE_LINGUEE_SERVICES)
        const dictionary_url = `https://android.linguee.com/${sourceLanguage}-${supportLanguage}/translation/${currentLemma}.html`
        const Frame = (props) => (<iframe
            {...props}
            title='definition'
            key={`${currentLemma}_${sourceLanguage}`}
            style={{width: '100%', height: '100%'}}/>)
        // if (currentLemma && USE_LINGUEE_SERVICES) {
        //     return  <Frame src={dictionary_url}/>
        // }
        // return <Frame ref={this.frame}/>
        return <iframe id='revisionDefinition'/>
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
