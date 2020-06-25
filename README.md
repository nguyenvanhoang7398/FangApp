Rebuild webapp checked-news:
1. Move `data_n` to `fakenewsnet_dataset`
2. Clear all logs other than `test_TWITTER_DATA_STAGE_complete.txt`
3. Remove all checked news and jobs
```
curl -X DELETE "localhost:9200/pending-news?pretty"
curl -X DELETE "localhost:9200/checked-news?pretty"
curl -X DELETE "localhost:9200/jobs?pretty"
```
4. Select the news in `misc.py`
5. Run `misc.py`
6. Update `test` job
```
curl -X POST "localhost:9200/jobs/_update/test?pretty" -H 'Content-Type: application/json' -d'
{
    "script" : {
        "source": "ctx._source.stage = params.stage",
        "lang": "painless",
        "params" : {
            "stage" : "TWITTER_DATA_STAGE"
        }
    }
}
'
```