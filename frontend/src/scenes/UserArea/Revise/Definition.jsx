import React, {useState} from 'react'

export default (props) => {
    const {lemma} = props
    const dictionary_url = `https://android.linguee.com/german-english/translation/${lemma}.html`
    if (lemma){
        return <iframe title='definition' src={dictionary_url} style={{width: '100%', height: '100%'}}/>
    }
    return <></>
}
