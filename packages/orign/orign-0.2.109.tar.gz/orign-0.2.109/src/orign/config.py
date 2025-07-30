from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import List, Optional

import yaml


# Original Config class for basic environment settings
class Config:
    ORIGN_ADDR = (
        os.getenv("ORIGN_ADDR")
        or os.getenv("ORIGN_SERVER")
        or os.getenv("ORIGIN_SERVER")
        or "https://orign.agentlabs.xyz"
    )
    AGENTSEA_API_KEY = os.getenv("AGENTSEA_API_KEY")
    NEBU_PROXY_URL = (
        os.getenv("NEBU_PROXY_URL")
        or os.getenv("NEBULOUS_PROXY_URL")
        or "https://proxy.agentlabs.xyz"
    )

    @classmethod
    def refresh(cls):
        """Refresh configuration by reloading environment variables."""
        cls.ORIGN_ADDR = (
            os.getenv("ORIGN_ADDR")
            or os.getenv("ORIGN_SERVER")
            or os.getenv("ORIGIN_SERVER")
            or "https://orign.agentlabs.xyz"
        )
        cls.AGENTSEA_API_KEY = os.getenv("AGENTSEA_API_KEY")
        cls.NEBU_PROXY_URL = (
            os.getenv("NEBU_PROXY_URL")
            or os.getenv("NEBULOUS_PROXY_URL")
            or "https://proxy.agentlabs.xyz"
        )


# ServerConfig for the multi-server GlobalConfig
@dataclass
class ServerConfig:
    """
    Python equivalent of the Rust ServerConfig struct.
    """

    name: Optional[str] = None
    api_key: Optional[str] = None
    server: Optional[str] = None
    auth_server: Optional[str] = None
    nebulous_server: Optional[str] = None


