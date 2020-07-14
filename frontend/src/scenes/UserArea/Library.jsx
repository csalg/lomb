
import React from "react";
import { Table } from 'antd';
import AuthService from "../../services/auth";
import {ALL_TEXTS, LIBRARY_UPLOADS} from "../../endpoints";
import getLanguages from "../../services/getLanguages";
import UserPreferences from "../../services/userPreferences";
import {LANGUAGE_NAMES} from "../../services/languages";





class Library extends React.Component {
    state = {
        data: [],
        languageCodes: {},
        loading: false,
    };

    columns = [
        {
            title: 'Title',
            dataIndex: 'title',
            sorter: true,
            render: (text, record) => (
                <a href={`/reader.html?open="${LIBRARY_UPLOADS}/${record.filename}"`} style={{ marginRight: 16 }}>{record.title}</a>
            ),
        },
        {
            title: 'Language',
            dataIndex: 'source_language',
            width: '20%',
            render: this.languageCodeToLanguageName
        },
        {
            title: 'Support language',
            dataIndex: 'support_language',
            width: '20%',
            render: this.languageCodeToLanguageName
        },
    ];

    languageCodeToLanguageName(languageCode){
        return LANGUAGE_NAMES[languageCode]
    }

    componentDidMount() {
        this.fetchTexts()
        // getLanguages().then(languageCodes => this.setState({languageCodes: languageCodes}))
    }

    async fetchTexts(){
        const learning_languages = await UserPreferences.get('learning_languages')
        const known_languages = await UserPreferences.get('known_languages')

        console.log(learning_languages, known_languages)
        AuthService
            .jwt_post(ALL_TEXTS, {
                learning_languages: learning_languages,
                known_languages: known_languages
            })
            .then(data => {
                this.setState({
                    loading:false,
                    data:data.data
                })
            })
            .catch(err => console.log('Error fetching texts: ', err))
    }


    render() {
        const { data, loading } = this.state;
        return (
            <Table
                columns={this.columns}
                rowKey={record => record._id}
                dataSource={data}
                pagination={false}
                loading={loading}
            />
        );
    }
}



export default Library;