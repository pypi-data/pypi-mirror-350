from typing import Optional


class SecretValue:
    pass


class AWSSecretsManagerValue(SecretValue):
    def __init__(self, name: str, path: Optional[str] = None) -> None: ...


class AWSParameterStoreValue(SecretValue):
    def __init__(self, name: str, path: Optional[str] = None) -> None: ...


class AzureKeyVaultValue(SecretValue):
    def __init__(self, name: str, vault: str, vault_type: str = "secret") -> None: ...
