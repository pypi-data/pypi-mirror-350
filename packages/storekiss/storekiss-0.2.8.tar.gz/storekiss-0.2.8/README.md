# storekiss LiteStore v0.2.7


SQLiteストレージを使用したNoSQL DB。シンプルで使いやすいNoSQL likeなAPIを提供します。

## 最新の更新（v0.2.7）

- バッチ処理の改善: テーブル存在確認、例外処理、ログ出力、リトライメカニズムを追加
- Firestore互換性の向上: `doc.reference.update()`メソッドが正常に動作するように改善
- デバッグ出力の削除: コード内のすべてのデバッグ用print文を削除
- コード品質の向上: lint警告やエラーを修正
- データベースの安定性向上: デフォルトでファイルベースのDBを使用

## 特徴

- シンプルなCRUD（Create, Read, Update, Delete）インターフェース
- SQLiteベースの物理ストレージ
- NoSQL likeなコレクションとドキュメントの使用
- Pythonネイティブの辞書型をデータ構造として使用
- モジュール固有の例外処理

## SQLiteストレージ構造

storekiss LiteStoreは以下の構造でSQLiteを物理ストレージメカニズムとして使用しています：

1. **データベース構成**:
   - 各コレクションはSQLiteデータベース内の個別のテーブルとして保存
   - 各ドキュメントは対応するテーブルの行として保存
   - ドキュメントデータはTEXTカラムにJSONとして保存
   - ドキュメントIDは別のカラムに保存され、高速検索のためにインデックス化

2. **スキーマ実装**:
   - SQLiteテーブル構造はコレクション名に基づいて動的に作成
   - 各テーブルには主に2つのカラム: `id` (TEXT) と `data` (TEXT)
   - `id`カラムは主キーであり、高速検索のためにインデックス化
   - `data`カラムはドキュメント全体をJSON文字列として保存

3. **インデックス作成**:
   - フィールドがインデックス付きとしてマークされると、SQLite JSON1拡張機能を使用してインデックスを作成
   - インデックスはJSON_EXTRACT式に対して`CREATE INDEX`を使用して作成
   - これによりJSON内の特定フィールドに対する効率的なクエリが可能

4. **クエリ実行**:
   - クエリはSQLite JSON1拡張機能を使用してSQLに変換
   - フィルタはJSON_EXTRACTを使用してネストされたフィールドにアクセス
   - ソートはJSON_EXTRACT式に対するORDER BYで実装
   - ページネーションはLIMITとOFFSETで実装

5. **トランザクションサポート**:
   - すべての操作はSQLiteトランザクション内で実行
   - これによりデータの一貫性とACID準拠を確保

この構造により、ドキュメントデータベースの柔軟性とSQLiteの信頼性のバランスが取れています。

## SQLiteの高速利用

LiteStoreはSQLiteを高速に利用するために以下の最適化を行っています：

1. **インデックス最適化**:
   - 主キー（ドキュメントID）に対する自動インデックス作成
   - JSON1拡張機能を使用した特定フィールドへのインデックス作成
   - 複合インデックスのサポートによる複数条件クエリの高速化

2. **クエリ最適化**:
   - プリペアドステートメントの使用によるSQLインジェクション防止と実行速度向上
   - JSON_EXTRACTを使用した効率的なJSONフィールドアクセス
   - 必要なフィールドのみを抽出するプロジェクション最適化

3. **キャッシュ戦略**:
   - SQLiteのページキャッシュを活用した読み取り操作の高速化
   - トランザクション内でのバッチ処理による書き込み操作の最適化
   - 頻繁にアクセスされるデータのメモリ内キャッシュ

4. **ストレージ最適化**:
   - 効率的なJSONシリアライズ/デシリアライズ
   - バイナリデータの適切な処理
   - 大規模データセットのための段階的なロード機能

5. **パフォーマンスチューニング**:
   - WALモード（Write-Ahead Logging）の使用によるトランザクションの並行性向上
   - 適切なページサイズとキャッシュサイズの設定
   - 定期的なVACUUMによるデータベースファイルの最適化

これらの最適化により、storekissは小〜中規模のアプリケーションで優れたパフォーマンスを発揮します。

## インストール

```bash
pip install storekiss
```

または Poetry を使用:

```bash
poetry add storekiss
```

## クイックスタート例

### 1. 基本的なCRUD操作

