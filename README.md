# srandom.com
スパランドットコム - ポップンミュージックのスパラン愛好家のためのクリア状況管理サイト

## 環境
* Python 3.5
* Django 1.10
* MySQL 5.6

## コマンド
Django のコマンド機能を利用したコマンドの一覧です。

### データ移行
移行元ユーザーの全てのクリアデータを移行先ユーザーに移行します。

移行元ユーザーのクリアデータは復元できません。

```
python manage.py data_migration <移行元のユーザ名> <移行先のユーザ名>
```

### CSVエクスポート
プレミアムユーザーのクリアデータをそれぞれCSVファイルで出力します。

/csv/export/<ユーザー名>.csv に出力されます。

通常は cron で実行されます。

```
python manage.py export2csv
```

### ユーザアカウント削除
指定したユーザアカウントを無効化し、クリアデータを完全に削除します。

クリアデータは復元できません。

```
python manage.py delete_account <username>
```
