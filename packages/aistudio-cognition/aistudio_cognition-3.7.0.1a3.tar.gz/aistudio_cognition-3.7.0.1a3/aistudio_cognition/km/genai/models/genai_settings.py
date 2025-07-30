from dataclasses import dataclass

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class GenAI:
    url: str
    km_project_id: str
    km_project_secret: str
