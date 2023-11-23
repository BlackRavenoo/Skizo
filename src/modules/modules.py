import importlib

from aiogram import Dispatcher

from config import modules_config

def enable_modules(disp: Dispatcher) -> None:
    for module, enabled in modules_config.items():
        if enabled:
            module = importlib.import_module(f"modules.{module}Extension.{module}")
            disp.include_router(module.router)