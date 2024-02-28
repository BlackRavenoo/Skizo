import importlib

from aiogram import Dispatcher

from config import modules_config

def enable_modules(disp: Dispatcher) -> None:
    for module, config in modules_config.items():
        if config["enabled"]:
            module = importlib.import_module(f"modules.{module}Extension.{module}")
            disp.include_router(module.router)