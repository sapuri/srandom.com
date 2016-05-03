<?php
/* 難易度をMySQLに挿入 */

/* ---------- パラメータ設定 ---------- */
$difficulty_list = array(
    'EXTRA',
    'HYPER',
    'NORMAL',
    'EASY'
);

// データベースのテーブル名
$table_name = 'main_difficulty';
/* ---------- /パラメータ設定 ---------- */


// 設定ファイルの読み込み
require_once('./config.php');
require_once('./functions.php');

// データベースに接続
$dbh = connectDb();


/* ---------- 関数定義 ---------- */
/**
 * 難易度を挿入
 * @param $dbh                      - データベースハンドラ
 * @param string|$table_name        - データベーステーブル名
 * @param array|$difficulty_list    - 難易度リスト
 */
function insertDifficulty($dbh, $table_name, $difficulty_list) {
    if (getSomethingId($dbh, $table_name)) {
        echo '既に', $table_name, 'にレベルが存在します。';
        exit(0);
    }

    try {
        $sql = "INSERT INTO $table_name(`difficulty`) VALUES(:difficulty)";
        $stmt = $dbh->prepare($sql);
        foreach ($difficulty_list as $difficulty) {
            echo "INSERT INTO $table_name(`difficulty`) VALUES($difficulty)", '<br>';
            $stmt->execute(array(":difficulty"=>$difficulty));
        }
    } catch (Exception $e) {
        echo 'INSERT処理で例外が発生: ', $e->getMessage(), "\n";
        exit(1);
    }
}

/**
 * 何か適当にIDを取得
 * @param $dbh                  - データベースハンドラ
 * @param string|$table_name    - データベーステーブル名
 * @return int|$id              - 取得したID
 */
function getSomethingId($dbh, $table_name) {
    try {
        $sql = "SELECT `id` FROM $table_name LIMIT 1";
        $stmt = $dbh->prepare($sql);
        $stmt->execute();
        if ($id = (int)$stmt->fetchColumn()) return $id;
        else return 0;
    } catch (Exception $e) {
        echo '参照処理で例外が発生: ', $e->getMessage(), "\n";
        exit(1);
    }
}
/* ---------- /関数定義 ---------- */


/* --------- Main ---------- */
// 難易度をMySQLに挿入
insertDifficulty($dbh, $table_name, $difficulty_list);

echo '難易度を', $table_name, 'に挿入しました！';
