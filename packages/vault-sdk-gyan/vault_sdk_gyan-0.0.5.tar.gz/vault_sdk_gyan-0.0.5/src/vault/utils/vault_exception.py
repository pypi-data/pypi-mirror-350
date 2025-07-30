from dataclasses import dataclass


@dataclass
class VaultException(Exception):
    def __init__(self, message):
        self.message = message
