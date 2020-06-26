[![Maintainability](https://api.codeclimate.com/v1/badges/fd694687c7789977bcb3/maintainability)](https://codeclimate.com/github/mkaraev/github-analyzer/maintainability)

# github-analyzer
## Description
Simple github analyzer.

For given repo and branch retrieves:
* Most active contibutors for given time range
* Number of opened/closed pulls which created in given time range
* Number of "old" pulls which created in given time range
* Number of opened/closed issues which created in given time range

## Usage
```
usage: main.py [-h] --url URL [--since SINCE] [--until UNTIL]
               [--branch BRANCH]

optional arguments:
  -h, --help       show this help message and exit
  --url URL        Github repository url
  --since SINCE    Date from which analyzing should be done. Format YYYY-MM-
                   DD.
  --until UNTIL    Date until which analyzing should be done. Format YYYY-MM-
                   DD
  --branch BRANCH  Branch should be analyzed
```

Example

```
python main.py --url=https://github.com/OpenDiablo2/OpenDiablo2

+-----------------+-------------------+
| Contributor     | Number of commits |
+-----------------+-------------------+
| essial          | 8                 |
+-----------------+-------------------+
| carrelld        | 4                 |
+-----------------+-------------------+
| ewohltman       | 3                 |
+-----------------+-------------------+
| Ripolak         | 2                 |
+-----------------+-------------------+
| aziule          | 1                 |
+-----------------+-------------------+
| presiyan-ivanov | 1                 |
+-----------------+-------------------+
| goodevilgenius  | 1                 |
+-----------------+-------------------+
| brendanporter   | 1                 |
+-----------------+-------------------+
| joboscribe      | 1                 |
+-----------------+-------------------+
| Natureknight    | 1                 |
+-----------------+-------------------+
| gurkankaymak    | 1                 |
+-----------------+-------------------+
| Ziemas          | 1                 |
+-----------------+-------------------+
| gravestench     | 1                 |
+-----------------+-------------------+
| nicholas-eden   | 1                 |
+-----------------+-------------------+
| danhale-git     | 1                 |
+-----------------+-------------------+
| Intyre          | 1                 |
+-----------------+-------------------+
| malavv          | 1                 |
+-----------------+-------------------+
+----------------------------------------+-------+
|              Description               | count |
+========================================+=======+
| Open pulls created in given range:     | 0     |
+----------------------------------------+-------+
| Closed pulls in given range:           | 30    |
+----------------------------------------+-------+
| Closed pulls in given range:           | 0     |
+----------------------------------------+-------+
| Open issues created in given range:    | 29    |
+----------------------------------------+-------+
| Closed issues created in given range:  | 30    |
+----------------------------------------+-------+
| Open issues created in given range:    | 4     |
+----------------------------------------+-------+

```

## Project structure
```
src
├── __init__.py
├── filters.py    - filters that can be applied
├── github.py     - github api client
├── main.py       - main module
└── parser.py     - module with different parsers
```

