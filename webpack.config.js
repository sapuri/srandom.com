var path = require('path');
var webpack = require('webpack');
var commonsPlugin = new webpack.optimize.CommonsChunkPlugin('common.js');

module.exports = {
    /* ビルドの起点となるファイルの設定 */
    entry: {
        index: './static/react/src/index.jsx',
        level_select: './static/react/src/level_select.jsx',
        difflist: './static/react/src/difflist.jsx'
    },
    /* 出力されるファイルの設定 */
    output: {
        path: path.join(__dirname, 'static/react/assets'), // 出力先の絶対パス
        filename: '[name].js'                              // 出力先のファイル名
    },
    devtool: 'inline-source-map', // ソースマップをファイル内に出力
    module: {
        /* loader の設定 */
        loaders: [
            {
                test: /\.jsx$/,          // 対象となるファイルの拡張子 (正規表現可)
                exclude: /node_modules/, // 除外するファイル/ディレクトリ (正規表現可)
                loader: 'babel-loader'   // 使用する loader
            }
        ]
    },
    resolve: {
        extensions: ['', '.js', '.jsx']
    },
    plugins: [commonsPlugin]
};