```python
from storekiss import litestore

# クライアントの作成（デフォルトではインメモリSQLiteを使用）
db = litestore.client()

# アイテムの作成
item = db.create({"name": "テストアイテム", "value": 42})
print(f"作成されたアイテムのID: {item['id']}")

# アイテムの読み取り
retrieved = db.read(item["id"])
print(f"取得結果: {retrieved}")

# アイテムの更新
updated = db.update(item["id"], {"value": 100})
print(f"更新結果: {updated}")

# アイテムの削除
db.delete(item["id"])
print("アイテムが削除されました")
```

### 2. NoSQL likeなコレクションとドキュメントの使用

```python
from storekiss import litestore

# クライアントの作成
db = litestore.client()

# コレクションリファレンスの取得
users = db.collection("users")

# 自動IDでドキュメントを追加
user = users.add({
    "name": "山田太郎",
    "email": "yamada@example.com",
    "age": 30
})

# ドキュメントリファレンスの取得
doc = users.doc(user["id"])

# ドキュメントの更新
doc.update({"status": "active"})

# ドキュメントの削除
doc.delete()

# NoSQL likeなクエリ構文
active_users = users.where("status", "==", "active").get()
adult_users = users.where("age", ">=", 20).get()
```

### 3. スキーマによるデータ検証

```python
from storekiss import litestore
from storekiss.validation import Schema, StringField, NumberField, BooleanField

# スキーマの定義
user_schema = Schema({
    "name": StringField(required=True, min_length=2),
    "age": NumberField(required=True, min_value=0, integer_only=True),
    "email": StringField(required=True),
    "active": BooleanField(required=False)
})

# スキーマ検証付きのストアを作成
db = litestore.client(schema=user_schema, collection="users")

# データは保存前に検証されます
user = db.create({
    "name": "山田太郎",
    "age": 30,
    "email": "yamada@example.com",
    "active": True
})
```

### 4. 自動タイムスタンプ

```python
from storekiss import litestore, SERVER_TIMESTAMP

# ストアの作成
db = litestore.client()

# コレクションの取得
posts = db.collection("posts")

# 自動タイムスタンプ付きでドキュメントを作成
post = posts.add({
    "title": "最初の投稿",
    "content": "これは最初の投稿の内容です",
    "created_at": SERVER_TIMESTAMP,  # 自動的に現在時刻が設定される
    "updated_at": SERVER_TIMESTAMP   # 自動的に現在時刻が設定される
})

# 自動タイムスタンプ付きでドキュメントを更新
doc = posts.doc(post["id"])
updated = doc.update({
    "content": "更新された内容",
    "updated_at": SERVER_TIMESTAMP  # updated_atのみが現在時刻に変更される
})
```

### 5. 高度なクエリ

```python
from storekiss import litestore
from datetime import datetime, timedelta

# クライアントの作成
db = litestore.client()

# コレクションの取得
products = db.collection("products")

# テストデータの追加
now = datetime.now()
yesterday = now - timedelta(days=1)
last_week = now - timedelta(days=7)

products.add({
    "name": "ノートパソコン", 
    "price": 120000, 
    "category": "electronics", 
    "in_stock": True,
    "created_at": now,
    "stock_count": 15
})
products.add({
    "name": "スマートフォン", 
    "price": 80000, 
    "category": "electronics", 
    "in_stock": True,
    "created_at": yesterday,
    "stock_count": 8
})
products.add({
    "name": "ヘッドフォン", 
    "price": 20000, 
    "category": "accessories", 
    "in_stock": False,
    "created_at": last_week,
    "stock_count": 0
})

# 基本的なフィルタ付きクエリ
electronics = products.where("category", "==", "electronics").get()

# 複数フィルタ付きクエリ
available_electronics = products.where("category", "==", "electronics").where("in_stock", "==", True).get()

# ソート付きクエリ
expensive_first = products.order_by("price", direction="DESC").get()

# 制限付きクエリ
top_two = products.order_by("price", direction="DESC").limit(2).get()

# 結果のカウント
count = products.where("in_stock", "==", True).count()

# 数値範囲検索
affordable_products = products.where("price", ">=", 10000).where("price", "<=", 90000).get()
low_stock_items = products.where("stock_count", "<", 10).get()
well_stocked_items = products.where("stock_count", ">", 10).get()

# 時間範囲検索
recent_products = products.where("created_at", ">=", yesterday).get()
older_products = products.where("created_at", "<", yesterday).get()
last_week_products = products.where("created_at", ">=", last_week).where("created_at", "<", yesterday).get()

# 複合条件クエリ（数値範囲と時間範囲の組み合わせ）
recent_affordable = products.where("created_at", ">=", yesterday).where("price", "<", 100000).get()
```

