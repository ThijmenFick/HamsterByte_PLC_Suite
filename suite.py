from dataclasses import dataclass

@dataclass
class Tag:
    name: str
    type: str
    location: str
    initial_value: any
    comment: str

#ROM for all tags from the tag table
tag_table = [
    Tag("LED", "BOOL", "%QX0.0", None, ""),   # Digital output
    Tag("var", "INT", "", 0, ""),             # Normal variable
    Tag("var2", "INT", "", 2, ""),            # Fixed at 2
]

#Load in all tags into memory, change with tag_values["var"] = 2
tag_values = {tag.name: tag.initial_value for tag in tag_table}