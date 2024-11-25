
from queue import Queue
import signal
import sqlite3
from threading import Thread
import os

from dnaStreaming.listener import Listener

def processMessagesQueue(queue):
    db = sqlite3.connect('test_listener.sqlite3', isolation_level=None)
    cursor = db.cursor()
    while True:
        if not queue.empty():
            message = queue.get()
            cursor.execute(
                'INSERT INTO received_articles_python (an, ingestion_datetime) VALUES (?, ?)',
                (message['an'], message['ingestion_datetime'])
            )
            print(f"Written: {message['an']}")
            queue.task_done()

def main():
    try:
        assert (subscription_id := os.environ['SUBSCRIPTION_ID_PYTHON']), 'The subscription for python listener is not set'
        db = sqlite3.connect('test_listener.sqlite3', isolation_level=None)
        cursor = db.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS received_articles_python (an TEXT, ingestion_datetime TEXT)')
        db.close()
        the_queue = Queue()
        
        def callback(message, _):
            the_queue.put(message)
            return True
        
        writer_worker = Thread(target=processMessagesQueue, args=(the_queue,))
        writer_worker.setDaemon(True)
        writer_worker.start()
        listener = Listener()
        future = listener.listen_async(callback, subscription_id)
        
        def manage_closing():
            if future.running():
                future.cancel()
                future.result()
            the_queue.join()
        
        def signal_handler(signum, frame):
            manage_closing()
        
        signal.signal(signal.SIGTERM, signal_handler)
        future.result()
    except Exception as ex:
        print(f'Se encontró una excepción {ex}')
    except KeyboardInterrupt:
        pass
    finally:
        manage_closing()


if __name__ == '__main__':
    main()
