from unittest.mock import patch
from scripts.project_example_1.usecases.my_first_use_case import sumar_use_case


string_expected = """
INFO     transactional-tracer:transactional_tracer_logging.py:32 Received sumar a:9 b:3 None
INFO     transactional-tracer:transactional_tracer_logging.py:32 
################################################################################
Blank adapter for main-database on division: session 
execution of method 'get_last_session_user' with args (123,), kwargs {}
################################################################################
INFO     transactional-tracer:transactional_tracer_logging.py:32 
################################################################################
Blank adapter for main-database on division: session 
execution of method 'save_new_session_user' with args (123,), kwargs {}
################################################################################
INFO     transactional-tracer:transactional_tracer_logging.py:32 
################################################################################
Blank adapter for main-database on division: event_type 
execution of method 'loadWebhookEventType' with args (5,), kwargs {}
################################################################################
DEBUG    opener-logger:opener_tracer_logging.py:36 tx-002
INFO     transactional-tracer:transactional_tracer_logging.py:32 Received 1 my_second_use_case
INFO     transactional-tracer:transactional_tracer_logging.py:32 
################################################################################
Blank adapter for file-uploader on division: main 
execution of method 'upload_file_from_local' with args ('./test.txt', '/app/casa/20'), kwargs {}
################################################################################
DEBUG    opener-logger:opener_tracer_logging.py:54 tx-002 with result 0.3
DEBUG    opener-logger:opener_tracer_logging.py:36 
INFO     transactional-tracer:transactional_tracer_logging.py:32 BUAJAJA
INFO     transactional-tracer:transactional_tracer_logging.py:32 ()
INFO     transactional-tracer:transactional_tracer_logging.py:32 third_uc_res 89
WARNING  transactional-tracer:transactional_tracer_logging.py:70 It is greater than 10
INFO     transactional-tracer:transactional_tracer_logging.py:32 
################################################################################
Blank adapter for publisher-default on division: main 
execution of method '__call__' with args ('queue_suma', {'suma': 12.3, 'operation': 'a + b'}), kwargs {'partition': None}
################################################################################
"""


@patch("scripts.project_example_1.usecases.my_first_use_case.random", return_value=0.1)
def test_sumar_use_case_logs_with_format(mock_random, caplog):

    with caplog.at_level("DEBUG"):
        result = sumar_use_case.use(a=9, b=3, user_id=123, transaction_id="tx-002")

    # Assert expected result
    assert result == {"suma": 12}

    # Assertions on formatted log content
    for string_expected_item in string_expected.split("\n"):
        if string_expected_item:
            assert string_expected_item in caplog.text
