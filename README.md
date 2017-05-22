# Tweetopo

[![Build Status](https://api.travis-ci.org/zthxxx/tweetopo.png?branch=master)](https://travis-ci.org/zthxxx/tweetopo)
[![Coverage Status](https://coveralls.io/repos/github/zthxxx/tweetopo/badge.svg?branch=master)](https://coveralls.io/github/zthxxx/tweetopo?branch=master)
[![Code Climate](https://codeclimate.com/github/zthxxx/tweetopo/badges/gpa.svg)](https://codeclimate.com/github/zthxxx/tweetopo)
[![Language](https://img.shields.io/badge/language-python3.5.0+-blue.svg)](https://www.python.org/)

A simple spider for Twitter interpersonal topology.

## preview

![three_seed_pagerank_heatmap](./document/screenshot/three_seed_pagerank_heatmap.jpg)

## What's this?

This is design for analyse **relation** between  seed users's friends, to get the **topology distribution heatmap** and the **core persons** in circle of relationship.

As shown above, the net graph consist of 1200+ friends by 3 seed users.

The three, which **two** of them are each **especial relevance**, while the **another** is **irrelevant** to either. So their friends obvious divided into **two almost separate communities** in the picture.

A node represents a person, a edge represents which two follow each. Nodes and edges dye as **heatmap**, the color from warm to cool represent the node rank value from high to low. The warmer the color, the more important the node, the colder the color, the more irrelevant the node.

Strong (warm, red)   ------>    Weak (cool, blue)

![hot_to_cold_map](./document/screenshot/hot_to_cold_map.png)



## Usage

**Its need python 3.5 and above.**

### Install

First install require packages of python,

```bash
# recommend to use venv
$ python -m venv venv
$ source venv/bin/activate
# or in win
# > venv\Scripts\activate.bat
$ pip install -r requirements.txt
```

### config

Then change the config file for **your own info**,

```bash
$ cp tweetconf.json.example tweetconf.json
$ vim tweetconf.json
```

In the config json file, you need set `twitter tokens` and `mongo connetion` and `seed user`.

`twitter tokens` and `seed user name` are a list, so you can set multi item of them, `tokens` will be used in multitheading for spider, and `seed names` decide who we crawl and analyse with. Persons info and relation stored in mongo.

### Unit test

Before run the project, you can get **unit test** at first, it used `nose`, a unit testing framework of python. 

```bash
$ packages="conffor, database, logsetting, twitter"
$ python -m nose -w . -vs --with-coverage --cover-package="$packages"
```

**Note:** database test need MongoDB and config in test package as `db_unit_test.json`; Twitter test need key and token which configured in `tweetconf.json`.

### Entry

File struct:

```shell
tweetopo/		# root directory
│
├─ document/	# doc and image
│
├─ twitter/		# twitter spider with tweepy
│
├─ netgraph/	# graph struct process and data visualization
│
├─ database/	# package for database operate
│
├─ conffor/		# package for config and csv operate
│
├─ logsetting/	# package for log system setting
│
├─ tests/		# unit test
│
├─ README.md
├─ requirements.txt
├─ tweetconf.json	# config file
├─ main.py		# entry of data spider and db operator
└─ analyse_topology.py	# entry of data analyse, csv record, draw picture
```

The `main.py` is entry of twitter spider for get data, and database operate for store and export data.

`analyse_topology.py` is entry of csv file operate for cache data list, and graph analyse for data visualization, and draw result picture.

### workflow

1. crawl and store twitter user relation data with seed
2. export db relation to `relations.json` with seed user friends
3. calculate each mutual friends cache in `mutual_friends.csv`
4. load `mutual friends` file to edges with create graph struct
5. filter low rank node out  for cache hub node to `hub_persons.csv`
6. draw net graph, PDF, CDF
7. crawl and store twitter user details data with `hub persons` uid list
8. export db person to `hub_persons.json` with `hub persons` uid list
9. merge hub list and details data to `hub_details.csv`

The result `hub_details.csv` record people`s uid, name, 3 measure ranks, lcation, description and other account details information.

## License

GPL
