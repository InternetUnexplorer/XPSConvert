from dataclasses import dataclass, field
from typing import Dict


@dataclass
class MhsAssignments:
    parameters: Dict[str, str] = field(default_factory=dict)
    bus_interfaces: Dict[str, str] = field(default_factory=dict)
    ports: Dict[str, str] = field(default_factory=dict)


@dataclass
class MhsComponent:
    peripheral_name: str
    assignments: MhsAssignments = field(default_factory=MhsAssignments)

    @property
    def instance_name(self) -> str:
        return self.assignments.parameters["INSTANCE"]


@dataclass
class MhsRoot:
    components: Dict[str, MhsComponent] = field(default_factory=dict)
    assignments: MhsAssignments = field(default_factory=MhsAssignments)
