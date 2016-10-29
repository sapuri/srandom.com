import React from 'react';

export default class Music extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            record: {
                medal: '-',
                bad_count: '-',
                updated_at: '-'
            },
            clear_status: 'no-play'
        };
    }

    loadRecord() {
        $.ajax({
            url: `/api/users/${this.props.user.username}/record/${this.props.id}/`,
            dataType: 'json',
            cache: false,
            success: data => {
                const medal = data.medal.medal !== null ? data.medal.medal : '-';
                const bad_count = data.bad_count.bad_count !== null ? data.bad_count.bad_count : '-';
                const updated_at = data.medal.updated_at_jst !== null ? data.medal.updated_at_jst : '-';
                this.setState({
                    record: {
                        medal: medal,
                        bad_count: bad_count,
                        updated_at: updated_at
                    }
                });
            },
            error: (xhr, status, err) => console.error(status, err.toString())
        });
    }

    loadClearStatus() {
        $.ajax({
            url: `/api/get_clear_status/${this.props.id}/`,
            dataType: 'json',
            cache: false,
            success: data => this.setState({ clear_status: data.clear_status }),
            error: (xhr, status, err) => console.error(status, err.toString())
        });
    }

    componentDidMount() {
        this.loadRecord();
        this.loadClearStatus();
    }

    render() {
        const medal_img = () => (this.state.record.medal !== '-' && this.state.record.medal !== 12) ? <img src={`/static/img/medal/${this.state.record.medal}.png`} width="16" height="16" /> : '-'
        return (
            <tr id={`music-${this.props.id}`} className={this.state.clear_status}>
                <td className="level">{this.props.level}</td>
                <td className="title"><a href={`/edit/${this.props.id}/`}>{this.props.title}</a></td>
                <td className="difficulty">{this.props.difficulty}</td>
                <td className="bpm">{this.props.bpm}</td>
                <td className="medal">{medal_img()}</td>
                <td className="bad_count">{this.state.record.bad_count}</td>
                <td className="updated_at">{this.state.record.updated_at}</td>
            </tr>
        );
    }
}
Music.propTypes = {
    id: React.PropTypes.number.isRequired,
    title: React.PropTypes.string.isRequired,
    level: React.PropTypes.number.isRequired,
    difficulty: React.PropTypes.string.isRequired,
    bpm: React.PropTypes.string.isRequired,
    user: React.PropTypes.object.isRequired
};
