import React from 'react';
import ModalDialog from './ModalDialog';

export default class Music extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            record: {
                medal: null,
                bad_count: null,
                updated_at: null
            },
            clear_status: 'no-play',
            dialog: false
        };
        this.handleOpenDialog = this.handleOpenDialog.bind(this);
    }

    handleOpenDialog(event) {
        this.setState({ dialog: true });
    }

    loadRecord() {
        $.ajax({
            url: `/api/users/${this.props.user.username}/record/${this.props.id}/`,
            dataType: 'json',
            cache: false,
            success: data => {
                this.setState({
                    record: {
                        medal: data.medal.medal,
                        bad_count: data.bad_count.bad_count,
                        updated_at: data.medal.updated_at_jst
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
        return (
            <tr id={`music-${this.props.id}`} className={this.state.clear_status} ref="music_table">
                <td className="level">{this.props.level}</td>
                <td className="title"><a onClick={this.handleOpenDialog}>{this.props.title}</a></td>
                <td className="difficulty">{this.props.difficulty}</td>
                <td className="bpm">{this.props.bpm}</td>
                <td className="medal">{(this.state.record.medal !== null && this.state.record.medal !== 12) ? <img src={`/static/img/medal/${this.state.record.medal}.png`} width="16" height="16" /> : '-'}</td>
                <td className="bad_count">{this.state.record.bad_count !== null ? this.state.record.bad_count : '-'}</td>
                <td className="updated_at">{this.state.record.updated_at !== null ? this.state.record.updated_at : '-'}</td>
                {this.state.dialog ? <ModalDialog is_active={this.state.dialog} id={this.props.id} title={this.props.title} difficulty={this.props.difficulty} record={this.state.record} /> : null}
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
