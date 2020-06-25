from elasticsearch import Elasticsearch
from datetime import datetime
from fang import FangManager

es = Elasticsearch()


def add_pending_news():
    pending_news = {
        # "-Mj0VXEBoEBdeO2qhoEP": {
        #     "title": "Coronavirus: Prime Minister Boris Johnson tests positive",
        #     "url": "https://www.bbc.com/news/uk-52060791",
        #     "timestamp": datetime.now()
        # },
        # "-cj1VXEBoEBdeO2qEIFj": {
        #     "title": "Google release location data to help fight coronavirus",
        #     "url": "https://cnn.com/2020/04/03/tech/coronavirus-google-data-sharing-intl-scli/index.html?utm_content=2020-04-03T22%3A27%3A04",
        #     "timestamp": datetime.now()
        # },
        # "-sj1VXEBoEBdeO2qPoG1": {
        #     "title": "Trump asks medical supply firm 3M to stop selling N95 respirators to Canada",
        #     "url": "https://www.donaldjtrump.com/",
        #     "timestamp": datetime.now()
        # },
        # "98j0VXEBoEBdeO2qUoHN": {
        #     "title": "Singapore will go into lockdown, DORSCON Red",
        #     "url": "https://web.whatsapp.com/",
        #     "timestamp": datetime.now()
        # },
        # "9sj0VXEBoEBdeO2qJ4FQ": {
        #     "title": "flu vaccine protect against coronavirus",
        #     "url": "https://twitter.com",
        #     "timestamp": datetime.now()
        # },
        # "78jyVXEBoEBdeO2qj4GH": {
        #     "url": "https://www.facebook.com/",
        #     "title": "coronavirus remains in the air for 8 hours",
        #     "timestamp": datetime.now()
        # },
        # "7cjyVXEBoEBdeO2qLIHr": {
        #     "url": "https://www.cnbc.com/2020/03/11/who-declares-the-coronavirus-outbreak-a-global-pandemic.html",
        #     "title": "WHO declares the coronavirus outbreak a global pandemic",
        #     "timestamp": datetime.now()
        # },
        # "7MjxVXEBoEBdeO2q-4HK": {
        #     "url": "http://now8news.com/covid-19-found-in-toilet-paper",
        #     "title": "COVID-19 Found in Toilet Paper",
        #     "timestamp": datetime.now()
        # },
        # "7sjyVXEBoEBdeO2qYoHr": {
        #     "url": "http://web.archive.org/web/20200329153759/https://www.webgengh.com/breaking-queen-elizabeth-tests-positive-for-covid-19/",
        #     "title": "Queen Elizabeth tests positive for COVID-19",
        #     "timestamp": datetime.now()
        # },
        # "8MjyVXEBoEBdeO2qwIHF": {
        #     "url": "https://www.msn.com/en-sg/health/medical/bill-gates-predicted-the-coronavirus-pandemic-in-his-2015-ted-talk/ar-BB11hjmz?li=BBr8Cnr",
        #     "title": "Bill Gates told us about the coronavirus in 2015",
        #     "timestamp": datetime.now()
        # },
        # "88jzVXEBoEBdeO2qnIEN": {
        #     "url": "https://www.politico.com/news/2020/04/02/trump-mask-face-coverings-coronavirus-162138",
        #     "title": "trump urge americans to cover face",
        #     "timestamp": datetime.now()
        # },
        # "8cjzVXEBoEBdeO2qO4HR": {
        #     "url": "https://www.straitstimes.com/singapore/health/most-workplaces-to-close-schools-will-move-to-full-home-based-learning-from-next",
        #     "title": "singapore schools and most workplaces will close",
        #     "timestamp": datetime.now()
        # },
        # "8sjzVXEBoEBdeO2qbYFW": {
        #     "url": "https://abcnews.go.com/Health/rapid-coronavirus-diagnostic-test-provide-results-minutes/story?id=69875037",
        #     "title": "new rapid coronavirus test in 5 minutes",
        #     "timestamp": datetime.now()
        # },
        # "9cjzVXEBoEBdeO2q-YFJ": {
        #     "url": "https://www.meadvilletribune.com/coronavirus/university-of-pittsburgh-reports-successful-covid-19-vaccine-trial/article_d9120359-38f2-589e-b474-1bfec61682a9.html",
        #     "title": "University of Pittsburgh reports successful COVID-19 vaccine trial",
        #     "timestamp": datetime.now()
        # },
        # "9MjzVXEBoEBdeO2qyIF2": {
        #     "url": "https://www.facebook.com/",
        #     "title": "drinking water kills coronavirus",
        #     "timestamp": datetime.now()
        # },
        # "-8j1VXEBoEBdeO2qcIES": {
        #     "url": "https://web.whatsapp.com/",
        #     "title": "Clapping create vibrations that virus will lose all potency",
        #     "timestamp": datetime.now()
        # },
        # "_8j2VXEBoEBdeO2qFIHl": {
        #     "url": "https://nypost.com/2020/04/05/a-bronx-zoo-tiger-now-has-coronavirus/?utm_source=url_sitebuttons&utm_medium=site%20buttons&utm_campaign=site%20buttons",
        #     "title": "bronx zoo tiger test positive for coronavirus",
        #     "timestamp": datetime.now()
        # },
        # "AMj2VXEBoEBdeO2qVoJL": {
        #     "url": "https://www.donaldjtrump.com/",
        #     "title": "COVID-19 testing on airplanes, trains",
        #     "timestamp": datetime.now()
        # },
        # "_Mj1VXEBoEBdeO2qoIGu": {
        #     "url": "https://www.facebook.com/",
        #     "title": "drinking silver liquid cures virus",
        #     "timestamp": datetime.now()
        # },
        # "_sj1VXEBoEBdeO2q0oHf": {
        #     "url": "https://www.theepochtimes.com/amazons-jeff-bezos-donates-100-million-to-food-banks-amid-unemployment-surge_3296631.html",
        #     "title": "Jeff Bezos donates $100 million to US food banks",
        #     "timestamp": datetime.now()
        # },
        "A8j2VXEBoEBdeO2q4oK8": {
            "url": "https://twitter.com/",
            "title": "Nostradamus predicted the coronavirus",
            "timestamp": datetime.now()
        },
        "Asj2VXEBoEBdeO2qtYIQ": {
            "url": "https://twitter.com/",
            "title": "Trump shut down 37 global anti-pandemic programs",
            "timestamp": datetime.now()
        },
        "Acj2VXEBoEBdeO2qhYLv": {
            "url": "https://www.bbc.com/news/uk-52192604",
            "title": "Boris Johnson moved to intensive care",
            "timestamp": datetime.now()
        },
        "Bcj3VXEBoEBdeO2qRoLY": {
            "url": "https://www.cnbc.com/2020/04/05/apple-will-produce-1-million-face-shields-per-week-for-medical-workers.html",
            "title": "Apple will produce 1 million face shields",
            "timestamp": datetime.now()
        },
        "BMj3VXEBoEBdeO2qE4IA": {
            "url": "https://facebook.com/",
            "title": "5g spread coronavirus",
            "timestamp": datetime.now()
        },
        # "B8j3VXEBoEBdeO2q2III": {
        #     "url": "https://www.washingtonpost.com/sports/2020/04/01/wimbledon-canceled-coronavirus/",
        #     "title": "wimbledon canceled due to coronavirus",
        #     "timestamp": datetime.now()
        # },
        # "Bsj3VXEBoEBdeO2qnIL5": {
        #     "url": "https://www.cnbc.com/2020/04/06/video-tesla-building-ventilators-for-covid-19-patients-from-car-parts.html",
        #     "title": "tesla produce ventilators of car",
        #     "timestamp": datetime.now()
        # },
        # "Ccj4VXEBoEBdeO2qqoI8": {
        #     "url": "https://cnn.com/2020/04/07/asia/japan-coronavirus-state-of-emergency-intl-hnk/index.html",
        #     "title": "Japan to declare state of emergency over coronavirus pandemic",
        #     "timestamp": datetime.now()
        # },
        # "CMj4VXEBoEBdeO2qQoIS": {
        #     "url": "https://cnn.com/2020/04/06/europe/russia-shooting-lockdown-scli-intl/index.html",
        #     "title": "Russian man shot five people during coronavirus lockdown",
        #     "timestamp": datetime.now()
        # },
        # "Csj5VXEBoEBdeO2qAoJJ": {
        #     "url": "https://www.ft.com/content/2fc518e0-26cd-4d5f-8419-fe71f5c55c98",
        #     "title": "Zoom send data to china",
        #     "timestamp": datetime.now()
        # },
        # "C8j5VXEBoEBdeO2qN4IX": {
        #     "url": "https://www.bbc.com/news/world-asia-india-52180660",
        #     "title": "india release unproven corona drug",
        #     "timestamp": datetime.now()
        # },
        # "DMj5VXEBoEBdeO2qdYIg": {
        #     "url": "https://www.reuters.com/article/uk-health-coronavirus-vietnam/vietnam-donates-550000-masks-to-eu-countries-in-coronavirus-fight-idUSKBN21P1IO",
        #     "title": "Vietnam donates 550,000 masks to EU countries in coronavirus fight",
        #     "timestamp": datetime.now()
        # },
        # "E8iQWXEBoEBdeO2qrIKQ": {
        #     "url": "https://web.archive.org/web/20170701053501/http://beforeitsnews.com/politics/2017/01/celebutards-call-for-total-hollywood-strike-until-trump-resigns-video-2874146.html",
        #     "title": "total Hollywood strike until Trump resigns.",
        #     "timestamp": datetime.now()
        # },
        # "FciSWXEBoEBdeO2qe4JG": {
        #     "url": "https://twitter.com",
        #     "title": "exposed to sun for hours kill coronavirus",
        #     "timestamp": datetime.now()
        # },
        # "FMiRWXEBoEBdeO2qX4JR": {
        #     "url": "http://us-news.pro/archives/980",
        #     "title": "total Hollywood strike until Trump resigns.",
        #     "timestamp": datetime.now()
        # },
        # "F8iQWnEBoEBdeO2q4oLQ": {
        #     "url": "https://www.nbcnews.com/politics/2020-election/bernie-sanders-drops-out-presidential-race-n1155156",
        #     "title": "bernie sanders drop out of presidential race",
        #     "timestamp": datetime.now()
        # },
        # "G8ioXnEBoEBdeO2qdYLb": {
        #     "url": "https://www.telegraph.co.uk/science/2020/04/07/blood-recovered-coronavirus-victims-helps-patient-come-ventilator",
        #     "title": "Blood from recovered coronavirus victims helps patient come off ventilator in just two days",
        #     "timestamp": datetime.now()
        # },
        # "GcjKWnEBoEBdeO2qb4Jw": {
        #     "url": "https://www.facebook.com/",
        #     "title": "5g spread coronavirus",
        #     "timestamp": datetime.now()
        # },
        # "GMiTWnEBoEBdeO2qfYJ0": {
        #     "url": "https://twitter.com",
        #     "title": "Bill Gates create COVID-19",
        #     "timestamp": datetime.now()
        # },
        # "GsinXnEBoEBdeO2qOYJv": {
        #     "url": "https://nypost.com/2020/04/07/51-recovered-coronavirus-patients-test-positive-again-in-south-korea/?fbclid=IwAR2O1q5c2cDEuLvH8CRECZxMadyvYlEvJxq9Ly8ZunybBWwt-1_snWw2rJw",
        #     "title": "51 recovered coronavirus patients test positive again in South Korea",
        #     "timestamp": datetime.now()
        # }
    }

    new_job = {
        "stage": FangManager.PREPROCESS_STAGE,
        "timestamp": datetime.now(),
        "last_update": datetime.now()
    }

    for news_id, news_content in pending_news.items():
        es.index(index="pending-news", body=news_content, id=news_id)

    es.index(index="jobs", body=new_job, id="test")


add_pending_news()

