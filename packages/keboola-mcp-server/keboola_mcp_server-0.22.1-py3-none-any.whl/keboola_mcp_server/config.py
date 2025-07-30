"""Configuration handling for the Keboola MCP server."""

import dataclasses
import logging
from dataclasses import dataclass
from enum import Enum
from typing import Mapping, Optional

LOG = logging.getLogger(__name__)


@dataclass(frozen=True)
class Config:
    """Server configuration."""

    storage_api_url: Optional[str] = None
    """The URL to the Storage API."""
    storage_token: Optional[str] = None
    """The token to access the storage API using the MCP tools."""
    workspace_schema: Optional[str] = None
    """Workspace schema to access the buckets, tables and execute sql queries."""

    @classmethod
    def _read_options(cls, d: Mapping[str, str]) -> Mapping[str, str]:
        options: dict[str, str] = {}
        for f in dataclasses.fields(cls):
            if f.name in d:
                options[f.name] = d[f.name]
            elif (dict_name := f'KBC_{f.name.upper()}') in d:
                options[f.name] = d[dict_name]
        return options

    @classmethod
    def from_dict(cls, d: Mapping[str, str]) -> 'Config':
        """
        Creates new `Config` instance with values read from the input mapping.
        The keys in the input mapping can either be the names of the fields in `Config` class
        or their uppercase variant prefixed with 'KBC_'.
        """
        return cls(**cls._read_options(d))

    def replace_by(self, d: Mapping[str, str]) -> 'Config':
        """
        Creates new `Config` instance from the existing one by replacing the values from the input mapping.
        The keys in the input mapping can either be the names of the fields in `Config` class
        or their uppercase variant prefixed with 'KBC_'.
        """
        return dataclasses.replace(self, **self._read_options(d))

    def __repr__(self):
        params: list[str] = []
        for f in dataclasses.fields(self):
            value = getattr(self, f.name)
            if value:
                if 'token' in f.name or 'password' in f.name:
                    params.append(f"{f.name}='****'")
                else:
                    params.append(f"{f.name}='{value}'")
            else:
                params.append(f'{f.name}=None')
        joined_params = ', '.join(params)
        return f'Config({joined_params})'


class MetadataField(str, Enum):
    """
    Enum to hold predefined names of Keboola metadata fields
    Add others as needed
    """

    DESCRIPTION = 'KBC.description'
