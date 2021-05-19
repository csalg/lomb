import React from 'react'
import {List, Avatar} from 'antd';
import {
    SearchOutlined,
    DotChartOutlined,
    DownloadOutlined,
    ExperimentOutlined
} from '@ant-design/icons'
import {
    ADD_METADATA_URL,
    ETL_FROM_SCRATCH_URL, GET_DATASET_URL, REMOVE_IGNORED_DATAPOINTS,
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
        description: "Recalculate everything again from the logs. This generates current datapoints as well as a dataset with past datapoint dataset.",
        action: () => {
            AuthService
                .jwt_get(ETL_FROM_SCRATCH_URL)
                .then(()=> toast('ETL from scratch completed'))
                .catch(error => toast(parseErrorMessage(error)))
        },
        last_performed: '2020/08/01',
        Icon: DotChartOutlined
    },
    {
        command: 'Add metadata to data interpretations.',
        description: "Add support language and frequency to the datapoints table.",
        action: () => {
            AuthService
                .jwt_get(ADD_METADATA_URL)
                .then(()=> toast('Metadata successfully generated'))
                .catch(error => toast(parseErrorMessage(error)))
        },
        last_performed: '2020/08/01',
        Icon: ExperimentOutlined
    },
    {
        command: 'Remove ignored datapoints.',
        description: "Deletes all datapoints in the ignored set.",
        action: () => {
            AuthService
                .jwt_get(REMOVE_IGNORED_DATAPOINTS)
                .then(()=> toast('Removed ignored datapoints'))
                .catch(error => toast(parseErrorMessage(error)))
        },
        last_performed: '2020/08/01',
        Icon: ExperimentOutlined
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
                <List.Item>
                    <List.Item.Meta
                        avatar={<Avatar><DownloadOutlined/></Avatar>}
                        title={<a href={GET_DATASET_URL}>Get dataset</a>}
                        description="Download dataset with past datapoints for training models."
                    />
                    <div>Last performed: '2020/08/01'</div>
                </List.Item>
            </List>

        </div>
    )
}
