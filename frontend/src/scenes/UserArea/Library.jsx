import React from "react";
import {Alert, Tag, Table} from 'antd';
import AuthService from "../../services/auth";
import {ALL_TEXTS, LIBRARY_TEXT, LIBRARY_UPLOADS} from "../../endpoints";
import UserPreferences from "../../services/userPreferences";
import {LANGUAGE_NAMES} from "../../services/languages";
import parseErrorMessage from "../../services/parseErrorMessage";
import {AdminOnlyContainer, AdminOrSameUsernameContainer} from "../../services/Permissions";
import jwt_decode from 'jwt-decode'
import {toast} from "react-toastify";

const actionsView = (id,username,deleteRow) => {
    const deleteHandler = _ => {
        AuthService
            .jwt_delete(`${LIBRARY_TEXT}/${id}`)
            .then(response => {
                toast(response.data);
                deleteRow(id)
            })
            .catch(error => toast(parseErrorMessage(error)))
    }
    return (
        <>
            {/*<a>Pre-drill vocabulary</a>*/}
            {/*<a>Read</a>*/}
            <AdminOrSameUsernameContainer username={username} >
                <a onClick={deleteHandler}>Delete</a>
                {/*<a>Edit</a>*/}
            </AdminOrSameUsernameContainer>
        </>
    )
}

class Library extends React.Component {
    constructor() {
        super();
        this.deleteRow = this.deleteRow.bind(this)
    }
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
            width: '40%',
            sorter: true,
            render: (text, record) => (
                <a href={`/reader.html?open="${LIBRARY_UPLOADS}/${record.filename}"`}
                   style={{marginRight: 16}}>{record.title}</a>
            ),
        },
        {
            title: 'Difficulty',
            dataIndex: 'average_lemma_rank',
            width: '10%',
        },
        {
            title: 'Tags',
            dataIndex: 'tags',
            width: '10%',
            render: (text, record) => (
                <>{
                    record.tags.map(tag =>
                        <Tag>{tag}</Tag>
                    )
                }</>
            ),
        },
        {
            title: 'Language',
            dataIndex: 'source_language',
            width: '10%',
            render: this.languageCodeToLanguageName
        },
        {
            title: 'Support language',
            dataIndex: 'support_language',
            width: '10%',
            render: this.languageCodeToLanguageName
        },
        {
            title: 'Uploader',
            dataIndex: 'owner',
            width: '10%',
        },
        {
            title: 'Actions',
            dataIndex: '_id',
            width: '10%',
            render: (id,record) => actionsView(id,record.owner, this.deleteRow)
        },
    ];

    languageCodeToLanguageName(languageCode) {
        return LANGUAGE_NAMES[languageCode]
    }

    deleteRow(id){
        const new_data = this.state.data.filter(record => record._id != id)
        this.setState({data:new_data})
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
            this.setState({error: parseErrorMessage(err)})
        }
    }


    render() {
        const {data, loading} = this.state;
        const token = window.localStorage.getItem('user');
        console.log(jwt_decode(JSON.parse(token)))
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