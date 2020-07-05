import React, {useState} from 'react'

export default (props) => {
    const {lemma} = props
    const dictionary_url = `https://android.linguee.com/german-english/translation/${lemma}.html`
    return <iframe src={dictionary_url} style={{width: '100%', height: '100%'}}/>
}