## 使用方法

### 基本的な使用方法

```python
from storekiss import litestore

# クライアントの作成（デフォルトではインメモリSQLiteを使用）
db = litestore.client()

# アイテムの作成
item = db.create({"name": "テストアイテム", "value": 42})
print(f"作成されたアイテムのID: {item['id']}")

# アイテムの読み取り
retrieved = db.read(item["id"])
print(f"取得結果: {retrieved}")

# アイテムの更新
updated = db.update(item["id"], {"value": 100})
print(f"更新結果: {updated}")

# アイテムの削除
db.delete(item["id"])
print("アイテムが削除されました")
```

### ファイルベースのデータベースの使用

```python
# ファイルベースのSQLiteデータベースでストアを作成
db = litestore.client(db_path="my_database.db", collection="items")
```

### スキーマ検証の使用

```python
from storekiss import litestore
from storekiss.validation import Schema, StringField, NumberField, BooleanField

# スキーマの定義
user_schema = Schema({
    "name": StringField(required=True, min_length=2),
    "age": NumberField(required=True, min_value=0, integer_only=True),
    "email": StringField(required=True),
    "active": BooleanField(required=False)
})

# スキーマ検証付きのストアを作成
db = litestore.client(schema=user_schema, collection="users")

# データは保存前に検証されます
user = db.create({
    "name": "山田太郎",
    "age": 30,
    "email": "yamada@example.com",
    "active": True
})
```

### データのクエリ

```python
# すべてのアイテムをリスト
all_items = db.list()

# ページネーション付きリスト
page = db.list(limit=10, offset=20)

# フィールド値によるクエリ
results = db.query({"city": "東京", "active": True})
```

### ドキュメント数のカウント

LiteStoreはNoSQL likeに、コレクション内のドキュメント数を簡単に取得できる機能を提供します。

```python
from storekiss import litestore

db = litestore.client()
users = db.collection("users")

# コレクション全体のドキュメント数を取得
total_count = users.count()
print(f"ユーザー総数: {total_count}")

# 条件付きカウント（クエリ結果の数）
active_users_count = users.where("status", "==", "active").count()
print(f"アクティブユーザー数: {active_users_count}")

# 複合条件でのカウント
premium_active_count = users.where("status", "==", "active").where("plan", "==", "premium").count()
print(f"プレミアムアクティブユーザー数: {premium_active_count}")

# クライアントレベルでのカウント
total = db.count()
active_count = db.count({"active": True})

# 数値範囲条件でのカウント
expensive_items_count = db.collection("products").where("price", ">", 50000).count()

```

### 数値範囲と時間範囲の検索

```python
from storekiss import litestore
from datetime import datetime, timedelta

db = litestore.client()
events = db.collection("events")

# 現在時刻を基準にした日付
now = datetime.now()
one_hour_ago = now - timedelta(hours=1)
one_day_ago = now - timedelta(days=1)
one_week_ago = now - timedelta(days=7)

# 数値範囲検索の例
high_priority = events.where("priority", ">=", 8).get()
medium_priority = events.where("priority", ">", 3).where("priority", "<", 8).get()
low_cost_events = events.where("cost", "<", 1000).get()

# 時間範囲検索の例
recent_events = events.where("created_at", ">=", one_hour_ago).get()
today_events = events.where("created_at", ">=", one_day_ago).get()
last_week_events = events.where("created_at", ">=", one_week_ago).where("created_at", "<", one_day_ago).get()
future_events = events.where("scheduled_for", ">", now).get()
past_events = events.where("scheduled_for", "<", now).get()

# 複合条件（数値範囲と時間範囲の組み合わせ）
urgent_recent = events.where("priority", ">=", 8).where("created_at", ">=", one_hour_ago).get()
upcoming_low_cost = events.where("scheduled_for", ">", now).where("cost", "<", 1000).get()
```

## エラー処理

このライブラリは異なるエラーシナリオに対してカスタム例外を使用します：

