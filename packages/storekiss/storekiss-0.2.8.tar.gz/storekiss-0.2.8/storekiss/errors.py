"""
storekiss エラー定義モジュール

このモジュールは、storekissライブラリで使用される例外クラスを定義します。
"""


class StorekissError(Exception):
    """storekissの基本例外クラス"""

    pass


class DatabaseError(StorekissError):
    """データベース操作に関連するエラー"""

    pass


class NotFoundError(StorekissError):
    """リソースが見つからない場合のエラー"""

    pass


class ValidationError(StorekissError):
    """データ検証に失敗した場合のエラー"""

    pass


class ConfigError(StorekissError):
    """設定に関連するエラー"""

    pass


class ExportError(StorekissError):
    """エクスポート処理に関連するエラー"""

    pass


class ImportError(StorekissError):
    """インポート処理に関連するエラー"""

    pass
