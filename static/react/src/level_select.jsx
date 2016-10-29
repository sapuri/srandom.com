import React from 'react';
import ReactDOM from 'react-dom';
import FolderList from './components/FolderList';

// URLから難易度表を判定
const url = window.location.href;
const split_url = url.split('/');
const is_srandom = split_url[3] === 'difflist';

ReactDOM.render(
    <FolderList is_srandom={is_srandom} />,
    document.getElementById('content')
);
