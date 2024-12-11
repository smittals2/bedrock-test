import sys
from config import printer

class UserInputManager:
    shutdown_executor = False
    executor = None

    @staticmethod
    def set_executor(executor):
        UserInputManager.executor = executor

    @staticmethod
    def start_shutdown_executor():
        UserInputManager.shutdown_executor = False
        raise Exception()

    @staticmethod
    def start_user_input_loop():
        while True:
            sys.stdin.readline().strip()
            printer(f'[DEBUG] User input to shut down executor...', 'debug')
            UserInputManager.shutdown_executor = True

    @staticmethod
    def is_executor_set():
        return UserInputManager.executor is not None

    @staticmethod
    def is_shutdown_scheduled():
        return UserInputManager.shutdown_executor