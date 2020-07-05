
import React from "react";
import { Table } from 'antd';
import reqwest from 'reqwest';
import AuthService from "../../services/auth";
import {ALL_TEXTS, LIBRARY_UPLOADS} from "../../endpoints";
import {Link} from "react-router-dom";

const columns = [
    {
        title: 'Title',
        dataIndex: 'title',
        sorter: true,
        // width: '20%',
        render: (text, record) => (
        <a href={`/reader.html?open="${LIBRARY_UPLOADS}/${record.filename}"`} style={{ marginRight: 16 }}>{record.title}</a>
        ),
    },
    {
        title: 'Language',
        dataIndex: 'source_language',
        filters: [
            { text: 'German', value: 'de' },
            { text: 'English', value: 'en' },
            { text: 'Spanish', value: 'es' },
            { text: 'Chinese', value: 'zh' },
        ],
        width: '20%',
        render: languageCode => (languageCodeToLanguageName(languageCode))
    },
    {
        title: 'Support language',
        dataIndex: 'support_language',
        filters: [
            { text: 'German', value: 'de' },
            { text: 'English', value: 'en' },
        ],
        width: '20%',
        render: languageCode => (languageCodeToLanguageName(languageCode))
    },
    // {
    //     title: 'Type',
    //     dataIndex: 'type',
    // },
];

const languageCodeToLanguageName = languageCode => ({
    de: 'German',
    en: 'English',
    es: 'Spanish',
    zh: 'Chinese'
}[languageCode])

// const getRandomuserParams = params => {
//     return {
//         results: params.pagination.pageSize,
//         page: params.pagination.current,
//         ...params,
//     };
// };

class Library extends React.Component {
    state = {
        data: [],
        pagination: {
            current: 1,
            pageSize: 10,
        },
        loading: false,
    };

    componentDidMount() {
        // const { pagination } = this.state;
        // this.fetch({ pagination });
        this.fetchTexts()
    }

    handleTableChange = (pagination, filters, sorter) => {
        // this.fetch({
        //     sortField: sorter.field,
        //     sortOrder: sorter.order,
        //     pagination,
        //     ...filters,
        // });
    };

    // fetch = (params = {}) => {
    //     this.setState({ loading: true });
    //     reqwest({
    //         url: 'https://randomuser.me/api',
    //         method: 'get',
    //         type: 'json',
    //         data: getRandomuserParams(params),
    //     }).then(data => {
    //         console.log(data.results);
    //         // this.setState({
    //         //     loading: false,
    //         //     data: data.results,
    //         //     pagination: {
    //         //         ...params.pagination,
    //         //         total: 200,
    //         //         // 200 is mock data, you should read it from server
    //         //         // total: data.totalCount,
    //         //     },
    //         // });
    //     });
    // };

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
        const { data, pagination, loading } = this.state;
        return (
            <Table
                columns={columns}
                rowKey={record => record._id}
                dataSource={data}
                pagination={pagination}
                loading={loading}
                onChange={this.handleTableChange}
            />
        );
    }
}



export default Library;