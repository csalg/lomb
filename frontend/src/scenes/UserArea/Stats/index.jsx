import React from 'react';
import {STATS_URL} from "../../../endpoints";
import AuthService from "../../../services/auth";

export default class extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            loading: true,
        }

        this.fetchStats = this.fetchStats.bind(this)
    }

    componentDidMount() {
        this.fetchStats()
    }

    async fetchStats(){
        const res = await AuthService.jwt_get(STATS_URL)
        await this.setState({...(res.data), loading: false})
    }

    render() {
        const formatAmounts = num => num ? num.toLocaleString('en-US', {maximumFractionDigits:0}) : 0
        const weeklyAverage = formatAmounts(this.state.seen_last_week/7)
        const monthlyAverage = formatAmounts(this.state.seen_last_month/30)
        return (<div style={{padding: '2em 0'}}>
            <span style={{display: this.state.loading? 'auto' : 'none'}}>Loading</span>
            <ul style={{display: this.state.loading? 'none': 'block'}}>
                <li>There are <strong>{formatAmounts(this.state.ignored_lemmas)}</strong> lemmas in your ignore list.</li>
                <li>You have added <strong>{formatAmounts(this.state.learning_lemmas)}</strong> lemmas to your learning list.</li>
                <li>Activity level - here's how many exposures you have logged recently:</li>
                <ul>
                    <li><strong>{formatAmounts(this.state.seen_last_day)}</strong> in the past 24h.</li>
                    <li><strong>{formatAmounts(this.state.seen_last_week)}</strong> in the past week ({weeklyAverage} avg/day).</li>
                    <li><strong>{formatAmounts(this.state.seen_last_month)}</strong> in the past month ({monthlyAverage} avg/day).</li>
                </ul>
                <li>Distinct exposures - here's how many unique lemmas you have been exposed to recently:</li>
                <ul>
                    <li><strong>{formatAmounts(this.state.seen_last_day_unique)}</strong> in the past 24h.</li>
                    <li><strong>{formatAmounts(this.state.seen_last_week_unique)}</strong> in the past week.</li>
                    <li><strong>{formatAmounts(this.state.seen_last_month_unique)}</strong> in the past month.</li>
                </ul>
                {/*<li>Distribution of learning words and PoR Over a certain frequency?</li>*/}
            </ul>
        </div>)
    }
}