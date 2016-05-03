<?php
/* ポップンS乱クリア難易度表からデータを収集してCSVとして出力 */

// ライブラリ読み込み
require_once('simple_html_dom.php');

// URLを設定
$url1 = 'http://hellwork.jp/popn/wiki/734.html';	// S乱クリア難易度表
$url2 = 'http://hellwork.jp/popn/wiki/?%E3%81%9D%E3%81%AE%E4%BB%96%2FS%E4%B9%B1Lv0%E9%9B%A3%E6%98%93%E5%BA%A6%E8%A1%A8';

// 出力するCSVのファイル名を設定
$fileName = '../csv/srandom.csv';

// CSVのカラム名を設定
$columnName = array('レベル', '曲名', 'BPM');


/* ---------- 関数定義 ---------- */
/**
 * ポップン難易度表からデータを収集する (simple_html_dom.php を使用)
 * @param string $url		スクレイピング対象のURL
 * @return array $csv_data	CSVに書き込むデータ
 */
function scrapeHtml($url) {
	/* Lv4〜Lv17を取得 */

	// HTMLを取得
	$html = file_get_html($url);

	// データ格納用配列を定義
	$lv = array();
	$music_lv = array();
	$music_name = array();
	$music_bpm = array();
	$csv_data = array();

	$lv_num = 0;	// Lvごとに番地を指定

    // #content_1_4 〜 #content_1_17 を指定
    for ($i = 4; $i <= 17; $i++) {
		// Lv15.5をスキップ
		// if ($i == 6) continue;

		// Lv表記を探索
        $content = $html->find("h3#content_1_$i", 0);
		$h3 = $content->plaintext;
		// Lv表記部分のみを取り出す
		preg_match('/Lv[0-9]+(.[1-9])?/', $h3, $h3);
		// Lv表記が見つからなければ強制終了
		if (empty($h3)) {
			echo 'Lv表記が見つかりませんでした。';
			exit(1);
		}
		// Lv表記を配列に格納
		$lv[] = $h3[0];
		echo $h3[0], '<br>';

        // $content 直下の div.table-responsive 以下を指定
		$tr_address = 0;	// <tr>の場所を指定
		// 全ての<tr>を走査
		while (1) {
			// div.table-responsive(2~17)->table->tbody->tr
			$tr = $html->find('div.table-responsive', $i-3)->children(0)->children(0)->children($tr_address);
			// <tr>が存在しなければループを抜ける
			if (!isset($tr)) break;
			// tr->td
			$music_lv[$lv_num][$tr_address] = $tr->children(0)->plaintext;
			// tr->td->span->a
			$music_name[$lv_num][$tr_address] = $tr->children(1)->children(0)->children(0)->plaintext;
			echo $music_name[$lv_num][$tr_address], '<br>';
			// tr->td
			$music_bpm[$lv_num][$tr_address] = $tr->children(2)->plaintext;
			// 次の<tr>を指定
			$tr_address++;
		}
		$lv_num++;	// 次のLvを指定
    }
	$html->clear();	// メモリ解放

	// 収集したデータを配列に格納 (先頭、末尾の空白を除去)
	try {
		$lv_num = 0;
		foreach ($lv as $row) {
			$line = 0;	// CSVの行を指定
			$csv_data[$lv_num][$line][0] = $row;	// Lvを格納
			$line++;
			for ($music_num = 0; $music_num < count($music_lv[$lv_num]); $music_num++) {
				$csv_data[$lv_num][$line][0] = trim($music_lv[$lv_num][$music_num]);
				$csv_data[$lv_num][$line][1] = trim($music_name[$lv_num][$music_num]);
				$csv_data[$lv_num][$line][2] = trim($music_bpm[$lv_num][$music_num]);
				$line++;
			}
			$lv_num++;
		}
	} catch (Exception $e) {
		echo '収集したデータを配列に格納できませんでした: ', $e;
		exit(1);
	}
	return $csv_data;
}

/**
 * ポップン難易度表からデータを収集する (simple_html_dom.php を使用)
 * @param string $url		スクレイピング対象のURL
 * @return array $csv_data	CSVに書き込むデータ
 */
