import React, {useEffect, useState} from "react";
import {authHeader} from "../../../../services/auth";
import {API_URL, LIBRARY_URL} from "../../../../endpoints";

const fetch_document = (url) => {
    const xhr = new XMLHttpRequest();
    return new Promise((resolve,reject) => {
        xhr.responseType = 'blob';
        xhr.onreadystatechange = function () {
                if (this.readyState === this.DONE) {
                    if (this.status === 200) {
                        resolve(URL.createObjectURL(this.response))
                    } else {
                        reject(xhr);
                    }
                }
            }
        xhr.open('GET', url);
        xhr.setRequestHeader('Authorization', authHeader().Authorization );
        xhr.send();
    });
}

export default function(props) {
    const [ blob, setBlob ] = useState("");

    // useEffect(async ()=> {
    //     const blob = await fetch_document('www.linguee.com');
    //     setBlob(blob)
    // }, [])

    useEffect(() => {
        let ignore = false;

        async function fetchData() {
            let url = LIBRARY_URL+'/uploads/'+props.match.params.file
            fetch_document(url)
                .then(data => {
                    if (!ignore)
                        setBlob(data)})
        }
        fetchData();
        return () => { ignore = true; }
    }, []);

    return (
        <div>
            <h2>{props.match.params.type}</h2>
            <h2>{props.match.params.file}</h2>
            <iframe src={blob} frameborder="0"/>
            {blob}
        </div>
    )
}
