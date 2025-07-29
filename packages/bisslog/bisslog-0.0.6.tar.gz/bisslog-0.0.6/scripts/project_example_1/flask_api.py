import logging, sys

from flask import Flask, request, abort

from bisslog.adapters.tracing.logging_filter import BisslogFilterLogging
from bisslog.database.bisslog_db import bisslog_db
from scripts.project_example_1.database.impls.session_division_cache import session_division_cache
from scripts.project_example_1.usecases.my_first_use_case import sumar_use_case


bisslog_db.register_adapters(session=session_division_cache)

format_from_env = "[%(asctime)s][%(transaction_id)s][%(levelname)s][%(checkpoint_id)s] %(message)s"

logging.basicConfig(level=logging.DEBUG, format=format_from_env, stream=sys.stdout)
logging.root.handlers[0].addFilter(BisslogFilterLogging())

app = Flask(__name__)

@app.route("/first-use-case/<a>/<b>")
def home(a, b):
    user_id = request.headers.get("user_id")
    if user_id is None:
        abort(400, "No user_id header")
    user_id = int(user_id)
    res = sumar_use_case(int(a), int(b), user_id)
    res["identifier"] = "flask"
    return res

