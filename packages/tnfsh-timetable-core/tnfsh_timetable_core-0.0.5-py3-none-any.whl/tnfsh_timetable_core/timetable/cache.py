from typing import Dict
from pathlib import Path
import json
from tnfsh_timetable_core.timetable.models import TimeTable
from tnfsh_timetable_core.utils.logger import get_logger

# 設定日誌

logger = get_logger(logger_level="INFO")


# 第一層：記憶體快取
prebuilt_cache: Dict[str, TimeTable] = {} # str: Teacher name or class code

# 第二層：本地 JSON 快取目錄
CACHE_DIR = Path(__file__).resolve().parent / "cache"
CACHE_DIR.mkdir(exist_ok=True)

def load_from_disk(target: str) -> dict:
    """從磁碟載入快取的課表資料。

    Args:
        target: 目標班級代號

    Returns:
        dict: 快取的課表資料，如果載入失敗則返回空字典
    """
    path = CACHE_DIR / f"prebuilt_{target}.json"
    try:
        if path.exists() and path.stat().st_size > 0:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
                logger.debug(f"成功從 {path} 載入快取資料")  # 改為 debug 層級
                return data
        else:
            logger.debug(f"快取檔案 {path} 不存在或為空")  # 改為 debug 層級
    except json.JSONDecodeError as e:
        logger.error(f"快取檔案 {path} JSON 格式無效: {e}")  # 保留 error 層級
    except Exception as e:
        logger.error(f"讀取快取檔案 {path} 時發生錯誤: {e}")  # 保留 error 層級
    return {}

def save_to_disk(target: str, table: TimeTable) -> bool:
    """將課表資料儲存到磁碟快取。

    Args:
        target: 目標班級代號
        table: 要儲存的課表物件

    Returns:
        bool: 儲存是否成功
    """
    path = CACHE_DIR / f"prebuilt_{target}.json"
    try:
        with open(path, "w", encoding="utf-8") as f:
            json_data = table.model_dump_json(indent=4)
            f.write(json_data)
            logger.debug(f"成功將資料儲存至 {path}")  # 改為 debug 層級
            return True
    except Exception as e:
        logger.error(f"儲存資料至 {path} 時發生錯誤: {e}")  # 保留 error 層級
        return False


async def preload_all(only_missing: bool = True, max_concurrent: int = 5):
    """
    預載入所有課表，加入併發上限控制，避免同時連線過多導致請求失敗。
    Args:
        only_missing (bool): 是否只預載入缺少的課表，預設為 True
        max_concurrent (int): 最大併發請求數量，預設為 5
    """

    from tnfsh_timetable_core.index.index import Index
    import asyncio

    # 初始化並載入索引
    index = Index()
    await index.fetch()
    
    if not index.reverse_index:
        logger.error("❌ 無法獲取課表索引")
        return
        
    targets = list(index.reverse_index.keys())
    logger.info(f"🔄 開始預載入所有課表，共 {len(targets)} 項")

    semaphore = asyncio.Semaphore(max_concurrent)

    async def process(target: str):
        if only_missing and (target in prebuilt_cache or load_from_disk(target)):
            logger.debug(f"快取已存在，略過：{target}")
            return
        async with semaphore:
            try:
                logger.debug(f"➡️ 開始預載入：{target}")
                await TimeTable.fetch_cached(target)
                logger.debug(f"✅ 預載入成功：{target}")
            except Exception as e:
                logger.error(f"❌ 預載入失敗 {target}: {e}")

    await asyncio.gather(*(process(t) for t in targets))
    logger.info("🏁 預載入完成")


if __name__ == "__main__":
    # For test cases, see: tests/test_timetable/test_cache.py
    pass