function scrapeHtml2($url) {
	/* Lv1〜Lv3を取得 */

	// HTMLを取得
	$html = file_get_html($url);

	// データ格納用配列を定義
	$lv = array();
	$music_lv = array();
	$music_name = array();
	$music_bpm = array();
	$csv_data = array();

	$lv_num = 0;	// Lvごとに番地を指定

    // #content_1_1 〜 #content_1_5 を指定
    for ($i = 1; $i <= 5; $i++) {
		if ($i == 2) $h3 = 'Lv2';		// Lv2強
		elseif ($i == 3) $h3 = 'Lv2';	// Lv2弱
		elseif ($i == 4) $h3 = 'Lv1';	// Lv1強
		elseif ($i == 5) $h3 = 'Lv1';	// Lv1弱
		else {
			// Lv表記を探索
	        $content = $html->find("h3#content_1_$i", 0);
			$h3 = $content->plaintext;
			// Lv表記部分のみを取り出す
			// preg_match('/Lv[0-9]+(.[1-9])?/', $h3, $h3_ed);
			preg_match('/Lv[0-9]+(.[1-9])?/', $h3, $h3);
			$h3 = $h3[0];
			// Lv表記が見つからなければ強制終了
			if (empty($h3)) {
				echo 'Lv表記が見つかりませんでした。';
				exit(1);
			}
		}
		// Lv表記を配列に格納
		if ($i != 3 && $i != 5) {
			// '弱'の時はLv表記を格納しない
			$lv[] = $h3;
			echo $h3, '<br>';
		}

        // $content 直下の div.table-responsive 以下を指定
		if ($i != 3 && $i != 5) {
			// '弱'の時はスキップして追記
			$arr_address = 0;	// 配列のアドレスを指定
		}

		$tr_address = 0;	// <tr>の場所を指定
		// 全ての<tr>を走査
		while (1) {
			// div.table-responsive(1~5)->table->tbody->tr
			$tr = $html->find('div.table-responsive', $i-1)->children(0)->children(0)->children($tr_address);
			// <tr>が存在しなければループを抜ける
			if (!isset($tr)) break;
			// tr->td
			$music_lv[$lv_num][$arr_address] = $tr->children(0)->plaintext;
			// tr->td->span->a
			$music_name[$lv_num][$arr_address] = $tr->children(1)->children(0)->children(0)->plaintext;
			echo $music_name[$lv_num][$arr_address], '<br>';
			// tr->td
			$music_bpm[$lv_num][$arr_address] = $tr->children(2)->plaintext;
			// 次の<tr>を指定
			$tr_address++;
			// 次の配列のアドレスを指定
			$arr_address++;
		}
		if ($i != 2 && $i != 4) {
			// '強'の時はレベルを変えない
			$lv_num++;	// 次のLvを指定
		}
    }
	$html->clear();	// メモリ解放

	// 収集したデータを配列に格納 (先頭、末尾の空白を除去)
	$lv_num = 0;
	foreach ($lv as $row) {
		$line = 0;	// CSVの行を指定
		$csv_data[$lv_num][$line][0] = $row;	// Lvを格納
		$line++;
		for ($music_num = 0; $music_num < count($music_lv[$lv_num]); $music_num++) {
			$csv_data[$lv_num][$line][0] = trim($music_lv[$lv_num][$music_num]);
			$csv_data[$lv_num][$line][1] = trim($music_name[$lv_num][$music_num]);
			$csv_data[$lv_num][$line][2] = trim($music_bpm[$lv_num][$music_num]);
			$line++;
		}
		$lv_num++;
	}
	return $csv_data;
}

/**
 * 収集したデータをCSVに出力する
 * @param array $csv_data		CSVに書き込むデータ
 * @param string $fileName		出力するCSVのファイル名
 * @param string $columnName	CSVのカラム名
 * @param boolean $append		True: appendモード / False: writeモード
 */
function arr2csv($csv_data, $fileName, $columnName, $append = False) {
	if ($append === False) {
		/* writeモード */
		// CSV読み込み
		$fp = fopen($fileName, "w");

		// カラム名を出力
		mb_convert_variables('SJIS-win', 'UTF-8', $columnName);
		fputcsv($fp, $columnName);
	} else {
		/* appendモード */
		// CSV読み込み
		$fp = fopen($fileName, "a");
	}

	// 取得したデータを出力
	foreach ($csv_data as $lines) {
		foreach ($lines as $line) {
			mb_convert_variables('SJIS-win', 'UTF-8', $line);
			fputcsv($fp, $line);
		}
	}

	// ファイルクローズ
	fclose($fp);
}
/* ---------- 関数定義終了 ---------- */

// データを収集して配列に格納
$csv_data = scrapeHtml($url1);

// データを収集して配列に格納
$csv_data2 = scrapeHtml2($url2);

// CSVに出力
try {
	arr2csv($csv_data, $fileName, $columnName);
} catch (Exception $e) {
	echo 'CSV出力に失敗: ', $e;
}

// CSVに追加出力
try {
	arr2csv($csv_data2, $fileName, $columnName, $append = True);
} catch (Exception $e) {
	echo 'CSV追加出力に失敗: ', $e;
}

echo 'Done!';
