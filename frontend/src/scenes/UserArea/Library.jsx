
import React from "react";
import { Table } from 'antd';
import reqwest from 'reqwest';
import AuthService from "../../services/auth";
import {ALL_TEXTS} from "../../endpoints";

const columns = [
    {
        title: 'Title',
        dataIndex: 'title',
        sorter: true,
        width: '20%',
    },
    {
        title: 'Language',
        dataIndex: 'source_language',
        filters: [
            { text: 'German', value: 'de' },
            { text: 'English', value: 'en' },
        ],
        width: '20%',
    },
    {
        title: 'Support language',
        dataIndex: 'support_language',
        filters: [
            { text: 'German', value: 'de' },
            { text: 'English', value: 'en' },
        ],
        width: '20%',
    },
    {
        title: 'Type',
        dataIndex: 'type',
    },
      {
    title: 'Action',
    key: 'action',
    render: (text, record) => (
      <span>
        <a href={record.filename} style={{ marginRight: 16 }}>Read</a>
        <a>Delete</a>
      </span>
    ),
  },
];

const getRandomuserParams = params => {
    return {
        results: params.pagination.pageSize,
        page: params.pagination.current,
        ...params,
    };
};

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
        const { pagination } = this.state;
        this.fetch({ pagination });
        this.fetchTexts()
    }

    handleTableChange = (pagination, filters, sorter) => {
        this.fetch({
            sortField: sorter.field,
            sortOrder: sorter.order,
            pagination,
            ...filters,
        });
    };

    fetch = (params = {}) => {
        this.setState({ loading: true });
        reqwest({
            url: 'https://randomuser.me/api',
            method: 'get',
            type: 'json',
            data: getRandomuserParams(params),
        }).then(data => {
            console.log(data.results);
            // this.setState({
            //     loading: false,
            //     data: data.results,
            //     pagination: {
            //         ...params.pagination,
            //         total: 200,
            //         // 200 is mock data, you should read it from server
            //         // total: data.totalCount,
            //     },
            // });
        });
    };

    fetchTexts(){
        AuthService
            .jwt_get(ALL_TEXTS)
            .then(data => {
                console.log('data', data)
                console.log('data.data', data.data)
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