<?php
/* 都道府県をMySQLに挿入 */

/* ---------- パラメータ設定 ---------- */
// 都道府県リスト
$location_list = array(
    '北海道',
    '青森県',
    '岩手県',
    '宮城県',
    '秋田県',
    '山形県',
    '福島県',
    '茨城県',
    '栃木県',
    '群馬県',
    '埼玉県',
    '千葉県',
    '東京都',
    '神奈川県',
    '山梨県',
    '長野県',
    '新潟県',
    '富山県',
    '石川県',
    '福井県',
    '岐阜県',
    '静岡県',
    '愛知県',
    '三重県',
    '滋賀県',
    '京都府',
    '大阪府',
    '兵庫県',
    '奈良県',
    '和歌山県',
    '鳥取県',
    '島根県',
    '岡山県',
    '広島県',
    '山口県',
    '徳島県',
    '香川県',
    '愛媛県',
    '高知県',
    '福岡県',
    '佐賀県',
    '長崎県',
    '熊本県',
    '大分県',
    '宮崎県',
    '鹿児島県',
    '沖縄県',
    '韓国',
    '海外'
);

// データベースのテーブル名
$table_name = 'users_location';
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
 * @param array|$location_list      - 都道府県リスト
 */
function insertLocation($dbh, $table_name, $location_list) {
    if (getSomethingId($dbh, $table_name)) {
        echo '既に', $table_name, 'に都道府県が存在します。';
        exit(0);
    }

    try {
        $sql = "INSERT INTO $table_name(`location`) VALUES(:location)";
        $stmt = $dbh->prepare($sql);
        foreach ($location_list as $location) {
            echo "INSERT INTO $table_name(`location`) VALUES($location)", '<br>';
            $stmt->execute(array(":location"=>$location));
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
// 都道府県をMySQLに挿入
insertLocation($dbh, $table_name, $location_list);

echo '都道府県を', $table_name, 'に挿入しました！';
