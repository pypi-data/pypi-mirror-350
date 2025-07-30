import os
import ydb
import ydb.iam
import ast
import json

driver = ydb.Driver(
  endpoint=os.getenv('YDB_ENDPOINT', 'grpcs://ydb.serverless.yandexcloud.net:2135'),
  database=os.getenv('YDB_DATABASE'),
  credentials=ydb.iam.MetadataUrlCredentials(),
)

driver.wait(fail_fast=True, timeout=5)

pool = ydb.QuerySessionPool(driver)

INIT_SQL = """
create table if not exists device_capability_state (
  user_id Uint64 not null,
  capability_key Utf8 not null,
  capability_state Utf8,
  device_id Utf8 not null,   
  primary key (user_id, capability_key)    
)
with (
  AUTO_PARTITIONING_BY_SIZE = ENABLED,
  AUTO_PARTITIONING_PARTITION_SIZE_MB = 512
);
"""

UPSERT_CAPABILITY_STATE_SQL = """
DECLARE $uid AS Uint64;
DECLARE $cid AS Utf8;
DECLARE $did AS Utf8;
DECLARE $state AS Utf8;

UPSERT INTO device_capability_state (user_id, capability_key, device_id, capability_state) 
VALUES ($uid, $cid, $did, $state);
"""

GET_CAPABILITY_STATE_SQL = """
DECLARE $uid AS Uint64;
DECLARE $cid AS Utf8;

SELECT state FROM device_capability_state WHERE user_id = $uid AND capability_key = $cid;
"""


"""
Этот модуль предоставляет интерфейс для взаимодействия с базой данных 
YDB для управления состояниями возможностей устройств.
"""
class YandexDB:
  def __init__(self):
    pool.execute_with_retries(INIT_SQL)


  """
  Получает состояние возможности устройства для указанного пользователя и ключа возможности.
  Если состояние не найдено, возвращает None.
  """
  def get_capability_state(self, user_id, capability_key):
    result = pool.execute_with_retries(
      GET_CAPABILITY_STATE_SQL,
      {
        '$uid': user_id,
        '$cid': capability_key
      }
    )

    if result[0].rows:
      state = result[0].rows[0].capability_state.decode("utf-8")
      return ast.literal_eval(state)

    return None    


  """
  Устанавливает состояние возможности устройства для указанного пользователя,
  ключа возможности и идентификатора устройства.
  """  
  def set_capability_state(self, user_id, capability_key, device_id, capability_state):
    pool.execute_with_retries(
      UPSERT_CAPABILITY_STATE_SQL,
      {
        '$uid': ydb.TypedValue(user_id, ydb.PrimitiveType.Uint64),
        '$cid': capability_key,
        '$did': device_id,
        '$state': json.dumps(capability_state)
      }
    )