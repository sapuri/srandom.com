// webpack を読み込む
var webpack = require('webpack');

module.exports = {
    /* ビルドの起点となるファイルの設定 */
    entry: './static/react/src/index.jsx',
    /* 出力されるファイルの設定 */
    output: {
        path: './static/react/dist', // 出力先のパス
        filename: 'bundle.js'  // 出力先のファイル名
    },
    /* ソースマップをファイル内に出力 */
    devtool: 'inline-source-map',
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
    /* プラグインの設定 */
    plugins: [
        /* DefinePlugin の実行 */
        new webpack.DefinePlugin({
            // process.env.NODE_ENV を 'production' に置き換える
            'process.env.NODE_ENV': JSON.stringify('production')
        }),
        /* UglifyJsPlugin の実行 */
        new webpack.optimize.UglifyJsPlugin({
            compress: {
                // 圧縮する時に警告を除去
                warnings: false
            }
        })
    ]
};
