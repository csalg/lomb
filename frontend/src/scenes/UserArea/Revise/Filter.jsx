import React from "react";
import 'antd/dist/antd.css';
import {Slider, InputNumber, Row, Col, Button} from 'antd';
import styled from 'styled-components'
import {neutral1, neutral2, neutral3} from "../../../PALETTE";
import {Weight} from "@styled-icons/fa-solid/Weight";
import ReloadOutlined from "@ant-design/icons/lib/icons/ReloadOutlined";
import UserPreferences from "../../../services/userPreferences";

class IntegerStep extends React.Component {
    state = {
        inputValue: 5,
    };

    componentDidMount() {
        UserPreferences.get('revision__minimum_frequency')
            .then(inputValue =>
                this.setState({inputValue: inputValue})
            )
    }

    onChange = value => {
        this.setState({
            inputValue: value,
        });
    };

    render() {
        const Container = styled.div`
          background: ${neutral1};
          border: thin solid ${neutral3};
        padding: 1rem;
        margin: 1rem;
`

        const ScaleIcon = styled(Weight)`
height: 16px;
width:16px;
        
`
        const {inputValue} = this.state;
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
                            min={3}
                            max={50}
                            onChange={this.onChange}
                            value={typeof inputValue === 'number' ? inputValue : 0}
                        />
                    </Col>
                    <Col span={8}>
                        <InputNumber
                            min={3}
                            max={50}
                            style={{margin: '0'}}
                            value={inputValue}
                            onChange={this.onChange}
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
                                UserPreferences.set('revision__minimum_frequency', this.state.inputValue)
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
        return <div><IntegerStep {...this.props}/></div>
    }
}