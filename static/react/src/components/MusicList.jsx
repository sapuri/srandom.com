import React from 'react';
import MusicTable from './MusicTable';
import Loader from './Loader';

export default class MusicList extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            data: [],
            folder_lamp: 'no-play',
            loading: true
        };
    }

    loadMusicList() {
        const max_lv = this.props.is_srandom ? 17 : 50;
        const url = this.props.is_srandom ? `/api/music/?sran_level=${max_lv+1-this.props.lv}&ordering=level,title` : `/api/music/?level=${max_lv+1-this.props.lv}&ordering=sran_level,title`;
        $.ajax({
            url: url,
            dataType: 'json',
            cache: false,
            success: data => this.setState({
                data: data,
                loading: false
            }),
            error: (xhr, status, err) => console.error(status, err.toString())
        });
    }

    loadFolderLamp() {
        $.ajax({
            url: `/api/get_folder_lamp/${this.props.lv}/`,
            dataType: 'json',
            data: {is_srandom: this.props.is_srandom},
            cache: false,
            success: data => this.setState({ folder_lamp: data.folder_lamp }),
            error: (xhr, status, err) => console.error(status, err.toString())
        });
    }

    componentDidMount() {
        this.loadMusicList();
        this.loadFolderLamp();
    }

    render() {
        return (
            <div id="music-list">
                <h3 id={`lv${this.props.lv}`} className={`level-folder ${this.state.folder_lamp}`}>Lv{this.props.lv}</h3>
                <MusicTable data={this.state.data.results} count={this.state.data.count} is_srandom={this.props.is_srandom} />
                <Loader is_active={this.state.loading} />
            </div>
        );
    }
}
MusicList.propTypes = {
    lv: React.PropTypes.number.isRequired,
    is_srandom: React.PropTypes.bool.isRequired
};
