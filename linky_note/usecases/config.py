from typing import Any, Dict

from dataclasses import asdict
from pathlib import Path

import yaml
from linky_note.dto.dto import (
    LinkSystem,
    LinkyNoteConfig,
    ModifyConfig,
    ParseConfig,
    ReferenceBy,
)


def _config_from_dict(config_dict: Dict[str, Any]) -> LinkyNoteConfig:
    parse_config = ParseConfig(
        parse_wikilinks=config_dict.get(
            "parse_config", ParseConfig.parse_wikilinks
        ),
    )
    modify_config = ModifyConfig(
        link_system=LinkSystem(
            config_dict.get(
                "modify_config", {"link_system": ModifyConfig.link_system}
            )["link_system"]
        ),
        reference_by=ReferenceBy(
            config_dict.get(
                "modify_config", {"reference_by": ModifyConfig.reference_by}
            )["reference_by"]
        ),
    )
    return LinkyNoteConfig(
        parse_config=parse_config, modify_config=modify_config
    )


class Config:
    @staticmethod
    def write(path: Path, config: LinkyNoteConfig):
        with open(path, "w+") as config_file:
            yaml.dump(asdict(config), config_file)

    @staticmethod
    def read(path: Path) -> LinkyNoteConfig:
        if path.is_file():
            with open(path) as config_file:
                config_dict = yaml.full_load(config_file)
                return _config_from_dict(config_dict)
        else:
            return LinkyNoteConfig()
