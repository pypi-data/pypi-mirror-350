import logging, sys

from bisslog.database.bisslog_db import bisslog_db
from .database.impls.session_division_cache import session_division_cache
from .usecases.my_first_use_case import sumar_use_case


bisslog_db.register_adapters(session=session_division_cache)

format_from_env = "[%(asctime)s][%(transaction_id)s][%(levelname)s][%(checkpoint_id)s] %(message)s"

logging.basicConfig(level=logging.DEBUG, format=format_from_env, stream=sys.stdout)

res = sumar_use_case(5, 7, user_id=20)
print(res)

res2 = sumar_use_case(888, 777, user_id=20)
print(res2)


