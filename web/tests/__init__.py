from datetime import datetime, timedelta
from collections import namedtuple
from copy import deepcopy
from aiohttp import web
import json

from aiounittest import async_test
import unittest

import server


source_news = {
    "news": [
        {
            "id": 1,
            "title": "test_news_1",
            "date": (datetime.now() - timedelta(days=5)).replace(microsecond=0).strftime('%Y-%m-%dT%H:%M:%S'),
            "body": "test The news 1",
            "deleted": False
        },
        {
            "id": 2,
            "title": "test_news_2",
            "date": (datetime.now() - timedelta(days=1)).replace(microsecond=0).strftime('%Y-%m-%dT%H:%M:%S'),
            "body": "test The news 2",
            "deleted": False
        },
        {
            "id": 3,
            "title": "test_news_3",
            "date": (datetime.now() - timedelta(days=3)).replace(microsecond=0).strftime('%Y-%m-%dT%H:%M:%S'),
            "body": "test The news 3",
            "deleted": False
        },
        {
            "id": 4,
            "title": "test_news_4",
            "date": (datetime.now() - timedelta(days=2)).replace(microsecond=0).strftime('%Y-%m-%dT%H:%M:%S'),
            "body": "test The news 4",
            "deleted": True
        },
        {
            "id": 5,
            "title": "test_news_5",
            "date": (datetime.now() + timedelta(days=3)).replace(microsecond=0).strftime('%Y-%m-%dT%H:%M:%S'),
            "body": "test The news 5",
            "deleted": False
        }
    ],
    "news_count": 5
}

source_comments = {
    "comments": [
        {
            "id": 1,
            "news_id": 1,
            "title": "test_comment_1",
            "date": (datetime.now() - timedelta(days=3)).replace(microsecond=0).strftime('%Y-%m-%dT%H:%M:%S'),
            "comment": "Comment 1"
        },
        {
            "id": 2,
            "news_id": 1,
            "title": "test_comment_2",
            "date": (datetime.now() - timedelta(days=2)).replace(microsecond=0).strftime('%Y-%m-%dT%H:%M:%S'),
            "comment": "Comment 2"
        },
        {
            "id": 3,
            "news_id": 1,
            "title": "test_comment_3",
            "date": (datetime.now() - timedelta(days=1)).replace(microsecond=0).strftime('%Y-%m-%dT%H:%M:%S'),
            "comment": "Comment 3"
        },
        {
            "id": 4,
            "news_id": 1,
            "title": "test_comment_4",
            "date": (datetime.now() + timedelta(days=1)).replace(microsecond=0).strftime('%Y-%m-%dT%H:%M:%S'),
            "comment": "Comment 4"
        },
    ],
    "comments_count": 3
}

Request = namedtuple('request', ['match_info'])


class TestCli(unittest.TestCase):
    def setUp(self):

        def load_files():
            return deepcopy(source_news), deepcopy(source_comments)

        server.load_files = load_files

    @async_test
    async def test_news(self):

        res = await server.get_news({})
        self.assertEqual(res.status, 200)
        news_list = json.loads(res.text)
        self.assertEqual(news_list["news_count"], 3)
        self.assertEqual(news_list["news_count"], len(news_list["news"]))
        self.assertEqual(news_list["news"][0]["id"], 2)
        self.assertEqual(news_list["news"][2]["id"], 1)
        self.assertEqual(news_list["news"][0]["comments_count"], 0)
        self.assertEqual(news_list["news"][2]["comments_count"], 3)

    @async_test
    async def test_news_by_id(self):
        res = await server.get_news_by_id(Request(match_info={'news_id': 1}))
        self.assertEqual(res.status, 200)
        news_item = json.loads(res.text)
        self.assertEqual(news_item["comments_count"], 3)
        self.assertEqual(news_item["comments_count"], len(news_item['comments']))

    @async_test
    async def test_not_found(self):
        with self.assertRaises(web.HTTPNotFound) as context:
            await server.get_news_by_id(Request(match_info={'news_id': 500}))
        self.assertEqual(404, context.exception.status)
        with self.assertRaises(web.HTTPNotFound) as context:
            await server.get_news_by_id(Request(match_info={'news_id': -1}))
        self.assertEqual(404, context.exception.status)
        with self.assertRaises(web.HTTPNotFound) as context:
            await server.get_news_by_id(Request(match_info={'news_id': '0'}))
        self.assertEqual(404, context.exception.status)


