import React from "react";
import {Alert, Table} from 'antd';
import AuthService from "../../services/auth";
import {ALL_TEXTS, LIBRARY_UPLOADS} from "../../endpoints";
import UserPreferences from "../../services/userPreferences";
import {LANGUAGE_NAMES} from "../../services/languages";
import parseErrorMessage from "../../services/parseErrorMessage";


class Library extends React.Component {
    state = {
        data: [],
        languageCodes: {},
        loading: false,
        error: ""
    };

    columns = [
        {
            title: 'Title',
            dataIndex: 'title',
            sorter: true,
            render: (text, record) => (
                <a href={`/reader.html?open="${LIBRARY_UPLOADS}/${record.filename}"`}
                   style={{marginRight: 16}}>{record.title}</a>
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

    languageCodeToLanguageName(languageCode) {
        return LANGUAGE_NAMES[languageCode]
    }

    componentDidMount() {
        this.fetchTexts()
    }

    async fetchTexts() {
        try {
            const learning_languages = await UserPreferences.get('learning_languages')
            const known_languages = await UserPreferences.get('known_languages')
            AuthService
                .jwt_post(ALL_TEXTS, {
                    learning_languages: learning_languages,
                    known_languages: known_languages
                })
                .then(data => {
                    this.setState({
                        loading: false,
                        data: data.data
                    })
                })
                .catch(err => {
                    this.setState({error: parseErrorMessage(err)})
                })
        } catch (err) {
            console.log(err)
            this.setState({error: parseErrorMessage(err)})
        }
    }


    render() {
        const {data, loading} = this.state;
        if (this.state.error)
            return (
                <Alert
                    description={this.state.error}
                    type="error"
                    style={{margin: '2em 0'}}
                    showIcon
                />
            )
        else
            return (
                <Table
                    columns={this.columns}
                    rowKey={record => record._id}
                    dataSource={data}
                    pagination={false}
                    loading={loading}
                />
            )
    }
}


export default Library;