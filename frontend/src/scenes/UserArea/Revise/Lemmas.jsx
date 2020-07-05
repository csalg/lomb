
import React from "react";
import { Table } from 'antd';
import reqwest from 'reqwest';
import AuthService from "../../../services/auth";
import {ALL_TEXTS, LIBRARY_UPLOADS, REVISE_URL} from "../../../endpoints";
import {Link} from "react-router-dom";



class Lemmas extends React.Component {

    render() {
        const columns = [
            {
                title: 'Lemma',
                dataIndex: '_id',
                width: '20%',
            },
        ];
        const { rows} = this.props;
        return (
            <>
            <Table
                columns={columns}
                onRow={(record, rowIndex) => {
                    return {
                        onClick: event => {
                            console.log(event,record)
                            this.props.changeLemma(record._id)
                        }, // click row
                    };
                }}
                rowKey={record => record._id}
                dataSource={rows}
                onChange={this.handleTableChange}
                pagination={false}
            />
            <div style={{height: '105vh'}}></div>
            </>
        );
    }
}

export default Lemmas;