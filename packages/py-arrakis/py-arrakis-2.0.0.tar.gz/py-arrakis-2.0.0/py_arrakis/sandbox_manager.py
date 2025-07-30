"""
Manager module for handling multiple sandbox VM instances.
"""

from .client import APIClient
from .sandbox import Sandbox
from . import API_VERSION


class SandboxManager:
    """Manages sandbox VMs through the REST API."""

    def __init__(self, base_url: str):
        """Initialize the sandbox manager.

        Args:
            base_url: Base URL of the sandbox management server (e.g. 'http://localhost:8080')
        """
        self._api = APIClient(base_url)

    def list_all(self) -> list[Sandbox]:
        """List all sandbox VMs.

        Returns:
            List of Sandbox instances representing all VMs.

        Raises:
            Exception: If the API request fails.
        """
        response = self._api.get(f"{API_VERSION}/vms")
        return [Sandbox(self._api, vm.get("vmName")) for vm in response.get("vms", [])]

    def destroy_all(self) -> None:
        """Delete all sandbox VMs.

        Raises:
            Exception: If the API request fails.
        """
        self._api.delete(f"{API_VERSION}/vms")

    def restore(self, vm_name: str, snapshot_id: str) -> Sandbox:
        """Restore a VM from a snapshot.

        Args:
            vm_name: Name to give to the restored VM.
            snapshot_id: ID of the snapshot to restore from.

        Returns:
            Sandbox: A new Sandbox instance representing the restored VM.

        Raises:
            Exception: If the API request fails.
        """
        self._api.post(f"{API_VERSION}/vms", {"vmName": vm_name, "snapshotId": snapshot_id})

        return Sandbox(self._api, vm_name)

    def start_sandbox(self, name: str) -> Sandbox:
        """Start a new sandbox VM.

        Args:
            name: Name to give to the new VM.

        Returns:
            Sandbox: A new Sandbox instance representing the started VM.

        Raises:
            Exception: If the API request fails.
        """
        self._api.post(f"{API_VERSION}/vms", {"vmName": name})
        return Sandbox(self._api, name)
