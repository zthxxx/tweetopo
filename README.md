# Tweetopo

[![Build Status](https://api.travis-ci.org/zthxxx/tweetopo.png?branch=master)](https://travis-ci.org/zthxxx/tweetopo)
[![Coverage Status](https://coveralls.io/repos/github/zthxxx/tweetopo/badge.svg?branch=master)](https://coveralls.io/github/zthxxx/tweetopo?branch=master)
[![Code Climate](https://codeclimate.com/github/zthxxx/tweetopo/badges/gpa.svg)](https://codeclimate.com/github/zthxxx/tweetopo)
[![Language](https://img.shields.io/badge/language-python3.5.0+-blue.svg)](https://www.python.org/)

A simple spider for Twitter interpersonal topology.



## Usage

**Its need python 3.5 and above.**

First install require packages of python,

```bash
# recommend to use venv
$ pip install -r requirements.txt
```

Then change the config file for **your own info**,

```bash
$ cp tweetconf.json.example tweetconf.json
$ vim tweetconf.json
```

Before run the project, you can get **unit test** at first,

```bash
$ packages="conffor, database, logsetting, twitter"
$ python -m nose -w . -vs --with-coverage --cover-package="$packages"
```

**Note:** database test need **MongoDB** and config in test package as `xxx-unit.json`; twitter test need key and token which configured in `tweetconf.json`.

## License

GPL