import React from 'react'
import {List, Avatar} from 'antd';
import {
    OrderedListOutlined,
    SearchOutlined,
    DiffOutlined,
    LineChartOutlined,
} from '@ant-design/icons'
import {
    ETL_FROM_SCRATCH_URL,
    MAKE_DATASET_URL,
    UPDATE_LEMMA_RANKS_URL,
    UPDATE_TEXT_DIFFICULTIES
} from "../../../endpoints";
import AuthService from '../../../services/auth'
import {toast} from "react-toastify";
import parseErrorMessage from "../../../services/parseErrorMessage";

const data = [
    // {
    //     command: 'Update lemma ranks',
    //     description: "Update lemma ranks for a specific language",
    //     action: () => {
    //         AuthService
    //             .jwt_get(UPDATE_LEMMA_RANKS_URL)
    //             .then(response => toast(response.data))
    //             .catch(error => toast(parseErrorMessage(error)))
    //     },
    //     last_performed: '2020/08/01',
    //     Icon: OrderedListOutlined
    // },
    // {
    //     command: 'Calculate text difficulties',
    //     description: "Calculate text difficulties for a specific language",
    //     action: () => {
    //         AuthService
    //             .jwt_get(UPDATE_TEXT_DIFFICULTIES)
    //             .then(response => toast(response.data))
    //             .catch(error => toast(parseErrorMessage(error)))
    //     },
    //     last_performed: '2020/08/01',
    //     Icon: DiffOutlined
    // },
    {
        command: 'Search for new examples',
        description: "Search for new examples for everyone",
        action: () => console.log('update lemma ranks'),
        last_performed: '2020/08/01',
        Icon: SearchOutlined
    },

    {
        command: 'ETL from scratch',
        description: "Delete all datapoints and recalculate everything again from the logs.",
        action: () => {
            AuthService
                .jwt_get(ETL_FROM_SCRATCH_URL)
                .then(response => toast(response.data))
                .catch(error => toast(parseErrorMessage(error)))
        },
        last_performed: '2020/08/01',
        Icon: DiffOutlined
    },
    {
        command: 'Make dataset',
        description: "Make dataset from logs.",
        action: () => {
            AuthService
                .jwt_get(MAKE_DATASET_URL)
                .catch(error => toast(parseErrorMessage(error)))
        },
        last_performed: '2020/08/01',
        Icon: LineChartOutlined
    },
];

export default props => {
    return (
        <div>
            <List
                itemLayout="horizontal"
            >
                {data.map(command => {
                    const {Icon} = command
                    return (
                        <List.Item>
                            <List.Item.Meta
                                avatar={<Avatar><Icon/></Avatar>}
                                title={<a onClick={command.action}>{command.command}</a>}
                                description={command.description}
                            />
                            <div>Last performed: {command.last_performed}</div>
                        </List.Item>
                    )
                })}
            </List>

        </div>
    )
}