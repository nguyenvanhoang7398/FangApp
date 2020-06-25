from cores.ssh_service import SshService
from utils import *
import subprocess
from elasticsearch import Elasticsearch
import elasticsearch
import logging
from datetime import datetime


class FangManager(object):
    NEWS_GRAPH_ROOT = "/home/nguyen/NewsGraph"
    FAKE_NEWS_NET_ROOT = "/home/nguyen/FakeNewsNet"
    GRAPH_LEARNING_ROOT = "/home/nguyen/GraphLearning"
    LOG_DIR = "/home/nguyen/FangLogs"
    FANG_HOST = "aws5"
    TWEET_ID_STAGE = "TWEET_ID_STAGE"
    TWITTER_DATA_STAGE = "TWITTER_DATA_STAGE"
    PREPROCESS_STAGE = "PREPROCESS_STAGE"
    INFERENCE_STAGE = "INFERENCE_STAGE"
    COMPLETE_STAGE = "COMPLETE_STAGE"
    COMPLETED_MESSAGE = "COMPLETED"

    NEWS_BUFFER_SIZE = 5
    N_LAST_LOG_LINES = 10

    def __init__(self, es_client: Elasticsearch):
        self.ssh_service = SshService()
        self.es_client = es_client

    def _get_running_log_file(self, job_id, stage):
        return os.path.join(self.LOG_DIR, "{}_{}_running.txt".format(job_id, stage))

    def _get_complete_log_file(self, job_id, stage):
        return os.path.join(self.LOG_DIR, "{}_{}_complete.txt".format(job_id, stage))

    def _get_next_stage(self, current_stage):
        if current_stage == self.TWEET_ID_STAGE:
            return self.TWITTER_DATA_STAGE
        elif current_stage == self.TWITTER_DATA_STAGE:
            return self.PREPROCESS_STAGE
        elif current_stage == self.PREPROCESS_STAGE:
            return self.INFERENCE_STAGE
        elif current_stage == self.INFERENCE_STAGE:
            return self.COMPLETE_STAGE
        else:
            raise ValueError("Unsupported stage {}".format(current_stage))

    def execute_job(self):
        current_stage = None
        pending_news_list = []
        job_id = None

        # check running job and assign stage
        try:
            es_job_result = self.es_client.search(index="jobs", body={"query": { "match_all": {} }})

            # there must be only one running job
            assert len(es_job_result["hits"]["hits"]) <= 1, "There can be at most 1 job running at a time"
            if len(es_job_result["hits"]["hits"]) == 1:
                # check the id and stage of the running job
                job_id = es_job_result["hits"]["hits"][0]["_id"]
                stage = es_job_result["hits"]["hits"][0]["_source"]["stage"]

                # check if the running job can be moved to next stage
                complete_log_file = self._get_complete_log_file(job_id, stage)
                check_complete_cmd = "cat {}".format(complete_log_file)
                output = self.ssh_service.execute(self.FANG_HOST, check_complete_cmd)
                if len(output) == 1 and output[0].rstrip("\n\r") == self.COMPLETED_MESSAGE:
                    current_stage = self._get_next_stage(stage)

                    # update job stage
                    self.es_client.update(index="jobs", id=job_id, body={
                        "script": {
                            "source": "ctx._source.stage = params.stage",
                            "lang": "painless",
                            "params": {
                                "stage": current_stage
                            }
                        }
                    })

                    # update job last update
                    self.es_client.update(index="jobs", id=job_id, body={
                        "script": {
                            "source": "ctx._source.last_update = params.last_update",
                            "lang": "painless",
                            "params": {
                                "last_update": datetime.now()
                            }
                        }
                    })

                else:
                    logging.info("Current stage has not completed.")
                    running_log_file = self._get_running_log_file(job_id, stage)
                    check_log_cmd = "tail -{} {}".format(self.N_LAST_LOG_LINES, running_log_file)
                    logs = self.ssh_service.execute(self.FANG_HOST, check_log_cmd)
                    return logs

        except elasticsearch.exceptions.NotFoundError:
            # no job is running, check if there is enough pending news to check
            logging.info("No job is running, checking for pending news.")

        # try to see if we can start a job
        if job_id is None:
            try:
                es_pending_news_results = self.es_client.search(index="pending-news", body={
                    "query": {"match_all": {}},
                    "sort": [{"timestamp": "asc"}],
                    "size": self.NEWS_BUFFER_SIZE
                })
                if es_pending_news_results["hits"]["total"]["value"] >= self.NEWS_BUFFER_SIZE:
                    # start checking pending news
                    logging.info("Set stage to {}".format(self.TWEET_ID_STAGE))
                    current_stage = self.TWEET_ID_STAGE

                    # parse es results to pending news
                    for hit in es_pending_news_results["hits"]["hits"]:
                        pending_news_list.append([hit["_id"], hit["_source"]["url"], hit["_source"]["title"]])

            except elasticsearch.exceptions.NotFoundError:
                logging.info("No pending news is found.")

        if current_stage is not None:
            if current_stage == self.TWEET_ID_STAGE:
                self._execute_tweet_id_stage(pending_news_list)
            elif current_stage == self.TWITTER_DATA_STAGE:
                self._execute_twitter_data(job_id)
            elif current_stage == self.PREPROCESS_STAGE:
                self._execute_preprocess(job_id)
            elif current_stage == self.INFERENCE_STAGE:
                self._execute_inference(job_id)
            elif current_stage == self.COMPLETE_STAGE:
                self._execute_complete(job_id)
            else:
                raise ValueError("Unsupported stage {}".format(current_stage))

    def _execute_tweet_id_stage(self, pending_news_list):
        # since this is the first stage, create a job entry
        new_job = {
            "stage": self.TWEET_ID_STAGE,
            "timestamp": datetime.now(),
            "last_update": datetime.now()
        }
        create_job_res = self.es_client.index(index="jobs", body=new_job)
        job_id = create_job_res["_id"]

        # save pending news list to a file
        tmp_news_path = os.path.join("data", "news.tsv")
        write_csv(pending_news_list, ["id", "url", "claim"], tmp_news_path,  "\t")

        # transport data to fang machine
        remote_copy_cmd = "scp {} {}:{}".format(tmp_news_path, self.FANG_HOST, os.path.join(self.FAKE_NEWS_NET_ROOT, "dataset"))
        ps = subprocess.Popen(remote_copy_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout, stderr = ps.communicate()

        # crawl tweet_ids
        working_dir = os.path.join(self.FAKE_NEWS_NET_ROOT, "code")
        script = "crawl_tweet_ids.sh"

        complete_log_file = self._get_complete_log_file(job_id, self.TWEET_ID_STAGE)
        running_log_file = self._get_running_log_file(job_id, self.TWEET_ID_STAGE)
        crawl_tweet_ids_cmd = "bash {} -p {}".format(os.path.join(working_dir, script),
                                                     complete_log_file)
        self.ssh_service.async_execute(self.FANG_HOST, crawl_tweet_ids_cmd, running_log_file, working_dir)

    def _execute_twitter_data(self, job_id):
        # simply execute crawl tweets command
        assert job_id is not None
        working_dir = os.path.join(self.FAKE_NEWS_NET_ROOT, "code")
        script = "crawl_twitter_data.sh"

        complete_log_file = self._get_complete_log_file(job_id, self.TWITTER_DATA_STAGE)
        running_log_file = self._get_running_log_file(job_id, self.TWITTER_DATA_STAGE)
        crawl_tweet_ids_cmd = "bash {} -p {} -j {}".format(os.path.join(working_dir, script),
                                                           complete_log_file, job_id)
        self.ssh_service.async_execute(self.FANG_HOST, crawl_tweet_ids_cmd, running_log_file, working_dir)

    def _execute_preprocess(self, job_id):
        # simply execute preprocess command
        assert job_id is not None
        working_dir = self.NEWS_GRAPH_ROOT
        script = "preprocess_fake_news.sh"

        complete_log_file = self._get_complete_log_file(job_id, self.PREPROCESS_STAGE)
        running_log_file = self._get_running_log_file(job_id, self.PREPROCESS_STAGE)
        preprocess_cmd = "bash {} -p {}".format(os.path.join(working_dir, script),
                                                complete_log_file)
        self.ssh_service.async_execute(self.FANG_HOST, preprocess_cmd, running_log_file, working_dir)

    def _execute_inference(self, job_id):
        # simply execute inference command
        assert job_id is not None
        working_dir = self.GRAPH_LEARNING_ROOT
        script = "infer_fake_news.sh"

        complete_log_file = self._get_complete_log_file(job_id, self.INFERENCE_STAGE)
        running_log_file = self._get_running_log_file(job_id, self.INFERENCE_STAGE)
        inference_cmd = "bash {} -p {}".format(os.path.join(working_dir, script),
                                               complete_log_file)
        self.ssh_service.async_execute(self.FANG_HOST, inference_cmd, running_log_file, working_dir)

    def _execute_complete(self, job_id):
        assert job_id is not None

        # copy inference results to local
        result_remote_path = os.path.join(self.GRAPH_LEARNING_ROOT, "infer.tsv")
        result_local_path = os.path.join("data", "infer.tsv")
        attn_remote_path = os.path.join(self.GRAPH_LEARNING_ROOT, "infer_attn.tsv")
        attn_local_path = os.path.join("data", "infer_attn.tsv")

        result_remote_copy_cmd = "scp {}:{} {}".format(self.FANG_HOST, result_remote_path, result_local_path)
        ps = subprocess.Popen(result_remote_copy_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout, stderr = ps.communicate()

        attn_remote_copy_cmd = "scp {}:{} {}".format(self.FANG_HOST, attn_remote_path, attn_local_path)
        ps = subprocess.Popen(attn_remote_copy_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout, stderr = ps.communicate()

        # read infer results, save to checked news and remove from pending news of ES
        infer_results = read_csv(result_local_path, False, "\t")
        infer_attns = read_csv(attn_local_path, False, "\t")
        for i, result_row in enumerate(infer_results):
            news_id, prediction, real_prob, fake_prob = result_row[0], result_row[1], \
                                                        float(result_row[2]), float(result_row[3])
            attn_row = infer_attns[i]
            attn_users, attn_tweets, stances, stance_attn_toks = \
                attn_row[1].split(" "), attn_row[2].split(" "), attn_row[3].split(" "), attn_row[4].split(" ")
            engagements = []
            for user_id, tweet_id, stance, attn_tokens in zip( attn_users, attn_tweets, stances, stance_attn_toks):
                engagements.append(
                    {
                        "user_id": remove_tag(user_id),
                        "tweet_id": remove_tag(tweet_id),
                        "stance": stance,
                        "attn_tokens": attn_tokens
                    }
                )

            news_id = remove_tag(news_id)   # extract the actual news id
            res = self.es_client.get(index="pending-news", id=news_id)
            pending_news = res['_source']
            title = pending_news["title"]
            url = pending_news["url"]
            ts = pending_news["timestamp"]
            checked_news = {
                "title": title,
                "url": url,
                "timestamp": ts,
                "prediction": prediction,
                "real_prob": real_prob,
                "fake_prob": fake_prob,
                "job": job_id,
                "engagements": engagements
            }

            # save checked news
            self.es_client.index(index="checked-news", body=checked_news, id=news_id)

            # remove pending news
            self.es_client.delete(index="pending-news", id=news_id)

        self.es_client.delete(index="jobs", id=job_id)
