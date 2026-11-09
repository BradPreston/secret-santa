#!/usr/bin/env python3
"""Secret Santa generator.
 
Usage: python main.py <people-file>.json [output.json]
 
Input:  [{"name": "Alice", "exclude": "Bob"}, {"name": "Bob"}, ...]
Output: [{"name": "Alice", "gifting": "Carol"}, ...]
 
Rules:
- Nobody gets themselves.
- If a person has an `exclude`, the two are never paired in either direction.
  (`exclude` may be a single name or a list of names.)
"""
import sys
import json
import random
from typing import Dict, List, Set, TypedDict, Union


class _PersonRequired(TypedDict):
    name: str


class Person(_PersonRequired, total=False):
    exclude: Union[str, List[str]]

def build_blocked(people: List[Person]):
    names = {p["name"] for p in people}
    # nobody gifts themselves, example output {bob: {bob}}
    blocked = {n: {n} for n in names}
    for p in people:
        ex = p.get("exclude")
        # if person doesn't contain exclude key, continue
        if not ex:
            continue
        for other in [ex] if isinstance(ex, str) else ex:
            # raise an error if the exclude name doesn't exist in the participant names
            if other not in names:
                raise ValueError(f"{p['name']} excludes unknown person: {other}")
            # add excluded participant to the name
            blocked[p["name"]].add(other)
            blocked[other].add(p["name"])  # symmetric
    return blocked

def assign(people: List[Person]) -> List[Dict[str, str]]:
    names = [p["name"] for p in people]
    if len(set(names)) != len(names):
        raise ValueError("Duplicate name in input")
    blocked = build_blocked(people)

    givers = names[:] # clone the names list into givers
    random.shuffle(givers)
    used: Set[str] = set() # the list of names who are already being gifted to
    result: Dict[str, str] = {} # the dictionary containing the giver (key) and receiver (value)

    # assign each giver a receiver
    def solve(i: int):
        # if every giver has a receiver, return
        if i == len(givers):
            return True
        giver = givers[i]
        # the list of available names for the giver to gift to
        options = [n for n in names if n not in blocked[giver] and n not in used]
        random.shuffle(options)
        for receiver in options:
            # assign the receiver to the giver
            result[giver] = receiver
            # mark the receiver as taken
            used.add(receiver)
            # test if everyone after this can still be properly assigned a receiver
            if solve(i + 1):
                return True
            # remove the receiver because they are not used due to the solve failing
            used.discard(receiver)
            # giver has no receiver, so delete the giver from results
            del result[giver]
        # let the previous giver know that it needs to pick a different receiver
        return False

    if not solve(0):
        raise ValueError("No valid assignment exists with these exclusions")
    return [{"name": n, "gifting": result[n]} for n in names]

def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    with open(sys.argv[1]) as f:
        people = json.load(f)
    out = json.dumps(assign(people), indent=2)
    if len(sys.argv) > 2:
        with open(sys.argv[2], "w") as f:
            f.write(out + "\n")
    else:
        print(out)
 
 
if __name__ == "__main__":
    main()