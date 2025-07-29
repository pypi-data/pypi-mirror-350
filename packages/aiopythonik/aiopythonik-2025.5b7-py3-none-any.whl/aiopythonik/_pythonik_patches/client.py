from pythonik.client import PythonikClient as _PythonikClient


__all__ = ["PythonikClient"]

from .specs import (
    AssetSpec,
    CollectionSpec,
    FilesSpec,
    JobSpec,
    MetadataSpec,
    SearchSpec,
)


class PythonikClient(_PythonikClient):

    def acls(self):
        """
        Access ACLs (Access Control Lists) API endpoints.

        Raises:
            NotImplementedError: ACLs endpoint not yet implemented
        """
        raise NotImplementedError(
            "ACLs endpoint is not yet implemented. "
            "Please check the documentation for updates or contribute "
            "to the pythonik project."
        )

    def assets(self) -> AssetSpec:
        return AssetSpec(self.session, self.timeout, self.base_url)

    def auth(self):
        """
        Access authentication API endpoints.

        Raises:
            NotImplementedError: Auth endpoint not yet implemented
        """
        raise NotImplementedError(
            "Authentication endpoint is not yet implemented. "
            "Please check the documentation for updates or contribute "
            "to the pythonik project."
        )

    def automations(self):
        """
        Access automations API endpoints.

        Raises:
            NotImplementedError: Automations endpoint not yet implemented
        """
        raise NotImplementedError(
            "Automations endpoint is not yet implemented. "
            "Please check the documentation for updates or contribute "
            "to the pythonik project."
        )

    def collections(self) -> CollectionSpec:
        return CollectionSpec(self.session, self.timeout, self.base_url)

    def files(self) -> FilesSpec:
        return FilesSpec(self.session, self.timeout, self.base_url)

    def jobs(self) -> JobSpec:
        return JobSpec(self.session, self.timeout, self.base_url)

    def metadata(self) -> MetadataSpec:
        return MetadataSpec(self.session, self.timeout, self.base_url)

    def notifications(self):
        """
        Access notifications API endpoints.

        Raises:
            NotImplementedError: Notifications endpoint not yet implemented
        """
        raise NotImplementedError(
            "Notifications endpoint is not yet implemented. "
            "Please check the documentation for updates or contribute "
            "to the pythonik project."
        )

    def search(self) -> SearchSpec:
        return SearchSpec(self.session, self.timeout, self.base_url)

    def settings(self):
        """
        Access settings API endpoints.

        Raises:
            NotImplementedError: Settings endpoint not yet implemented
        """
        raise NotImplementedError(
            "Settings endpoint is not yet implemented. "
            "Please check the documentation for updates or contribute "
            "to the pythonik project."
        )

    def stats(self):
        """
        Access statistics API endpoints.

        Raises:
            NotImplementedError: Stats endpoint not yet implemented
        """
        raise NotImplementedError(
            "Statistics endpoint is not yet implemented. "
            "Please check the documentation for updates or contribute "
            "to the pythonik project."
        )

    def transcode(self):
        """
        Access transcoding API endpoints.

        Raises:
            NotImplementedError: Transcode endpoint not yet implemented
        """
        raise NotImplementedError(
            "Transcoding endpoint is not yet implemented. "
            "Please check the documentation for updates or contribute "
            "to the pythonik project."
        )

    def users(self):
        """
        Access users API endpoints.

        Raises:
            NotImplementedError: Users endpoint not yet implemented
        """
        raise NotImplementedError(
            "Users endpoint is not yet implemented. "
            "Please check the documentation for updates or contribute "
            "to the pythonik project."
        )

    def users_notifications(self):
        """
        Access user notifications API endpoints.

        Raises:
            NotImplementedError: User notifications endpoint not yet
                implemented
        """
        raise NotImplementedError(
            "User notifications endpoint is not yet implemented. "
            "Please check the documentation for updates or contribute "
            "to the pythonik project."
        )
