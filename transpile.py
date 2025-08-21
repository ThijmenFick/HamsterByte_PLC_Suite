from dataclasses import dataclass
import sys
import re

#Get the full size of objects for compiler
def getDeepSize(obj, seen=None):
    """Recursively finds the memory footprint of an object and all its contents."""
    if seen is None:
        seen = set()

    objId = id(obj)
    if objId in seen:
        return 0  # Avoid double counting
    seen.add(objId)

    size = sys.getsizeof(obj)

    if isinstance(obj, dict):
        size += sum(getDeepSize(k, seen) + getDeepSize(v, seen) for k, v in obj.items())
    elif isinstance(obj, (list, tuple, set, frozenset)):
        size += sum(getDeepSize(i, seen) for i in obj)

    return size

def varTranspile(tag):
    pretype = tag.type
    replacements = {
        "BOOL": "bool",
        "INT": "int"
    }

    initValue = ""
    if tag.initialValue == "FALSE" or tag.initialValue == "TRUE":
        initValue = tag.initialValue.lower()
    else:
        initValue = tag.initialValue

    type = " ".join(replacements.get(word.strip(), word.strip()) for word in pretype.split(" "))
    return f"{type} {tag.name} = {initValue};"

def transpile(line, statement):
    constructed = ""
    if statement == "if":
        constructed += "if ("
        replacements = {
            "IF": "if (",
            "THEN": ") {",
            "AND": "&&",
            "OR": "||",
            "NOT": "!",
            "<>": "!="
        }
        operandsContent = " ".join(replacements.get(word.strip(), word.strip()) for word in line.split(" "))
        print(operandsContent)

@dataclass
class Tag:
    name: str
    type: str
    location: str
    initialValue: any
    comment: str

#ROM for all tags from the tag table
tagTable = [
]

linesBetween = []
allLines = []
with open("code.txt") as f:
    for lineno, line in enumerate(f, start=1):
        allLines.append(line.strip())
        stripped = line.strip()
        if stripped == "VAR":
            insideBlock = True
            continue
        elif stripped == "END_VAR":
            insideBlock = False
            continue

        if insideBlock:
            linesBetween.append(line.strip())
            newVar = line.strip().split("=")
            newTag = Tag(newVar[0], newVar[1], newVar[2], newVar[3], newVar[4])
            tagTable.append(newTag)

#Load in all tags into memory, change with tag_values["var"] = 2
tagValues = {tag.name: tag.initialValue for tag in tagTable}

#======== Find and Load all vars in mem ========#
print(f"Found {len(linesBetween)} variable(s)")
print(f"Loaded VARROM into RAM with a total of {getDeepSize(tagValues)} bytes in size")

#======== Generating C-headers based on packages and vars ========#
print("Generating C-headers")
with open("code.c", "a") as f:
    f.write('#include <stdio.h>\n#include <string.h>\n#include <stdlib.h>\n#include <stdint.h>\n#include <stdbool.h>\n#include "driver/gpio.h"\n#include "freertos/FreeRTOS.h"\n#include "freertos/task.h"\n\n')

    for tag in tagTable:
        f.write(f"{varTranspile(tag)}\n")

for l in allLines:
    if l.startswith("IF") and l.endswith("THEN"):
        print("Detected a IF-statement")


