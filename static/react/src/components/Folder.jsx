import React from 'react';

export default class Folder extends React.Component {
    constructor(props) {
        super(props);
        this.state = { folder_lamp: 'no-play' };
    }

    loadFolderLamp() {
        $.ajax({
            url: `/api/get_folder_lamp/${level}/`,
            dataType: 'json',
            data: {is_srandom: this.props.is_srandom},
            cache: false,
            success: data => this.setState({ folder_lamp: data.folder_lamp }),
            error: (xhr, status, err) => console.error(status, err.toString())
        });
    }

    render() {
        const url = this.props.is_srandom ? `/difflist/${this.props.level}/` : `/level/${this.props.level}/`;
        return (
            <a href={url} className="no-decoration">
                <h3 id={`lv${this.props.level}`} className={`level-folder ${this.state.folder_lamp}`}>Lv{this.props.level}</h3>
            </a>
        );
    }
}
Folder.propTypes = {
    level: React.PropTypes.number.isRequired,
    is_srandom: React.PropTypes.bool.isRequired
};
