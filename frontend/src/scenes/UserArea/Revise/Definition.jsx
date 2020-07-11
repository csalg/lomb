import React, {useState} from 'react'
import getLanguages from "../../../services/getLanguages";
import {LANGUAGE_NAMES} from "../../../services/languages";
import {USE_LINGUEE_SERVICES} from "../../../config";

export default class extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            currentLemma: "",
            sourceLanguage: "en",
            supportLanguage: "en"
        }
    }


    shouldComponentUpdate(nextProps, nextState, nextContext) {
        console.log('shouldComponentUpdate Definition')
        console.log(nextProps)
        return this.state.currentLemma != nextState.currentLemma
    }

    componentDidMount() {
        document.body.addEventListener('wordWasClicked', e => {
                console.log('Component did mount')
                this.setState({...e.detail()})
                console.log('state was updated')
                console.log(e.detail())
                console.log(this.state)
            }
        )
    }

    render() {
        let {currentLemma, sourceLanguage, supportLanguage} = this.state
        sourceLanguage  = LANGUAGE_NAMES[sourceLanguage].toLowerCase()
        supportLanguage = LANGUAGE_NAMES[supportLanguage].toLowerCase()
        const dictionary_url = `https://android.linguee.com/${sourceLanguage}-${supportLanguage}/translation/${currentLemma}.html`
        const Frame = (props) => (<iframe
            {...props}
            title='definition'
            key={`${currentLemma}_${sourceLanguage}`}
            style={{width: '100%', height: '100%'}}/>)
        if (currentLemma && USE_LINGUEE_SERVICES) {
            return  <Frame src={dictionary_url}/>
        }
        return <Frame/>
    }
}
