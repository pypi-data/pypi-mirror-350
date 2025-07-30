"""
LiteStore互換のエクスポート/インポート機能

このモジュールは、Google Cloud LiteStoreと互換性のあるフォーマットで
コレクションデータのエクスポートとインポートを行う機能を提供します。
"""

import os
import json
import datetime
import sqlite3
import base64
from typing import Dict, Any
import logging

from storekiss.geopoint import GeoPoint
from storekiss.reference import Reference, is_reference

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from storekiss.crud import LiteStore


class LiteStoreExporter:
    """
    LiteStore互換のエクスポート機能を提供するクラス
    """

    def __init__(self, db: "LiteStore"):
        """
        LiteStoreExporterを初期化します。

        Args:
            db: LiteStoreインスタンス
        """
        self.db = db

    def export_collection(self, collection_name: str, output_dir: str) -> str:
        """
        指定されたコレクションをLiteStore互換形式でエクスポートします。

        Args:
            collection_name: エクスポートするコレクション名
            output_dir: 出力ディレクトリのパス

        Returns:
            エクスポートされたメタデータファイルのパス
        """
        # 出力ディレクトリを作成
        os.makedirs(output_dir, exist_ok=True)

        # コレクションのパス（LiteStore形式）
        collection_path = f"projects/_/databases/(default)/documents/{collection_name}"

        # コレクションディレクトリを作成
        collection_dir = os.path.join(output_dir, collection_name)
        os.makedirs(collection_dir, exist_ok=True)

        # コレクションのドキュメントを取得
        collection = self.db.collection(collection_name)
        documents = collection.get()

        # ドキュメントデータをLiteStore形式に変換
        litestore_documents = []
        for doc in documents:
            doc_id = doc.id
            doc_data = doc.to_dict()

            # LiteStoreフォーマットのドキュメント
            litestore_doc = {
                "name": f"{collection_path}/{doc_id}",
                "fields": self._convert_to_litestore_fields(doc_data),
                "createTime": self._format_timestamp(doc_data.get("created_at")),
                "updateTime": self._format_timestamp(doc_data.get("updated_at")),
            }
            litestore_documents.append(litestore_doc)

        # ドキュメントをJSONLファイルに書き込み
        documents_file = os.path.join(collection_dir, f"{collection_name}.jsonl")
        with open(documents_file, "w", encoding="utf-8") as f:
            for doc in litestore_documents:
                f.write(json.dumps(doc) + "\n")

        # メタデータファイルを作成
        metadata = {
            "version": "1.0",
            "exportTime": self._format_timestamp(datetime.datetime.now()),
            "collections": [
                {
                    "name": collection_name,
                    "path": collection_path,
                    "documentCount": len(documents),
                }
            ],
        }

        metadata_file = os.path.join(output_dir, "metadata.json")
        with open(metadata_file, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2)

        return metadata_file

    def export_all_collections(self, output_dir: str) -> str:
        """
        すべてのコレクションをLiteStore互換形式でエクスポートします。

        Args:
            output_dir: 出力ディレクトリのパス

        Returns:
            エクスポートされたメタデータファイルのパス
        """
        # 出力ディレクトリを作成
        os.makedirs(output_dir, exist_ok=True)

        # データベース接続を取得
        conn = sqlite3.connect(self.db.db_path)
        cursor = conn.cursor()

        # テーブル一覧を取得（itemsテーブルを除く）
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name != 'items'"
        )
        tables = cursor.fetchall()
        conn.close()

        # 各テーブルをエクスポート
        collections_metadata = []
        for table in tables:
            table_name = table[0]

            # コレクション名を逆変換（難しいため、現状ではテーブル名をそのまま使用）
            collection_name = table_name

            # コレクションのパス（LiteStore形式）
            collection_path = (
                f"projects/_/databases/(default)/documents/{collection_name}"
            )

            # コレクションディレクトリを作成
            collection_dir = os.path.join(output_dir, collection_name)
            os.makedirs(collection_dir, exist_ok=True)

            # コレクションのドキュメントを取得
            collection = self.db.collection(collection_name)
            documents = collection.get()

            # ドキュメントデータをLiteStore形式に変換
            litestore_documents = []
            for doc in documents:
                doc_id = doc.id
                doc_data = doc.to_dict()

                # LiteStoreフォーマットのドキュメント
                litestore_doc = {
                    "name": f"{collection_path}/{doc_id}",
                    "fields": self._convert_to_litestore_fields(doc_data),
                    "createTime": self._format_timestamp(doc_data.get("created_at")),
                    "updateTime": self._format_timestamp(doc_data.get("updated_at")),
                }
                litestore_documents.append(litestore_doc)

            # ドキュメントをJSONLファイルに書き込み
            documents_file = os.path.join(collection_dir, f"{collection_name}.jsonl")
            with open(documents_file, "w", encoding="utf-8") as f:
                for doc in litestore_documents:
                    f.write(json.dumps(doc) + "\n")

            # コレクションメタデータを追加
            collections_metadata.append(
                {
                    "name": collection_name,
                    "path": collection_path,
                    "documentCount": len(documents),
                }
            )

        # メタデータファイルを作成
        metadata = {
            "version": "1.0",
            "exportTime": self._format_timestamp(datetime.datetime.now()),
            "collections": collections_metadata,
        }

        metadata_file = os.path.join(output_dir, "metadata.json")
        with open(metadata_file, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2)

        return metadata_file

    def _convert_to_litestore_fields(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        通常のPythonオブジェクトをLiteStoreフィールド形式に変換します。

        Args:
            data: 変換するデータ

        Returns:
            LiteStore形式のフィールドデータ
        """
        result = {}
        for key, value in data.items():
            if isinstance(value, str):
                result[key] = {"stringValue": value}
            elif isinstance(value, int):
                result[key] = {"integerValue": str(value)}
            elif isinstance(value, float):
                result[key] = {"doubleValue": value}
            elif isinstance(value, bool):
                # ブール値は正しくbooleanValueとして変換
                result[key] = {"booleanValue": value}
            elif isinstance(value, dict):
                result[key] = {
                    "mapValue": {"fields": self._convert_to_litestore_fields(value)}
                }
            elif isinstance(value, list):
                array_values = []
                for item in value:
                    if isinstance(item, str):
                        array_values.append({"stringValue": item})
                    elif isinstance(item, int):
                        array_values.append({"integerValue": str(item)})
                    elif isinstance(item, float):
                        array_values.append({"doubleValue": item})
                    elif isinstance(item, bool):
                        # 配列内のブール値も正しくbooleanValueとして変換
                        array_values.append({"booleanValue": item})
                    elif isinstance(item, dict):
                        array_values.append(
                            {
                                "mapValue": {
                                    "fields": self._convert_to_litestore_fields(item)
                                }
                            }
                        )
                    elif isinstance(item, bytes):
                        array_values.append({"bytesValue": base64.b64encode(item).decode('ascii')})
                    elif isinstance(item, GeoPoint):
                        array_values.append({
                            "geoPointValue": {
                                "latitude": item.latitude,
                                "longitude": item.longitude
                            }
                        })
                    elif is_reference(item):
                        array_values.append({
                            "referenceValue": f"{item.collection_path}/{item.document_id}"
                        })
                    elif item is None:
                        array_values.append({"nullValue": None})
                    else:
                        array_values.append({"stringValue": str(item)})
                result[key] = {"arrayValue": {"values": array_values}}
            elif isinstance(value, datetime.datetime):
                result[key] = {"timestampValue": value.isoformat() + "Z"}
            elif isinstance(value, bytes):
                result[key] = {"bytesValue": base64.b64encode(value).decode('ascii')}
            elif isinstance(value, GeoPoint):
                result[key] = {
                    "geoPointValue": {
                        "latitude": value.latitude,
                        "longitude": value.longitude
                    }
                }
            elif is_reference(value):
                result[key] = {
                    "referenceValue": f"{value.collection_path}/{value.document_id}"
                }
            elif value is None:
                result[key] = {"nullValue": None}
            else:
                # その他の型は文字列として扱う
                result[key] = {"stringValue": str(value)}

        return result

    def _format_timestamp(self, timestamp) -> str:
        """
        タイムスタンプをLiteStore形式にフォーマットします。

        Args:
            timestamp: フォーマットするタイムスタンプ

        Returns:
            LiteStore形式のタイムスタンプ文字列
        """
        if isinstance(timestamp, str):
            # すでに文字列の場合は、ISO形式に変換を試みる
            try:
                dt = datetime.datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
                return dt.isoformat() + "Z"
            except ValueError:
                # 変換できない場合は現在時刻を使用
                return datetime.datetime.now().isoformat() + "Z"
        elif isinstance(timestamp, datetime.datetime):
            return timestamp.isoformat() + "Z"
        else:
            # タイムスタンプがない場合は現在時刻を使用
            return datetime.datetime.now().isoformat() + "Z"


class LiteStoreImporter:
    """
    LiteStore互換のインポート機能を提供するクラス
    """

    def __init__(self, db: "LiteStore"):
        """
        LiteStoreImporterを初期化します。

        Args:
            db: LiteStoreインスタンス
        """
        self.db = db

    def import_collection(self, collection_name: str, import_dir: str) -> int:
        """
        指定されたコレクションをLiteStore互換形式からインポートします。

        Args:
            collection_name: インポートするコレクション名
            import_dir: インポートディレクトリのパス

        Returns:
            インポートされたドキュメント数
        """
        # コレクションディレクトリのパス
        collection_dir = os.path.join(import_dir, collection_name)

        # コレクションのJSONLファイルのパス
        jsonl_file = os.path.join(collection_dir, f"{collection_name}.jsonl")

        if not os.path.exists(jsonl_file):
            raise FileNotFoundError(f"コレクションファイルが見つかりません: {jsonl_file}")

        # コレクションを取得
        collection = self.db.collection(collection_name)

        # ドキュメントをインポート
        imported_count = 0
        with open(jsonl_file, "r", encoding="utf-8") as f:
            for line in f:
                litestore_doc = json.loads(line)

                # ドキュメントIDを抽出
                doc_path = litestore_doc.get("name", "")
                doc_id = doc_path.split("/")[-1] if doc_path else None

                if not doc_id:
                    logging.warning("ドキュメントIDが見つかりません。スキップします。")
                    continue

                # LiteStoreフィールドを通常のPythonオブジェクトに変換
                fields = litestore_doc.get("fields", {})
                doc_data = self._convert_from_litestore_fields(fields)

                # タイムスタンプを設定
                create_time = litestore_doc.get("createTime")
                update_time = litestore_doc.get("updateTime")

                if create_time:
                    doc_data["created_at"] = create_time
                if update_time:
                    doc_data["updated_at"] = update_time

                # ドキュメントを作成または更新
                collection.document(doc_id).set(doc_data)
                imported_count += 1

        return imported_count

    def import_all_collections(self, import_dir: str) -> Dict[str, int]:
        """
        すべてのコレクションをLiteStore互換形式からインポートします。

        Args:
            import_dir: インポートディレクトリのパス

        Returns:
            コレクション名とインポートされたドキュメント数の辞書
        """
        # メタデータファイルのパス
        metadata_file = os.path.join(import_dir, "metadata.json")

        if not os.path.exists(metadata_file):
            raise FileNotFoundError(f"メタデータファイルが見つかりません: {metadata_file}")

        # メタデータを読み込み
        with open(metadata_file, "r", encoding="utf-8") as f:
            metadata = json.load(f)

        # コレクション一覧を取得
        collections = metadata.get("collections", [])

        # 各コレクションをインポート
        result = {}
        for collection_info in collections:
            collection_name = collection_info.get("name")
            if not collection_name:
                continue

            try:
                imported_count = self.import_collection(collection_name, import_dir)
                result[collection_name] = imported_count
            except Exception as e:
                logging.error(f"コレクション '{collection_name}' のインポート中にエラーが発生しました: {e}")
                result[collection_name] = 0

        return result

    def _convert_from_litestore_fields(self, fields: Dict[str, Any]) -> Dict[str, Any]:
        """
        LiteStoreフィールド形式を通常のPythonオブジェクトに変換します。

        Args:
            fields: 変換するLiteStoreフィールド

        Returns:
            通常のPythonオブジェクト
        """
        result = {}
        for key, value_container in fields.items():
            value_type, value = next(iter(value_container.items()))

            if value_type == "stringValue":
                result[key] = value
            elif value_type == "integerValue":
                # ブール値が整数として保存されている場合の処理
                if value == "True":
                    result[key] = True
                elif value == "False":
                    result[key] = False
                else:
                    result[key] = int(value)
            elif value_type == "doubleValue":
                result[key] = float(value)
            elif value_type == "booleanValue":
                if isinstance(value, str):
                    result[key] = value.lower() == "true"
                else:
                    result[key] = bool(value)
            elif value_type == "mapValue":
                result[key] = self._convert_from_litestore_fields(
                    value.get("fields", {})
                )
            elif value_type == "arrayValue":
                array_result = []
                for item in value.get("values", []):
                    item_type, item_value = next(iter(item.items()))

                    if item_type == "stringValue":
                        array_result.append(item_value)
                    elif item_type == "integerValue":
                        # 配列内のブール値が整数として保存されている場合の処理
                        if item_value == "True":
                            array_result.append(True)
                        elif item_value == "False":
                            array_result.append(False)
                        else:
                            array_result.append(int(item_value))
                    elif item_type == "doubleValue":
                        array_result.append(float(item_value))
                    elif item_type == "booleanValue":
                        array_result.append(bool(item_value))
                    elif item_type == "mapValue":
                        array_result.append(
                            self._convert_from_litestore_fields(
                                item_value.get("fields", {})
                            )
                        )
                    elif item_type == "bytesValue":
                        array_result.append(base64.b64decode(item_value))
                    elif item_type == "geoPointValue":
                        array_result.append(GeoPoint(item_value["latitude"], item_value["longitude"]))
                    elif item_type == "referenceValue":
                        parts = item_value.split('/')
                        collection_path = '/'.join(parts[:-1])
                        document_id = parts[-1]
                        array_result.append(Reference(collection_path, document_id))
                    elif item_type == "nullValue":
                        array_result.append(None)
                    else:
                        array_result.append(str(item_value))

                result[key] = array_result
            elif value_type == "timestampValue":
                try:
                    result[key] = datetime.datetime.fromisoformat(
                        value.replace("Z", "+00:00")
                    )
                except ValueError:
                    result[key] = value
            elif value_type == "bytesValue":
                result[key] = base64.b64decode(value)
            elif value_type == "geoPointValue":
                result[key] = GeoPoint(value["latitude"], value["longitude"])
            elif value_type == "referenceValue":
                parts = value.split('/')
                collection_path = '/'.join(parts[:-1])
                document_id = parts[-1]
                result[key] = Reference(collection_path, document_id)
            elif value_type == "nullValue":
                result[key] = None
            else:
                result[key] = str(value)

        return result


# LiteStoreクラスに拡張メソッドを追加
def export_collection(self, collection_name: str, output_dir: str) -> str:
    """
    指定されたコレクションをLiteStore互換形式でエクスポートします。

    Args:
        collection_name: エクスポートするコレクション名
        output_dir: 出力ディレクトリのパス

    Returns:
        エクスポートされたメタデータファイルのパス
    """
    exporter = LiteStoreExporter(self)
    return exporter.export_collection(collection_name, output_dir)


def export_all_collections(self, output_dir: str) -> str:
    """
    すべてのコレクションをLiteStore互換形式でエクスポートします。

    Args:
        output_dir: 出力ディレクトリのパス

    Returns:
        エクスポートされたメタデータファイルのパス
    """
    exporter = LiteStoreExporter(self)
    return exporter.export_all_collections(output_dir)


def import_collection(self, collection_name: str, import_dir: str) -> int:
    """
    指定されたコレクションをLiteStore互換形式からインポートします。

    Args:
        collection_name: インポートするコレクション名
        import_dir: インポートディレクトリのパス

    Returns:
        インポートされたドキュメント数
    """
    importer = LiteStoreImporter(self)
    return importer.import_collection(collection_name, import_dir)


def import_all_collections(self, import_dir: str) -> Dict[str, int]:
    """
    すべてのコレクションをLiteStore互換形式からインポートします。

    Args:
        import_dir: インポートディレクトリのパス

    Returns:
        コレクション名とインポートされたドキュメント数の辞書
    """
    importer = LiteStoreImporter(self)
    return importer.import_all_collections(import_dir)


# LiteStoreクラスにメソッドを追加
try:
    from storekiss.crud import LiteStore
    LiteStore.export_collection = export_collection
    LiteStore.export_all_collections = export_all_collections
    LiteStore.import_collection = import_collection
    LiteStore.import_all_collections = import_all_collections
except ImportError:
    pass

# LiteStoreClientクラス用のメソッド

# LiteStoreClientクラスのインポート
try:
    from storekiss.litestore import LiteStoreClient

    def client_export_collection(self, collection_name: str, output_dir: str) -> str:
        """
        指定されたコレクションをLiteStore互換形式でエクスポートします。

        Args:
            collection_name: エクスポートするコレクション名
            output_dir: 出力ディレクトリのパス

        Returns:
            エクスポートされたメタデータファイルのパス
        """
        exporter = LiteStoreExporter(self._store)
        return exporter.export_collection(collection_name, output_dir)

    def client_export_all_collections(self, output_dir: str) -> str:
        """
        すべてのコレクションをLiteStore互換形式でエクスポートします。

        Args:
            output_dir: 出力ディレクトリのパス

        Returns:
            エクスポートされたメタデータファイルのパス
        """
        exporter = LiteStoreExporter(self._store)
        return exporter.export_all_collections(output_dir)

    def client_import_collection(self, collection_name: str, import_dir: str) -> int:
        """
        指定されたコレクションをLiteStore互換形式からインポートします。

        Args:
            collection_name: インポートするコレクション名
            import_dir: インポートディレクトリのパス

        Returns:
            インポートされたドキュメント数
        """
        importer = LiteStoreImporter(self._store)
        return importer.import_collection(collection_name, import_dir)

    def client_import_all_collections(self, import_dir: str) -> Dict[str, int]:
        """
        すべてのコレクションをLiteStore互換形式からインポートします。

        Args:
            import_dir: インポートディレクトリのパス

        Returns:
            コレクション名とインポートされたドキュメント数の辞書
        """
        importer = LiteStoreImporter(self._store)
        return importer.import_all_collections(import_dir)

    # LiteStoreClientクラスにメソッドを追加
    LiteStoreClient.export_collection = client_export_collection
    LiteStoreClient.export_all_collections = client_export_all_collections
    LiteStoreClient.import_collection = client_import_collection
    LiteStoreClient.import_all_collections = client_import_all_collections

except ImportError:
    # LiteStoreClientが定義されていない場合はスキップ
    pass
