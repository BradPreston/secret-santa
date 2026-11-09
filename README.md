# Name Exchange

A small command-line Secret Santa generator. Give it a JSON list of participants and it randomly assigns each person someone to buy a gift for, while respecting any exclusions you set (for example, so partners don't draw each other).

## Requirements

- Python 3.8 or newer
- No third-party packages

## Usage

```sh
python main.py <people-file>.json [output.json]
```

- `people-file.json` (required): the list of participants.
- `output.json` (optional): where to write the assignments. If you leave it out, the results are printed to the terminal.

## Input format

A JSON array of people. Each person needs a unique `name`. `exclude` is optional and can be a single name or a list of names.

```json
[
  { "name": "Alice", "exclude": "Bob" },
  { "name": "Bob" },
  { "name": "Carol", "exclude": ["Dave", "Erin"] },
  { "name": "Dave" },
  { "name": "Erin" }
]
```

## Output format

A JSON array in the same order as the input. `gifting` is the person they buy for.

```json
[
  { "name": "Alice", "gifting": "Carol" },
  { "name": "Bob", "gifting": "Erin" },
  ...
]
```

## Rules

- Nobody draws themselves.
- Exclusions go both ways. If Alice excludes Bob, Alice won't draw Bob **and** Bob won't draw Alice. You only need to list the exclusion on one of them.
- Each run gives a new random result.

## Errors

The script stops with an error if:

| Message | Cause |
| --- | --- |
| `Duplicate name in input` | Two people have the same `name`. |
| `<name> excludes unknown person: <other>` | An `exclude` entry doesn't match any participant's name. |
| `No valid assignment exists with these exclusions` | The exclusions are too strict for everyone to get a match, or there's only one participant. Remove some exclusions or add people. |

## Privacy note

`.gitignore` ignores all `*.json` files, so participant lists and results stay out of version control. Keep that in mind if you add other JSON files to the project.
