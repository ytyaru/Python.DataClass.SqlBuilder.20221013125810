PythonでORMっぽいのを書いてみる

　DataClassでクラス定義とアノテーションからSQL文を作りたい。

<!-- more -->

# 問題

* DataClassの型変換
	* 日付型
		* Pythonのdatetime.fromisoformat()では末尾`Z`の日時が変換できない
		* SQLite3の日付は末尾`Z`が基本
		* ISO8601の仕様でも末尾`Z`が基本

　`+00:00`なら`Z`と同じ意味になるし`datetime.fromisoformat()`でも変換できる。でも`-00:00`とも書けるし、`+00:00:00.000`とも書ける。つまり表記ゆれがある。

　外部からISO文字列で日付を取得するとき、以下のように変換しないといけない。

```python
iso = '2000-01-01T00:00:00Z'
pyiso = iso.replace('Z', '+00:00')
```

　ISO仕様を満たしていないくせにISOを名乗るのはどうかと思うよPythonさん。

