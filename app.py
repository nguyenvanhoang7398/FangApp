from flask import Flask, render_template, request, redirect
import helpers
from apscheduler.schedulers.background import BackgroundScheduler
from fang import *

app = Flask(__name__)
es = Elasticsearch()
fang_manager = FangManager(es_client=es)
scheduler = BackgroundScheduler()


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/search', methods=['GET'])
def posts():
    query = request.args.get('q')
    try:
        es_results = es.search(index="news", body={"query": {"match": {"title": query }}})
        verified_news = helpers.es2news(es_results)
    except elasticsearch.NotFoundError:
        verified_news = []
    return render_template('results.html', results=verified_news, query=query)


@app.route('/fang', methods=['GET', 'POST'])
def fang():
    if request.method == 'POST':
        title = request.form['title']
        url = request.form['url']
        pending_news = {
            "title": title,
            "url": url,
            "timestamp": datetime.now()
        }
        es.index(index="pending-news", body=pending_news)
        return redirect('/fang')
    else:
        try:
            pending_es = es.search(index="pending-news", body={"query": {"match_all": {}},
                                                               "sort": [{"timestamp": "desc"}]})
            pending_news = helpers.es2pending_news(pending_es)
        except elasticsearch.exceptions.NotFoundError:
            pending_news = []
        try:
            checked_es = es.search(index="checked-news", body={"query": {"match_all": {}},
                                                               "sort": [{"timestamp": "desc"}],
                                                               "size": 50})
            checked_news = helpers.es2checked_news(checked_es)
        except elasticsearch.exceptions.NotFoundError:
            checked_news = []

        job = {
            "progress": 100,
            "stage": "Idle"
        }
        try:
            job_es = es.search(index="jobs", body={"query": {"match_all": {}}})
            job = helpers.es2job(job_es) or job
        except elasticsearch.exceptions.NotFoundError:
            pass

        return render_template('fang.html', job=job, pending_news=pending_news, checked_news=checked_news)


if __name__ == "__main__":
    scheduler.add_job(func=fang_manager.execute_job, trigger="interval", seconds=300)
    scheduler.start()
    app.run(host='0.0.0.0')