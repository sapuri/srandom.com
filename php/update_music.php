<?php
/* S乱クリア難易度表CSVとMySQLを同期 */

/* ---------- パラメータ設定 ---------- */
// CSVファイルのパス
$filePath = "../../csv/srandom.csv";

// 難易度表の最大レベル
$max_lv = 17;

// データベースのテーブル名
$table_name = 'main_music';

// 追加例外曲リスト
$exceptionMusicList = array(
    '&quot;Schall&quot; we step?',   // "Schall" we step?
    '混乱少女?そふらんちゃん!!',         // 混乱少女♥そふらんちゃん!!
    'good night mommy',              // good night, mommy
);
/* ---------- /パラメータ設定 ---------- */


// 設定ファイルの読み込み
require_once('./config.php');
require_once('./functions.php');

// データベースに接続
$dbh = connectDb();
date_default_timezone_set('Asia/Tokyo');


/* ---------- 関数定義 ---------- */
/**
 * CSVを配列に格納する
 * @param string|$filePath  - CSVファイルのパス
 * @return array|$data      - CSVのデータを格納した配列
 */
/*
function csv2arr($filePath) {
    // ファイル取得
    $file = new SplFileObject($filePath);
    $file->setFlags(SplFileObject::READ_CSV);

    // ファイル内のデータループ
    foreach ($file as $key => $line) {
        // 空行はスキップ
        if (is_null($line[0])) continue;

        foreach ($line as $str) {
            // 文字コードをUTF-8に変換
            mb_convert_variables('UTF-8', 'SJIS-win', $str);
            // データを配列に格納
            $data[$key][] = $str;
        }
    }

    return $data;
}
*/

/**
 * CSVをMySQLにINSERTする
 * @param $dbh                  - データベースハンドラ
 * @param string|$table_name    - データベーステーブル名
 * @param string|$filePath      - CSVファイルのパス
 * @param int|$max_lv           - 難易度表の最大レベル
 */
function csv2mysql($dbh, $table_name, $filePath, $max_lv, $exceptionMusicList) {
    // ファイル取得
    $file = new SplFileObject($filePath);
    $file->setFlags(SplFileObject::READ_CSV);

    // Lv別のINSERTデータ格納用
    $ins_values = "";

    $lv = $max_lv;
    $is_loop_first = true;
    /* 行ごとにループ */
    foreach ($file as $key => $line) {
        /* LvごとにまとめてINSERTする */

        // 1行目はスキップ
        if ($is_loop_first) {
            $is_loop_first = false;
            continue;
        }

        // 空行はスキップ
        if (is_null($line[0])) continue;

        // Lvを含む行の処理
        if (strstr($line[0], 'Lv')) {
            if ($lv == $max_lv) {
                $lv--;
                continue;
            }

            // INSERTデータをデータベースに格納
            insertValues($dbh, $table_name, $max_lv, $lv, $ins_values, $exceptionMusicList);

            // Lv別のINSERTデータ格納配列を初期化
            $ins_values = "";
            $lv--;
            continue;
        }

        // 1行ごとのINSERTデータ格納用
        $line_values = "";

        /* カラムごとにループ */
        foreach ($line as $line_key => $str) {
            // カンマを追加
            if ($line_key > 0) {
                $line_values .= ",";
            }

            // 文字コードをUTF-8に変換
            mb_convert_variables('UTF-8', 'SJIS-win', $str);

            // 曲名と難易度を分割
            $str = splitDifficulty($str);

            // INSERT用データ作成
            $line_values .= $str;
        }

        // カンマを追加
        if (!empty($ins_values)) {
            $ins_values .= ",";
        }

        // 行データをINSERTデータに追加
        $ins_values .= $line_values;
    }

    // INSERTデータをデータベースに格納 (最後のレベル)
    insertValues($dbh, $table_name, $max_lv, $lv, $ins_values, $exceptionMusicList);
}

/**
 * 曲名と難易度を分割
 * @param string|$str   - 分割対象の文字列
 * @return string|$str  - 分割した文字列
 */
function splitDifficulty($str) {
    if ($title = mb_strstr($str, '(EX)', true)) {
        $str = $title . "," . "EXTRA";
    } elseif ($title = mb_strstr($str, '(H)', true)) {
        $str = $title . "," . "HYPER";
    } elseif ($title = mb_strstr($str, '(N)', true)) {
        $str = $title . "," . "NORMAL";
    } elseif ($title = mb_strstr($str, '(E)', true)) {
        $str = $title . "," . "EASY";
    }
    return $str;
}

