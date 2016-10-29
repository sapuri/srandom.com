import React from 'react';
import ReactDOM from 'react-dom';
import MusicList from './components/MusicList';

// URLから難易度表とレベルを判定
const url = window.location.href;
const split_url = url.split('/');
const is_srandom = split_url[3] === 'difflist';
const level = Number(split_url[4]);

// TODO: 記録編集機能を実装
ReactDOM.render(
    <MusicList lv={level} is_srandom={is_srandom} />,
    document.getElementById('content')
);
