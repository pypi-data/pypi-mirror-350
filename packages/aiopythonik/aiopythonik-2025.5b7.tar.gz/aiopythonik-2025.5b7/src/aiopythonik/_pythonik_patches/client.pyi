# src/aiopythonik/_pythonik_patches/client.pyi

from requests import Session

from .specs import (
    AssetSpec,
    CollectionSpec,
    FilesSpec,
    JobSpec,
    MetadataSpec,
    SearchSpec,
)


class PythonikClient:
    session: Session
    timeout: int
    base_url: str

    def __init__(
        self,
        app_id: str,
        auth_token: str,
        timeout: int = 3,
        base_url: str = "https://app.iconik.io",
    ) -> None:
        ...

    def acls(self) -> NotImplemented:
        ...

    def assets(self) -> AssetSpec:
        ...

    def auth(self) -> NotImplemented:
        ...

    def automations(self) -> NotImplemented:
        ...

    def collections(self) -> CollectionSpec:
        ...

    def files(self) -> FilesSpec:
        ...

    def jobs(self) -> JobSpec:
        ...

    def metadata(self) -> MetadataSpec:
        ...

    def notifications(self) -> NotImplemented:
        ...

    def search(self) -> SearchSpec:
        ...

    def settings(self) -> NotImplemented:
        ...

    def stats(self) -> NotImplemented:
        ...

    def transcode(self) -> NotImplemented:
        ...

    def users(self) -> NotImplemented:
        ...

    def users_notifications(self) -> NotImplemented:
        ...
