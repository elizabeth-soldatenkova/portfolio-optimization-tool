from dataclasses import dataclass, field
from typing import Dict

@dataclass
class Project:
    name: str
    mandatory: bool
    min_year: int
    max_year: int
    elements: Dict[str, Dict[int, float]] = field(default_factory=dict)

    def __repr__(self) -> str:
        averages = [
            f'{element}: {sum(values.values()) / len(values):.1f}' if values else f'{element}: 0.0'
            for element, values in self.elements.items()
        ]
        return (f'Project(name = {self.name!r}, '
                f'Mandatory Start = {self.mandatory!r}, '
                f'Project Start Window = {self.min_year!r} - {self.max_year!r}, '
                f'\nAverage Techno-Economic Profiles=[\n    ' + ',\n    '.join(averages) + '\n  ])')
