<?php
/* レベルをMySQLに挿入 */

/* ---------- パラメータ設定 ---------- */
// レベル範囲
$max_lv = 50;
$min_lv = 1;

// データベースのテーブル名
$table_name = 'main_level';
/* ---------- /パラメータ設定 ---------- */


// 設定ファイルの読み込み
require_once('./config.php');
require_once('./functions.php');

// データベースに接続
$dbh = connectDb();


/* ---------- 関数定義 ---------- */
/**
 * レベルを最大レベルから順に挿入
 * @param $dbh                  - データベースハンドラ
 * @param string|$table_name    - データベーステーブル名
 * @param int|$max_lv           - 最大レベル
 * @param int|$min_lv           - 最小レベル
 */
function insertLevel($dbh, $table_name, $max_lv, $min_lv) {
    if (getSomethingId($dbh, $table_name)) {
        echo '既に', $table_name, 'にレベルが存在します。';
        exit(0);
    }

    try {
        $sql = "INSERT INTO $table_name(`level`) VALUES(:level)";
        $stmt = $dbh->prepare($sql);
        for ($level = $max_lv; $level >= $min_lv; $level--) {
            echo "INSERT INTO $table_name(`level`) VALUES($level)", '<br>';
            $stmt->execute(array(":level"=>$level));
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
// レベルをMySQLに挿入
insertLevel($dbh, $table_name, $max_lv, $min_lv);

echo 'レベルを', $table_name, 'に挿入しました！';
