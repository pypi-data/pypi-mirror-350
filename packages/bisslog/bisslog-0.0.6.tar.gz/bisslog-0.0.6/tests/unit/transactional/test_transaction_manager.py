import threading
from concurrent.futures import ThreadPoolExecutor

from bisslog.transactional.transaction_manager import transaction_manager


def create_and_get_transaction():
    """Function to be executed in a thread to test transaction creation and retrieval."""
    transaction_id = transaction_manager.create_transaction_id("test_component")
    retrieved_id = transaction_manager.get_transaction_id()
    assert transaction_id == retrieved_id, f"Expected {transaction_id}, but got {retrieved_id}"


def test_concurrent_transactions():
    """Test multiple concurrent transactions to ensure thread safety."""
    transaction_manager.clear()
    num_threads = 100  # Number of concurrent threads

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(create_and_get_transaction) for _ in range(num_threads * 3)]

    for future in futures:
        future.result()  # Ensures all assertions pass
    transaction_manager.clear()


def test_transaction_isolation():
    """Test"""
    transaction_manager.clear()
    threads_used = set()

    def create_transaction_in_thread():
        thread_id = threading.get_ident()
        n = 10
        prc_transactions = {}
        for i in range(n):
            if i == 0:
                assert transaction_manager.get_transaction_id() is None
            else:
                assert prc_transactions[i - 1] == transaction_manager.get_transaction_id()
            transaction_id = transaction_manager.create_transaction_id(f"component_{thread_id}")
            prc_transactions[i] = transaction_id

        for i in range(n):
            if i < n - 1:
                assert prc_transactions[0] == transaction_manager.get_main_transaction_id()
            transaction_manager.close_transaction()
        threads_used.add(thread_id)

    threads = [threading.Thread(target=create_transaction_in_thread) for _ in range(100)]

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    # Ensure all transactions are unique per thread
    assert not threads_used - set(transaction_manager._thread_active_transaction_mapping.keys())
    # assert len(set(transaction_ids.values())) == 50  # Ensure all transaction IDs are unique
    transaction_manager.clear()


def test_main_transaction():
    """Test getting the first transaction in a thread."""
    transaction_manager.clear()
    expected_main_transaction = transaction_manager.create_transaction_id("main_component")
    transaction_manager.create_transaction_id("main_component")
    transaction_manager.create_transaction_id("main_component")
    expected_current_transaction = transaction_manager.create_transaction_id("main_component")
    main_transaction = transaction_manager.get_main_transaction_id()
    current_transaction = transaction_manager.get_transaction_id()
    current_component = transaction_manager.get_component()

    assert expected_main_transaction == main_transaction
    assert expected_current_transaction == current_transaction
    assert "main_component" == current_component
    transaction_manager.clear()


def test_no_transaction():
    """Test getting the first transaction in a thread when no transaction exists."""
    transaction_manager.clear()
    assert transaction_manager.get_transaction_id() is None
    assert transaction_manager.get_main_transaction_id() is None
    assert transaction_manager.get_component() is None
    transaction_manager.clear()


def test_close_transaction():
    """Ensure closing a transaction removes it from the thread's list."""
    transaction_manager.clear()
    transaction_id = transaction_manager.create_transaction_id("test_component")
    assert transaction_manager.get_transaction_id() == transaction_id

    transaction_manager.close_transaction()
    # print(transaction_manager._thread_active_transaction_mapping)
    assert transaction_manager.get_transaction_id() is None
    transaction_manager.clear()
