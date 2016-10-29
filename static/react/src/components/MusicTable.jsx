import React from 'react';
import Music from './Music';

export default class MusicTable extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            my_account: {
                id: '',
                username: ''
            }
        };
    }

    loadMyAccount() {
        $.ajax({
            url: '/api/users/my_account/',
            dataType: 'json',
            cache: false,
            success: data => this.setState({
                my_account: {
                    id: data.id,
                    username: data.username
                }
            }),
            error: (xhr, status, err) => console.error(status, err.toString())
        });
    }

    componentDidMount() {
        this.loadMyAccount();
    }

    render() {
        const MusicNodes = this.props.data.map((music, index) => {
            const level = this.props.is_srandom ? music.level.level : music.sran_level.level;
            return (
                <Music
                    key={index}
                    id={music.id}
                    title={music.title}
                    level={level}
                    difficulty={music.difficulty.difficulty_short}
                    bpm={music.bpm}
                    user={this.state.my_account}
                />
            );
        });

        return (
            <table className="music-list table table-condensed">
                <thead>
                    <tr>
                        <th>{this.props.is_srandom ? 'Lv' : 'S乱Lv'}</th>
                        <th>曲名</th>
                        <th>難易度</th>
                        <th>BPM</th>
                        <th>メダル</th>
                        <th>BAD数</th>
                        <th>更新日時</th>
                    </tr>
                </thead>
                <tbody>
                    {MusicNodes}
                </tbody>
            </table>
        );
    }
}
MusicTable.propTypes = {
    data: React.PropTypes.array.isRequired,
    count: React.PropTypes.number.isRequired,
    is_srandom: React.PropTypes.bool.isRequired
};
MusicTable.defaultProps = {
    data: [],
    count: 0
};