/**
 * 指定した数ごとに配列を分割
 * @param array|$arr        - 分割対象の配列
 * @param int|$num          - 何個ごとに分割させるか
 * @return array|$new_arr   - 分割した配列
 */
function splitArray($arr, $num) {
    $count = 0;
    foreach ($arr as $key => $value) {
        $index = $key % $num;  // 0, 1, 2, 3
        $new_arr[$count][$index] = $value;
        if ($index == $num - 1) {
            $count++;
        }
    }
    return $new_arr;
}

/**
 * INSERTデータをデータベースに格納
 * @param $dbh                         - データベースハンドラ
 * @param string|$table_name           - データベーステーブル名
 * @param int|$max_lv                  - 難易度表の最大レベル
 * @param int|$lv                      - 参照中のレベル
 * @param string|$ins_values           - INSERTデータ
 * @param array|$exceptionMusicList    - 追加例外曲リスト
 */
function insertValues($dbh, $table_name, $max_lv, $lv, $ins_values, $exceptionMusicList) {
    // ','で分割
    $ins_values = explode(',', $ins_values);

    // 曲単位に配列を分割
    $music = splitArray($ins_values, 4);

    // INSERTする値を外部キーに変換 (S乱レベルも配列に格納)
    $music = convert2ForeignKey($max_lv, $lv+1, $music);

    /* 曲の要素ごとにループ */
    foreach ($music as $element) {
        // 追加例外曲リストに含まれていればスキップ
        if (isExceptionMusicList($exceptionMusicList, $element[2])) {
            // echo '追加例外曲をスキップしました: ', $element[2], "<br>\n";
            continue;
        }

        // 曲が重複していれば更新
        if ($music_id = getMusicId($dbh, $table_name, $element[2], $element[3])) {
            // UPDATE処理
            if (update_music($dbh, $table_name, $element[2], $element[4], $element[3], $element[1], $element[0], $music_id)) {
                // 変更されたら更新内容を表示
                if ($element[3] == 1) {
                    $difficulty = 'EX';
                } elseif ($element[3] == 2) {
                    $difficulty = 'H';
                } elseif ($element[3] == 3) {
                    $difficulty = 'N';
                } elseif ($element[3] == 4) {
                    $difficulty = 'E';
                } else {
                    $difficulty = $element[3];
                }
                $sran_level = $max_lv - $element[0] + 1;
                $level = 50 - $element[1] + 1;
                echo "$music_id: ", $element[2], "(", $difficulty, ") を ", "S乱レベル: $sran_level ", "レベル: $level ", "BPM: $element[4] に更新しました。\n";
            }
            continue;
        }

        // INSERT処理
        insert_music($dbh, $table_name, $element[2], $element[4], $element[3], $element[1], $element[0]);

        // 結果表示
        $music_id = getMusicId($dbh, $table_name, $element[2], $element[3]);
        if ($element[3] == 1) {
            $difficulty = 'EX';
        } elseif ($element[3] == 2) {
            $difficulty = 'H';
        } elseif ($element[3] == 3) {
            $difficulty = 'N';
        } elseif ($element[3] == 4) {
            $difficulty = 'E';
        } else {
            $difficulty = $element[3];
        }
        echo "$music_id: ", $element[2], "(", $difficulty, ") を追加しました。\n";
    }
}

/**
 * INSERTする値を外部キーに変換
 * @param int|$max_lv           - 難易度表の最大レベル
 * @param int|$sran_level       - S乱レベル
 * @param array|$music          - 変換対象の配列
 * @return array|$converted     - 変換した値を格納した配列
 */
function convert2ForeignKey($max_lv, $sran_level, $music) {
    // 変換した値を格納する配列
    $converted = array();

    // S乱レベルのID
    $sran_level_id = $sran_level;

    foreach ($music as $key => $element) {
        // レベルのID
        $element[0] = 50 - $element[0] + 1;

        // 難易度のID
        if ($element[2] === 'EXTRA') {
            $element[2] = 1;
        } elseif ($element[2] === 'HYPER') {
            $element[2] = 2;
        } elseif ($element[2] === 'NORMAL') {
            $element[2] = 3;
        } elseif ($element[2] === 'EASY') {
            $element[2] = 4;
        } else {
            echo '不正な難易度です: ', $element[2], "\n";
            echo '曲名: ', $element[1];
            exit(1);
        }

        // 変換した値を配列に格納
        $converted[$key][0] = $sran_level_id;   // S乱レベルID
        $converted[$key][1] = $element[0];      // レベルID
        $converted[$key][2] = $element[1];      // 曲名
        $converted[$key][3] = $element[2];      // 難易度ID
        $converted[$key][4] = $element[3];      // BPM
    }

    return $converted;
}

