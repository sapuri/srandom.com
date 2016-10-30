import React from 'react';
import ReactDOM from 'react-dom';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import injectTapEventPlugin from 'react-tap-event-plugin';

import MusicList from './components/MusicList';

// Material-UI の onTouchTap に必要
injectTapEventPlugin();

// URLから難易度表とレベルを判定
const url = window.location.href;
const split_url = url.split('/');
const is_srandom = split_url[3] === 'difflist';
const level = Number(split_url[4]);

const App = () => (
    <MuiThemeProvider>
        <MusicList lv={level} is_srandom={is_srandom} />
    </MuiThemeProvider>
);

// TODO: 記録編集機能を実装
ReactDOM.render(
    <App />,
    document.getElementById('content')
);
