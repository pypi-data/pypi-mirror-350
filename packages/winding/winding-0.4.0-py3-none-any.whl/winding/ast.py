from dataclasses import dataclass, field
from typing import List, Union

@dataclass
class Image:
    caption: str = field(metadata={"description": "Image caption."})
    url:     str = field(metadata={"description": "Image URL."})

@dataclass
class Markdown:
    content: Union[str, 'Markdown', Image] = field(
        metadata={"description": "Plain text, nested Markdown, or Image node."}
    )

@dataclass
class Winding:
    receivers: List[str] = field(
        default_factory=lambda: ["this"],
        metadata={"description": "The @at receivers list, identifies recipient agents."}
    )
    arguments: List[str] = field(
        default_factory=list,
        metadata={"description": "Arguments: messages like size, orientation, !negation."}
    )
    windings:    List[Union[Markdown, 'Winding']] = field(
        default_factory=list,
        metadata={"description": "Windings: messages with free text or windings."}
    )

    @property
    def at(self) -> List[str]:
        """Returns comma-separated list of receivers."""
        return ",".join(self.receivers)
