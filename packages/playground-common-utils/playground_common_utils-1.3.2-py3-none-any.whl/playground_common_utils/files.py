import os
import shutil


from playground_common_utils.logger import *

###########
### 確認 ###
###########
def is_exist(path):
    """
    存在チェック
    引数:
        path -- 存在チェックをするパス<str>
    戻り値: 
        存在有無<bool>
    """
    return os.path.exists(path)

def is_file(path):
    """
    ファイルの存在チェック
    引数:
        path -- 存在チェックをするパス<str>
    戻り値: 
        存在有無<bool>
    """
    return os.path.isfile(path)

def is_dir(path):
    """
    ディレクトリの存在チェック
    引数:
        path -- 存在チェックをするパス<str>
    戻り値: 
        存在有無<bool>
    """
    return os.path.isdir(path)


###########
### 作成 ###
###########
def create_file(path):
    """
    空ファイルを作成する
    （すでに存在している場合は何もしない）
    
    引数:
        path -- 作成するファイルのパス<str>
    戻り値:
        なし
    """
    if not is_exist(path):
        with open(path, 'a', encoding='utf-8'):
            pass
        logger.debug(f"空ファイル作成: {path}")
    else:
        logger.warning(f"ファイル既に存在: {path}")

def create_dir(path):
    """
    ディレクトリの生成
    引数:
        path -- ディレクトリを生成するパス<str>
    戻り値: 
        存在有無<bool>
    """
    if is_dir(path):
        logger.debug(f"ディレクトリ既に存在: {path}")
        return 
    os.mkdir(path)
    logger.info("ディレクトリを生成しました。")


###########
### 取得 ###
###########
def read_current_dir():
    """
    現在のディレクトリ取得
    引数:
        なし
    戻り値:
        なし
    """
    return os.getcwd()

def read_file(path):
    """
    ファイルの読み込み
    引数:
        path -- ファイルのパス<str>
    戻り値: 
        ファイルの中身<str>
    """
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def read_list_dir(path):
    """
    ディレクトリ内の一覧を取得する

    引数:
        path -- 対象ディレクトリのパス<str>
    戻り値:
        ディレクトリ内のファイル・ディレクトリ一覧<list>
    """
    if is_dir(path):
        items = os.listdir(path)
        logger.debug(f"ディレクトリ一覧取得完了: {path}")
        return items
    else:
        logger.warning(f"対象ディレクトリが存在しません: {path}")
        return []

def read_enviroment(key):
    """
    環境変数の値を取得

    引数:
        key -- 環境変数のキー<str>
    戻り値:
        環境変数の値<str>
    """
    return os.environ.get(key)

###########
### 更新 ###
###########
def overwrite_file(path, content):
    """
    ファイルに内容を書き込む（上書き）
    引数:
        path -- ファイルのパス<str>
        content -- 新たに書き込む文字列<str>
    戻り値:
        なし
    """
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
        logger.debug(f"上書き完了: {path}")

def append_file(path, content):
    """
    ファイルに内容を追記する
    
    引数:
        path -- ファイルのパス<str>
        content -- 追記する文字列<str>
    戻り値:
        なし
    """
    with open(path, 'a', encoding='utf-8') as f:
        f.write(content)
        logger.debug(f"追記完了: {path}")

def load_env_file(path):
    """
    .envファイルを読み込んで環境変数にセットする

    引数:
        path -- .envファイルのパス<str>
    戻り値:
        なし
    """
    if not is_file(path):
        logger.warning(f".envファイルが存在しません: {path}")
        return

    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        if line and not line.startswith("#"):  # 空行とコメントは無視
            key_value = line.split('=', 1)
            if len(key_value) == 2:
                key, value = key_value
                os.environ[key.strip()] = value.strip()
                logger.debug(f"環境変数設定: {key.strip()}")
            else:
                logger.debug(f"無効な行: {line}")


###########
### 削除 ###
###########
def delete_file(path):
    """
    ファイルを削除する

    引数:
        path -- 削除するファイルのパス<str>
    戻り値:
        なし
    """
    if is_exist(path):
        os.remove(path)
        logger.debug(f"ファイル削除完了: {path}")
    else:
        logger.debug(f"ファイルが存在しないか、ファイルではない: {path}")

def delete_dir(path):
    """
    ディレクトリの削除
    引数:
        path -- ディレクトリを削除するパス<str>
    戻り値: 
        存在有無<bool>
    """
    if is_dir(path):
        os.rmdir(path)
        logger.info("ディレクトリを削除しました。")
    else:
        logger.debug(f"ディレクトリ既に存在: {path}")


###########
### 操作 ###
###########
def copy_file(src_path, dst_path):
    """
    ファイルをコピーする

    引数:
        src_path -- コピー元のパス<str>
        dst_path -- コピー先のパス<str>
    戻り値:
        なし
    """
    if is_file(src_path):
        shutil.copy(src_path, dst_path)
        logger.debug(f"ファイルコピー完了: {src_path} → {dst_path}")
    else:
        logger.warning(f"コピー元ファイルが存在しません: {src_path}")

def move_file(src_path, dst_path):
    """
    ファイルを移動する

    引数:
        src_path -- 移動元のパス<str>
        dst_path -- 移動先のパス<str>
    戻り値:
        なし
    """
    if is_file(src_path):
        shutil.move(src_path, dst_path)
        logger.debug(f"ファイル移動完了: {src_path} → {dst_path}")
    else:
        logger.warning(f"移動元ファイルが存在しません: {src_path}")
