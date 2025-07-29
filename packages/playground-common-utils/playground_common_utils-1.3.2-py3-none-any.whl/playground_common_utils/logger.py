import logging

class CustomColorEmojiFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: "\033[90m",   # 明るい黒 (グレー)
        logging.INFO: "\033[36m",    # シアン
        logging.WARNING: "\033[33m", # 黄色
        logging.ERROR: "\033[31m",   # 赤
        logging.CRITICAL: "\033[91m",# 明るい赤 (より強調)
    }
    RESET_COLOR = "\033[0m"

    EMOJIS = {
        logging.DEBUG: "🐞",
        logging.INFO: "ℹ️ ",
        logging.WARNING: "⚠️ ",
        logging.ERROR: "🚨",
        logging.CRITICAL: "🔥",
    }

    # フォーマッターの初期化時に基本となるフォーマット文字列を受け取る
    def __init__(self, fmt=None, datefmt=None, style='%'):
        super().__init__(fmt, datefmt, style)

    def format(self, record):
        # まず、親クラスのformatメソッドを呼び出して基本的なメッセージをフォーマットする
        # この時点では、まだ色や絵文字は付いていない
        original_message = super().format(record)

        # ログレベルに応じた色と絵文字を取得
        color_code = self.COLORS.get(record.levelno, "") # 色がなければ空文字列
        emoji = self.EMOJIS.get(record.levelno, "")      # 絵文字がなければ空文字列

        # 絵文字と色を元のメッセージに結合する
        # ここで絵文字とカラーコードを挿入し、最後に色をリセットする
        # 絵文字とカラーコードの間にスペースを入れることで、見た目を整える
        colored_message = f"{color_code}{emoji} {original_message}{self.RESET_COLOR}"
        
        return colored_message


# ロガーの設定
logger = logging.getLogger(__name__)


# ログレベル
DEBUG = logging.DEBUG
INFO = logging.INFO
WARNING = logging.WARNING
ERROR = logging.ERROR
CRITICAL = logging.CRITICAL

logger.setLevel(DEBUG)


# ハンドラーの設定
handler = logging.StreamHandler()
# フォーマッターの初期化時に、logging.basicConfigで使ったような一般的なフォーマット文字列を渡す
# 絵文字と色はこのフォーマッターのformatメソッド内で追加される
formatter = CustomColorEmojiFormatter(
    fmt='%(asctime)s [%(levelname)s] | %(filename)s / %(funcName)s  [%(lineno)s] | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
handler.setFormatter(formatter)
logger.addHandler(handler)

