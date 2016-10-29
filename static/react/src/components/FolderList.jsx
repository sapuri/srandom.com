import React from 'react';
import Folder from './Folder';

export default class FolderList extends React.Component {
    render() {
        const folder_list = [];
        const max_lv = this.props.is_srandom ? 17 : 50;
        const min_lv = this.props.is_srandom ? 1 : 38;
        for (let i = max_lv; i >= min_lv; i--) {
            folder_list.push(<Folder key={i} level={i} is_srandom={this.props.is_srandom} />);
        }

        return (
            <div id="folder-list">{folder_list}</div>
        );
    }
}
FolderList.propTypes = { is_srandom: React.PropTypes.bool.isRequired };
