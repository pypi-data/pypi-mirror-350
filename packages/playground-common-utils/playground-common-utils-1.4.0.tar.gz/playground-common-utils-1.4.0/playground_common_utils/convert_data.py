from playground_common_utils.logger import *
from playground_common_utils.http import *
from flask import jsonify, Response
from typing import Tuple, Any, Union, List

RESPONSE = 0
STATUS_CODE = 1
DATA="data"
MESSAGE="message"

# COMMON MAKE RESPONSE DATA
def response_data(status_code: int = 200, data: Union[dict, List[dict], None] = None, message: str = GET) -> Tuple[Response, int]:
    logger.debug(f"status_code: {status_code}")
    logger.debug(f"data: {data}")
    logger.debug(f"message: {message}")
    
    logger.debug(f"result: {jsonify({DATA: data, MESSAGE: message}), status_code}")
    return jsonify({DATA: data, MESSAGE: message}), status_code


def dict_to_model(request_dict: dict, model: Any) -> Any:
    logger.debug(f"request_dict: {request_dict}")
    
    # request_data(type: dict)からkey, value抽出
    for key, value in request_dict.items():
        
        # modelに追加
        setattr(model, key, value)
    
    logger.debug(f"model: {model}")
    return model


def model_to_dict(model: Any, exclude: List[str] = []) -> dict:
    logger.debug(f"model: {model}")
    result = {}
    for column in model.__table__.columns:
        if column.name in exclude:
            continue
        value = getattr(model, column.name)
        if hasattr(value, 'isoformat'):  # datetimeなど
            value = value.isoformat()
        result[column.name] = value
    
    logger.debug(f"dict: {result}")
    return result

def models_to_dicts(model_list: List[Any], exclude: List[str] = []) -> List[dict]:
    return [model_to_dict(model, exclude) for model in model_list]