```python
from storekiss import litestore
from storekiss.exceptions import NotFoundError, ValidationError, DatabaseError

db = litestore.client()

try:
    # 存在しないアイテムの読み取りを試みる
    db.read("non-existent-id")
except NotFoundError as e:
    print(f"見つかりません: {e}")

try:
    # 検証に失敗するアイテムの作成を試みる
    db.create({"invalid": "data"})
except ValidationError as e:
    print(f"検証エラー: {e}")

try:
    # データベースエラーの処理
    # （例：データベースファイルにアクセスできない場合）
    db = litestore.client(db_path="/invalid/path/db.sqlite")
except DatabaseError as e:
    print(f"データベースエラー: {e}")
```

## 高度な検証

このライブラリはLiteStoreにインスパイアされた複数のバリデータタイプを提供します：

- `StringField`: オプションの長さ制約付きで文字列を検証
- `NumberField`: オプションの範囲制約付きで数値を検証
- `BooleanField`: ブール値を検証
- `DateTimeField`: datetimeオブジェクトまたはISO形式の文字列を検証
- `ListField`: アイテムのリストを検証
- `MapField`: ネストされたオブジェクトを検証
- `Schema`: 完全なドキュメントを検証

高度な検証の例：

```python
from storekiss.validation import (
    Schema, StringField, NumberField, ListField, MapField
)

# 複雑なスキーマの定義
product_schema = Schema({
    "name": StringField(required=True, min_length=3),
    "price": NumberField(required=True, min_value=0),
    "tags": ListField(
        StringField(),
        required=False,
        min_length=1
    ),
    "dimensions": MapField({
        "width": NumberField(required=True),
        "height": NumberField(required=True),
        "depth": NumberField(required=True)
    }, required=False)
})

# スキーマをストアで使用
db = litestore.client(schema=product_schema, collection="products")
```

## PostgreSQLへの対応に関する考慮事項

LiteStoreはSQLiteをベースにしていますが、将来的にPostgreSQLに対応する場合、以下の点を考慮する必要があります：

1. **アダプタパターンの実装**:
   - データベース操作を抽象化するアダプタレイヤーの導入
   - SQLite固有のコードとPostgreSQL固有のコードを分離
   - 共通インターフェースを通じた両方のデータベースへのアクセス

2. **JSONサポートの違い**:
   - SQLiteのJSON1拡張機能とPostgreSQLのJSONB型の違いに対応
   - クエリ構文の違いを吸収するクエリビルダーの拡張
   - インデックス作成方法の違いに対応

3. **トランザクション処理の違い**:
   - PostgreSQLの高度なトランザクション機能（セーブポイント、分離レベルなど）のサポート
   - 分散トランザクションの可能性
   - ロック戦略の最適化

4. **スケーラビリティの向上**:
   - コネクションプールの実装
   - 非同期操作のサポート
   - 大規模データセットに対する効率的なページネーション

5. **マイグレーション機能**:
   - SQLiteからPostgreSQLへのデータ移行ツール
   - スキーマ変更の自動適用
   - バージョン管理されたマイグレーション

6. **パフォーマンス最適化**:
   - PostgreSQL固有のインデックスタイプ（GIN、GiSTなど）の活用
   - パーティショニングのサポート
   - 統計情報を活用したクエリプランの最適化

7. **セキュリティ強化**:
   - ロールベースのアクセス制御
   - 行レベルのセキュリティ
   - 暗号化オプションの拡張

これらの考慮事項を踏まえることで、SQLiteの軽量さと使いやすさを維持しながら、必要に応じてPostgreSQLの高度な機能とスケーラビリティを活用できるようになります。

## サポートされるデータ型

storekissは以下のデータ型をサポートしています：

| データ型     | 説明                                | Pythonでの対応型例                     |
|-----------|-------------------------------------|--------------------------------------|
| string    | UTF-8 文字列                        | `str`                                |
| boolean   | 真偽値（true / false）                | `bool`                               |
| number    | 整数および浮動小数点数（`int`, `float`） | `int`, `float`                       |
| map       | ネストされたキーと値のペア（JSONオブジェクトに相当）     | `dict`                               |
| array     | 順序付きの値のリスト（異種データを含んでもよい）     | `list`                               |
| null      | 空の値                               | `None`                               |
| timestamp | 日付と時刻（マイクロ秒精度）               | `datetime.datetime`                  |
| geopoint  | 緯度経度を表す地理座標                | `google.cloud.firestore_v1.GeoPoint` |
| reference | NoSQL likeなドキュメントへの参照             | `DocumentReference`                  |
| bytes     | バイナリデータ                             | `bytes`                              |

## ライセンス

MIT






サンプルの一括実行チェック
pytest形式の自動テスト追加
ドキュメント整備
その他（ご要望をお聞かせください）
