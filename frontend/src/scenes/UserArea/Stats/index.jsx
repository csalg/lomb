import React from 'react';
import AuthService from "../../../services/auth";
import {STATS_URL} from "../../../endpoints";
import awaitAuthService from "../../../services/auth";

export default class extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            loading: true,
            ignored_lemmas: 147,
            lemmas_with_high_por: 230,
            seen_last_day: 10,
            seen_last_week: 20,
            seen_last_month: 30,
            seen_total: 40,
        }

        this.fetchStats = this.fetchStats.bind(this)
    }


    componentDidMount() {
        this.fetchStats()
    }

    async fetchStats(){
        const res = await awaitAuthService.jwt_get(STATS_URL)
        console.log(res)
        this.setState({...(res.data), loading: false})
    }

    render() {
        return (<div style={{padding: '2em 0'}}>
            <span style={{display: this.state.loading? 'auto' : 'none'}}>Loading</span>
            <ul style={{display: this.state.loading? 'none': 'block'}}>
                <li>There are {this.state.ignored_lemmas} lemmas in your ignore list.</li>
                {/*<li>Of the lemmas you are learning, {this.state.lemmas_with_high_por} have a probability of recall (PoR)*/}
                {/*    of 0.5 or higher*/}
                {/*</li>*/}
                <li>Activity level - here's how many exposures you have logged recently:</li>
                <ul>
                    <li>{this.state.seen_last_day} in the past 24h.</li>
                    <li>{this.state.seen_last_week} in the past week, </li>
                    <li>{this.state.seen_last_month} in the past month.</li>
                </ul>
                {/*<li>Distribution of learning words and PoR Over a certain frequency?</li>*/}
            </ul>
        </div>)
    }
}
