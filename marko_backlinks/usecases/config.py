from typing import Any, Dict

from dataclasses import asdict
from pathlib import Path

import yaml
from marko_backlinks.dto.dto import (
    LinkSystem,
    MarkoBacklinksConfig,
    ModifyConfig,
    ParseConfig,
    ReferenceBy,
)


def _config_from_dict(config_dict: Dict[str, Any]) -> MarkoBacklinksConfig:
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
                "reference_by", {"reference_by": ModifyConfig.reference_by}
            )["reference_by"]
        ),
    )
    return MarkoBacklinksConfig(
        parse_config=parse_config, modify_config=modify_config
    )


class Config:
    @staticmethod
    def write(path: Path, config: MarkoBacklinksConfig):
        with open(path, "w+") as config_file:
            yaml.dump(asdict(config), config_file)

    @staticmethod
    def read(path: Path) -> MarkoBacklinksConfig:
        if path.is_file():
            with open(path) as config_file:
                config_dict = yaml.full_load(config_file)
                return _config_from_dict(config_dict)
        else:
            return MarkoBacklinksConfig()