# Multi-server GlobalConfig reading/writing nebu.yaml
@dataclass
class GlobalConfig:
    """
    Python equivalent of the Rust GlobalConfig struct.
    Manages multiple ServerConfig entries and a current_server pointer.
    Reads/writes ~/.agentsea/nebu.yaml
    """

    servers: List[ServerConfig] = field(default_factory=list)
    current_server: Optional[str] = None

    @classmethod
    def read(cls) -> GlobalConfig:
        """
        Read the config from ~/.agentsea/nebu.yaml, or create a default if it doesn't exist.
        Then ensure that we either find or create a matching server from environment variables,
        and set that as the `current_server` if relevant (mimicking the Rust logic).
        """
        path = _get_config_file_path()
        path_exists = os.path.exists(path)
        config_modified = False  # Track if we need to write back

        # Load from disk or create a default
        if path_exists:
            try:
                with open(path, "r") as yaml_file:
                    data = yaml.safe_load(yaml_file) or {}
                # Convert each server entry into a ServerConfig
                servers_data = data.get("servers", [])
                # Ensure data is a list and elements are dicts before comprehension
                if isinstance(servers_data, list):
                    servers = [
                        ServerConfig(**srv)
                        for srv in servers_data
                        if isinstance(srv, dict)
                    ]
                else:
                    servers = []  # Or handle error appropriately
                current_server = data.get("current_server")
                config = cls(servers=servers, current_server=current_server)
            except (yaml.YAMLError, TypeError, FileNotFoundError) as e:
                # Handle potential issues during loading or parsing
                print(
                    f"Warning: Could not load or parse config file '{path}': {e}. Starting with default config."
                )
                config = cls()
                path_exists = False  # Treat as if file didn't exist for saving later
        else:
            config = cls()  # default

        # Collect environment variables (no fallback defaults here)
        env_api_key = (
            os.environ.get("ORIGN_API_KEY")
            or os.environ.get("NEBU_API_KEY")
            or os.environ.get("NEBULOUS_API_KEY")
            or os.environ.get("ORIGIN_API_KEY")
            or os.environ.get("AGENTSEA_API_KEY")
        )

        env_server = os.environ.get("ORIGN_SERVER") or os.environ.get("ORIGIN_SERVER")
        env_auth_server = (
            os.environ.get("ORIGN_AUTH_SERVER")
            or os.environ.get("ORIGIN_AUTH_SERVER")
            or os.environ.get("NEBU_AUTH_SERVER")
            or os.environ.get("NEBULOUS_AUTH_SERVER")
            or os.environ.get("AGENTSEA_AUTH_SERVER")
            or os.environ.get("AGENTSEA_AUTH_URL")
        )

        # Only proceed if all three environment variables are present
        if env_api_key and env_server and env_auth_server:
            # Find a matching server
            found_server = None
            found_server_by_name = None
            server_name = "env-based-server"

            for srv in config.servers:
                # Check if this is a server with the same name
                if srv.name == server_name:
                    found_server_by_name = srv

                # Check if server attributes match env vars
                matches_api_key = srv.api_key == env_api_key
                matches_server = srv.server == env_server
                matches_auth_server = srv.auth_server == env_auth_server

                if matches_api_key and matches_server and matches_auth_server:
                    found_server = srv
                    break

            if found_server:
                # Ensure it has a name, so we can set current_server to it
                if found_server.name is None:
                    found_server.name = server_name
                    config_modified = True  # Name was assigned
                # Use that server's name as current if it's different
                if config.current_server != found_server.name:
                    config.current_server = found_server.name
                    config_modified = True  # Current server changed
            elif found_server_by_name:
                # Update the existing server with this name instead of creating a new one
                found_server_by_name.api_key = env_api_key
                found_server_by_name.server = env_server
                found_server_by_name.auth_server = env_auth_server

                # Set current_server if it's different or wasn't set
                if config.current_server != server_name:
                    config.current_server = server_name
                    config_modified = True

                config_modified = True  # Server was updated
            else:
                # Create a new server entry if no match found by attributes or name
                new_server = ServerConfig(
                    name=server_name,
                    api_key=env_api_key,
                    server=env_server,
                    auth_server=env_auth_server,
                )
                config.servers.append(new_server)
                # Set current_server if it's different or wasn't set
                if config.current_server != server_name:
                    config.current_server = server_name
                config_modified = (
                    True  # New server added and potentially current server changed
                )

        # Write if the file didn't exist OR if we modified the config based on env vars
        if not path_exists or config_modified:
            try:
                config.write()
            except IOError as e:
                print(f"Warning: Could not write config file '{path}': {e}")

        return config

    def write(self) -> None:
        """
        Write the current GlobalConfig to disk as YAML.
        """
        path = _get_config_file_path()
        # Create parent directories if they don't exist
        os.makedirs(os.path.dirname(path), exist_ok=True)

        # Convert server list to list of dicts, handling potential None values
        servers_dict_list = []
        for srv in self.servers:
            # Create dict only with non-None values to keep YAML clean
            srv_dict = {k: v for k, v in srv.__dict__.items() if v is not None}
            servers_dict_list.append(srv_dict)

        data = {
            "servers": servers_dict_list,
            "current_server": self.current_server,
        }

        with open(path, "w") as yaml_file:
            yaml.dump(data, yaml_file, default_flow_style=False, sort_keys=False)

    def get_current_server_config(self) -> Optional[ServerConfig]:
        """
        Get the server config for the current_server name, or None if unset/missing.
        """
        if self.current_server:
            for srv in self.servers:
                if srv.name == self.current_server:
                    return srv
        return None

    def get_server_config(self, name: str) -> Optional[ServerConfig]:
        """
        Get a specific server config by name.
        """
        for srv in self.servers:
            if srv.name == name:
                return srv
        return None


def _get_config_file_path() -> str:
    """
    Return the path to ~/.agentsea/orign.yaml
    """
    home = os.path.expanduser("~")
    config_dir = os.path.join(home, ".agentsea")
    return os.path.join(config_dir, "orign.yaml")
