import re

USER_TAG, NEWS_TAG, SOURCE_TAG, COMMUNITY_TAG = "user", "news", "source", "community"


def tag(entity_type, entity):
    return "{}_{}".format(entity_type, entity)


def is_tag(entity_type, entity):
    return entity.startswith(entity_type)


def remove_tag(tagged_entity):
    return tagged_entity.split("_", 1)[-1]


def remove_url(url_str):
    text = re.sub(r"http\S+", "", url_str)
    return text