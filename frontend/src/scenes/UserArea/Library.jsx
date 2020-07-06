
import React from "react";
import { Table } from 'antd';
import AuthService from "../../services/auth";
import {ALL_TEXTS, LIBRARY_UPLOADS} from "../../endpoints";
import getLanguages from "../../services/getLanguages";





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
            render: languageCode => (this.languageCodeToLanguageName(languageCode))
        },
        {
            title: 'Support language',
            dataIndex: 'support_language',
            width: '20%',
            render: languageCode => (this.languageCodeToLanguageName(languageCode))
        },
    ];

    languageCodeToLanguageName(languageCode){
        return this.state.languageCodes[languageCode]
    }

    componentDidMount() {
        this.fetchTexts()
        getLanguages().then(languageCodes => this.setState({languageCodes: languageCodes}))
    }

    fetchTexts(){
        AuthService
            .jwt_get(ALL_TEXTS)
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