import React from "react";
import 'antd/dist/antd.css';
import {Slider, InputNumber, Row, Col, Button} from 'antd';
import styled from 'styled-components'
import {neutral1, neutral3} from "../../../PALETTE";
import ReloadOutlined from "@ant-design/icons/lib/icons/ReloadOutlined";
import UserPreferences from "../../../services/userPreferences";

class Filter extends React.Component {
    state = {
        minimum_frequency: 5,
        maximum_por: 0.6,
        maximum_time_elapsed: 7,
    };

    componentDidMount() {
        UserPreferences.get('revision__minimum_frequency')
            .then(val =>
                this.setState({minimum_frequency: val})
            )
            .catch(e => console.log(e))
        UserPreferences.get('revision__maximum_por')
            .then(val =>
                this.setState({maximum_por: val})
            )
            .catch(e => console.log(e))
        UserPreferences.get('revision__maximum_time_elapsed')
            .then(maximum_time_elapsed =>
                this.setState({maximum_time_elapsed})
            )
            .catch(e => console.log(e))
    }

    render() {
        const Container = styled.div`
                background: ${neutral1};
                border: thin solid ${neutral3};
                padding: 1rem;
                margin: 1rem;
            `

        const {minimum_frequency, maximum_por, maximum_time_elapsed} = this.state;
        return (
            <Container style={this.props.style}>
                <Row>
                    <Col span={24}>
                        <b style={{color: 'hsla(0,0%,0%,0.5)'}}>
                            Minimum frequency:</b></Col>
                </Row>
                <Row>
                    <Col span={16}>
                        <Slider
                            min={1}
                            max={2000}
                            onChange={val => this.setState({minimum_frequency:val})}
                            value={typeof minimum_frequency === 'number' ? minimum_frequency : 0}
                        />
                    </Col>
                    <Col span={8}>
                        <InputNumber
                            min={1}
                            style={{margin: '0'}}
                            value={minimum_frequency}
                            onChange={val => this.setState({minimum_frequency:val})}
                        />
                    </Col>
                </Row>
                <Row>
                <Col span={24}>
                    <b style={{color: 'hsla(0,0%,0%,0.5)'}}>
                        Maximum probability of recall:</b></Col>
            </Row>
                <Row>
                    <Col span={16}>
                        <Slider
                            min={0}
                            max={1.0}
                            step={0.05}
                            onChange={val => this.setState({maximum_por:val})}
                            value={typeof maximum_por === 'number' ? maximum_por : 0}
                        />
                    </Col>
                    <Col span={8}>
                        <InputNumber
                            min={0}
                            max={1.0}
                            step={0.05}
                            style={{margin: '0'}}
                            value={maximum_por}
                            onChange={val => this.setState({maximum_por:val})}
                        />
                    </Col>
                </Row>
                <Row>
                    <Col span={24}>
                        <b style={{color: 'hsla(0,0%,0%,0.5)'}}>
                            Maximum time elapsed since last exposure</b></Col>
                </Row>
                <Row>
                    <Col span={16}>
                        <Slider
                            min={0}
                            max={60}
                            step={1}
                            onChange={maximum_time_elapsed => this.setState({maximum_time_elapsed})}
                            value={typeof maximum_time_elapsed === 'number' ? maximum_time_elapsed : 0}
                        />
                    </Col>
                    <Col span={8}>
                        <InputNumber
                            min={0}
                            max={50}
                            step={1}
                            style={{margin: '0'}}
                            value={maximum_time_elapsed}
                            onChange={maximum_time_elapsed => this.setState({maximum_time_elapsed})}
                        />
                    </Col>
                </Row>
                <Row>
                    <Col span={16}></Col>
                    <Col span={8}>
                        <Button
                            primary
                            shape="round"
                            icon={<ReloadOutlined/>}
                            size={'small'}
                            style={{marginTop: '1rem'}}
                            onClick={e => {
                                UserPreferences.set('revision__minimum_frequency', this.state.minimum_frequency)
                                UserPreferences.set('revision__maximum_por', this.state.maximum_por)
                                UserPreferences.set('revision__maximum_time_elapsed', this.state.maximum_time_elapsed)
                                this.props.fetchTexts()
                            }
                            }
                        >
                            Reload
                        </Button>
                    </Col>
                </Row>
            </Container>
        );
    }
}

export default class extends React.Component {
    render() {
        return <div><Filter {...this.props}/></div>
    }
}