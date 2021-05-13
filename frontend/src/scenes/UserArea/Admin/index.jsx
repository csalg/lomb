import React from 'react'
import {List, Avatar} from 'antd';
import {
    SearchOutlined,
    DiffOutlined,
    LineChartOutlined,
    DownloadOutlined
} from '@ant-design/icons'
import {
    ETL_FROM_SCRATCH_URL, GET_DATASET_URL,
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
        description: "Recalculate everything again from the logs. This also generates past datapoint dataset.",
        action: () => {
            AuthService
                .jwt_get(ETL_FROM_SCRATCH_URL)
                .then((response) => {
                    console.log(response)
                    const url = window.URL.createObjectURL(new Blob([response.data]));
                    const link = document.createElement('a');
                    link.href = url;
                    link.setAttribute('download', 'file.pdf');
                    document.body.appendChild(link);
                    link.click();
                }).catch(error => toast(parseErrorMessage(error)))
        },
        last_performed: '2020/08/01',
        Icon: LineChartOutlined
    },
    // {
    //     command: 'Make dataset',
    //     description: "Make dataset from scratch",
    //     action: () => AuthService.jwt_get(MAKE_DATASET_URL),
    //     last_performed: '2020/08/01',
    //     Icon: LineChartOutlined
    // },
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
                <List.Item>
                    <List.Item.Meta
                        avatar={<Avatar><DownloadOutlined/></Avatar>}
                        title={<a href={GET_DATASET_URL}>Get dataset</a>}
                        description="Download dataset."
                    />
                    <div>Last performed: '2020/08/01'</div>
                </List.Item>
            </List>

        </div>
    )
}
