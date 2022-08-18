from aiohttp import web

from typing import Tuple
import datetime
import json

routes = web.RouteTableDef()


def load_files() -> Tuple[dict, dict]:
    _news = {}
    with open('news.json', 'r') as f:
        _news = json.load(f)

    _comments = {}
    with open('comments.json', 'r') as f:
        _comments = json.load(f)

    return _news, _comments


def get_datetime(date_string: str) -> datetime.datetime:
    return datetime.datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S')


async def get_news(request):
    news, comments = load_files()
    dt_now = datetime.datetime.now()
    filtered_news = {n['id']: {'comments_count': 0, **n} for n in news['news'] if
                     not n['deleted'] and get_datetime(n['date']) <= dt_now}

    for c in comments['comments']:
        if c['news_id'] in filtered_news and get_datetime(c['date']) <= dt_now:
            filtered_news[c['news_id']]['comments_count'] += 1
    filtered_news = list(filtered_news.values())
    filtered_news.sort(key=lambda x: get_datetime(x['date']), reverse=True)
    return web.json_response({"news": filtered_news, "news_count": len(filtered_news)})


async def get_news_by_id(request):
    news_id = request.match_info.get('news_id', None)
    if news_id is not None:
        news_id = int(news_id)
        news, comments = load_files()

        for n in news['news']:
            if n['id'] == news_id:
                dt_now = datetime.datetime.now()
                if not n['deleted'] and get_datetime(n['date']) <= dt_now:
                    n['comments'] = [c for c in comments['comments'] if c['news_id'] == n['id'] and get_datetime(c['date']) <= dt_now]

                    # used a date parser for excluding error with timezones if it will be added
                    n['comments'].sort(key=lambda x: get_datetime(x['date']), reverse=True)
                    n['comments_count'] = len(n['comments'])
                    return web.json_response(n)
                break
    raise web.HTTPNotFound()


if __name__ == '__main__':
    app = web.Application()
    app.add_routes([web.get('/', get_news),
                    web.get('/news/{news_id}', get_news_by_id)])
    web.run_app(app)
