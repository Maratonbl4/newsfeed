import datetime, time
import random
import json

news = {'news': []}
comments = {'comments': []}

comment_id = 1

for n_id in range(1, 5):
    tp = random.randint(1577836800, 1704067200)     # 2020-01-01T00:00:00 to 2024-01-01T00:00:00 UTC

    news['news'].append({
        "id": n_id,
        "title": f"news_{n_id}",
        "date": datetime.datetime.fromtimestamp(tp).strftime('%Y-%m-%dT%H:%M:%S'),
        "body": f"The news {n_id}",
        "deleted": random.choice([True, False, False])
    })
    if tp < time.time():
        c_count = random.randint(0, 5)
        cs = [{
                    "id": comment_id + c_id,
                    "news_id": n_id,
                    "title": f"comment_{comment_id + c_id}",
                    "date": datetime.datetime.fromtimestamp(random.randint(tp, int(time.time()))).strftime('%Y-%m-%dT%H:%M:%S'),
                    "comment": f"Comment {comment_id + c_id}"
                } for c_id in range(0, c_count)]
        comments['comments'].extend(cs)
        comment_id += c_count
news['news_count'] = len(news['news'])
comments['comments_count'] = len(comments['comments'])
with open('../news.json', 'w', encoding='utf-8') as f:
    json.dump(news, f, indent=4)

with open('../comments.json', 'w', encoding='utf-8') as f:
    json.dump(comments, f, indent=4)
