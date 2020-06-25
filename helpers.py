import datetime
from fang import FangManager


def es2news(es_results):
    search_results = []
    if "hits" in es_results and "hits" in es_results["hits"]:
        for hit in es_results["hits"]["hits"]:
            search_results.append(es2news_fn(hit))
    return search_results


def es2news_fn(hit):
    return {
        "title": hit["_source"]["title"],
        "label": hit["_source"]["label"],
        "url": hit["_source"]["url"],
        "source_url": hit["_source"]["source_url"],
        "source": hit["_source"]["source"],
    }


def es2pending_news(es_results):
    search_results = []
    if "hits" in es_results and "hits" in es_results["hits"]:
        for hit in es_results["hits"]["hits"]:
            ts = datetime.datetime.strptime(hit["_source"]["timestamp"], '%Y-%m-%dT%H:%M:%S.%f')
            formatted_ts = ts.strftime("%b %d, %Y")
            search_results.append({
                "title": hit["_source"]["title"],
                "url": hit["_source"]["url"],
                "timestamp": formatted_ts
            })
    return search_results


def es2checked_news(es_results):
    search_results = []
    if "hits" in es_results and "hits" in es_results["hits"]:
        for hit in es_results["hits"]["hits"]:
            search_results.append(es2checked_news_fn(hit))
    return search_results


def es2checked_news_fn(hit, parse_attn=False):
    ts = datetime.datetime.strptime(hit["_source"]["timestamp"], '%Y-%m-%dT%H:%M:%S.%f')
    formatted_ts = ts.strftime("%b %d, %Y")
    real_prob = hit["_source"]["real_prob"]
    degree = 180 * real_prob
    percentage = float("{:.2f}".format(real_prob * 100))
    engagements = hit["_source"]["engagements"]
    if parse_attn:
        for eng in engagements:
            eng["attn_tokens"] = eng["attn_tokens"].split("_")
    for eng in engagements:
        eng["url"] = "https://twitter.com/HoangNg35203228/status/{}".format(eng["tweet_id"])
    return {
        "id": hit["_id"],
        "title": hit["_source"]["title"],
        "url": hit["_source"]["url"],
        "timestamp": formatted_ts,
        "prediction": hit["_source"]["prediction"],
        "job": hit["_source"]["job"],
        "percentage": percentage,
        "degree": degree,
        "engagements": engagements
    }


def es2job(es_job):
    if "hits" in es_job and "hits" in es_job["hits"]:
        assert len(es_job["hits"]["hits"]) <= 1, "There can be at most 1 job running at a time"
        if len(es_job["hits"]["hits"]) == 1:
            hit = es_job["hits"]["hits"][0]
            current_stage = hit["_source"]["stage"]
            if current_stage == FangManager.TWEET_ID_STAGE:
                stage = "Crawling Tweet IDs"
                progress = 0
            elif current_stage == FangManager.TWITTER_DATA_STAGE:
                stage = "Crawling Twitter data"
                progress = 10
            elif current_stage == FangManager.PREPROCESS_STAGE:
                stage = "Preprocessing data"
                progress = 50
            elif current_stage == FangManager.INFERENCE_STAGE:
                stage = "Predicting"
                progress = 80
            elif current_stage == FangManager.COMPLETE_STAGE:
                stage = "Completing"
                progress = 95
            else:
                raise ValueError("Unsupported {} stage".format(current_stage))
            return {
                "stage": stage,
                "progress": progress
            }
    return None
