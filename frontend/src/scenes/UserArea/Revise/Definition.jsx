import React, {useState} from 'react'
import getLanguages from "../../../services/getLanguages";
import {LANGUAGE_NAMES} from "../../../services/languages";

export default (props) => {
    let {lemma, sourceLanguage, supportLanguage} = props
    sourceLanguage = LANGUAGE_NAMES[sourceLanguage].toLowerCase()
    supportLanguage = LANGUAGE_NAMES[supportLanguage].toLowerCase()
    const dictionary_url = `https://android.linguee.com/${sourceLanguage}-${supportLanguage}/translation/${lemma}.html`
    if (lemma){
        return <iframe title='definition' src={dictionary_url} style={{width: '100%', height: '100%'}}/>
    }
    return <></>
}