/**
 * 曲名と難易度IDを指定すると曲IDを返す
 * @param $dbh                  - データベースハンドラ
 * @param string|$table_name    - データベーステーブル名
 * @param string|$title         - 曲名
 * @param int|$difficulty_id    - 難易度ID
 * @return int|$music_id        - 曲ID
 */
function getMusicId($dbh, $table_name, $title, $difficulty_id) {
    try {
        $sql = "SELECT `id`, `title`, `difficulty_id` FROM `$table_name` WHERE `title` = :title AND `difficulty_id` = :difficulty_id LIMIT 1";
        $stmt = $dbh->prepare($sql);
        $stmt->execute(array(":title"=>$title, ":difficulty_id"=>$difficulty_id));
        $music_id = (int)$stmt->fetchColumn();
    } catch (Exception $e) {
        echo '参照処理で例外が発生: ', $e->getMessage(), "\n";
        exit(1);
    }
    return $music_id;
}

/**
 * 曲が追加例外曲リストに含まれているかを判定
 * @param array|$exceptionMusicList    - 追加例外曲リスト
 * @param string|$title                - 曲名
 * @return boolean                     - 追加例外曲リストに含まれている: True / 含まれていない: False
 */
function isExceptionMusicList($exceptionMusicList, $title) {
    foreach ($exceptionMusicList as $exceptionMusic) {
        if ($title === $exceptionMusic) return True;
    }
    return False;
}

/**
 * 曲のINSERT処理
 * 新規楽曲情報を追加する
 * @param $dbh                  - データベースハンドラ
 * @param string|$table_name    - データベーステーブル名
 * @param string|$title         - 曲名
 * @param string|$bpm           - BPM
 * @param int|$difficulty_id    - 難易度
 * @param int|$level_id         - レベル
 * @param int|$sran_level_id    - S乱レベル
 */
function insert_music($dbh, $table_name, $title, $bpm, $difficulty_id, $level_id, $sran_level_id) {
    try {
        $sql = "INSERT INTO `$table_name`(`title`, `bpm`, `difficulty_id`, `level_id`, `sran_level_id`) VALUES(?, ?, ?, ?, ?)";
        $stmt = $dbh->prepare($sql);
        $stmt->execute(array($title, $bpm, $difficulty_id, $level_id, $sran_level_id));
    } catch (Exception $e) {
        echo 'INSERT処理で例外が発生: ', $e->getMessage(), "\n";
        exit(1);
    }
}

/**
 * 曲のUPDATE処理
 * 既に登録されている曲情報を更新する
 * @param $dbh                  - データベースハンドラ
 * @param string|$table_name    - データベーステーブル名
 * @param string|$title         - 曲名
 * @param string|$bpm           - BPM
 * @param int|$difficulty_id    - 難易度
 * @param int|$level_id         - レベル
 * @param int|$sran_level_id    - S乱レベル
 * @param int|$music_id         - 曲ID
 * @return int|$count           - 変更された行数(0, 1)
 */
function update_music($dbh, $table_name, $title, $bpm, $difficulty_id, $level_id, $sran_level_id, $music_id) {
    try {
        $sql = "UPDATE `$table_name` SET `title` = ?, `bpm` = ?, `difficulty_id` = ?, `level_id` = ?, `sran_level_id` = ? WHERE `id` = ?";
        $stmt = $dbh->prepare($sql);
        $stmt->execute(array($title, $bpm, $difficulty_id, $level_id, $sran_level_id, $music_id));
        // UPDATEで変更された行数を返す
        $count = $stmt->rowCount();
        return $count;
    } catch (Exception $e) {
        echo 'UPDATE処理で例外が発生: ', $e->getMessage(), "\n";
        exit(1);
    }
}
/* ---------- /関数定義 ---------- */


/* --------- Main ---------- */
// CSVとMySQLを同期
csv2mysql($dbh, $table_name, $filePath, $max_lv, $exceptionMusicList);

echo 'Done!';
