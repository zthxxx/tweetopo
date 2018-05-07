# -*- coding: utf-8 -*-
import os
from random import randint

from lib.database import relation

store = relation.people_save
query = relation.people_find
Relation = relation.Relation

uid_base = randint(86344422, 986344422)
PERSON_LENGTH = 5

EXPORT_STORE_FILE = './twitter_relations.test.json'

info = {
    'name': 'testname',
    'uid': uid_base,
    'protect': False,
    'friends_count': 4,
    'friends': [uid_base, uid_base + 1, uid_base + 2, uid_base + 3]
}


def people_info_save(info):
    store(**info)


def test_save_many_same():
    people_info_save(info)
    people_info_save(info)
    people_info_save(info)
    assert Relation.objects().count() is 1
    # It should save as only one, and not raise error.


def test_save_many_diff():
    for i in range(0, PERSON_LENGTH):
        people_info_save(info)
        info['uid'] = info['uid'] + 1
    assert Relation.objects().count() == 1 + i


def test_person_find():
    index = uid_base
    people = query(name=info['name'])
    assert people.name == info['name']
    for i in range(0, PERSON_LENGTH):
        people = query(uid=index + i)
        assert people.uid == index + i


def test_person_read_all():
    index = uid_base
    for people in Relation.objects().order_by('uid'):
        assert people.uid == index
        index += 1


def test_get_person_uids():
    index = uid_base
    uids = relation.get_uids()
    assert len(uids) is PERSON_LENGTH
    for i in range(0, PERSON_LENGTH):
        assert index + i in uids


def test_export_person_collection():
    relation.export_relation(EXPORT_STORE_FILE, seed_name=info['name'], limit=10)


def test_person_del_all():
    for people in Relation.objects():
        people.delete()
    assert Relation.objects().count() is 0


def teardown_module():
    Relation.drop_collection()
    if os.path.isfile(EXPORT_STORE_FILE):
        os.remove(EXPORT_STORE_FILE)


if __name__ == '__main__':
    test_save_many_same()
    test_save_many_diff()
    test_person_find()
    test_person_read_all()
    test_get_person_uids()
    test_export_person_collection()
    test_person_del_all()
    teardown_module()
