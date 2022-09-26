"""
Twitter周りのハンドリングを行う
参考:
* https://zenn.dev/ryo427/articles/aeb7aaf22aa8f9
* https://github.com/twitterdev/Twitter-API-v2-sample-code/blob/main/Filtered-Stream/filtered_stream.py

"""
import traceback
import requests
import os
import time
import json
import tweepy
from dotenv import load_dotenv

load_dotenv()

consumer_key = os.environ['API_KEY']
consumer_secret = os.environ['API_KEY_SECRET']
access_token = os.environ['ACCESS_TOKEN']
access_token_secret = os.environ['ACCESS_TOKEN_SECRET']
bearer_token = os.environ['BEARER_TOKEN']

Client = tweepy.Client(bearer_token, consumer_key, consumer_secret, access_token, access_token_secret)


def bearer_oauth(r):
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2FilteredStreamPython"
    return r


def get_rules():
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream/rules", auth=bearer_oauth
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot get rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print(json.dumps(response.json()))
    return response.json()


def delete_all_rules(rules):
    if rules is None or "data" not in rules:
        return None

    ids = list(map(lambda rule: rule["id"], rules["data"]))
    payload = {"delete": {"ids": ids}}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        auth=bearer_oauth,
        json=payload
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot delete rules (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    print(json.dumps(response.json()))


def set_rules(delete):
    rules = [
        {
            "value": "to:sample_bot_wata"
        }
    ]
    payload = {"add": rules}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        auth=bearer_oauth,
        json=payload,
    )
    if response.status_code != 201:
        raise Exception(
            "Cannot add rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print(json.dumps(response.json()))


def get_stream(set):
    run = 1
    while run > 0:
        try:
            with requests.get(
                    "https://api.twitter.com/2/tweets/search/stream", auth=bearer_oauth, stream=True,
            ) as response:
                print(response.status_code)
                if response.status_code != 200:
                    raise Exception(
                        "Cannot get stream (HTTP {}): {}".format(
                            response.status_code, response.text
                        )
                    )
                for response_line in response.iter_lines():
                    if response_line:
                        json_response = json.loads(response_line)
                        tweet_id = json_response["data"]["id"]  # ツイートID
                        reply_text = json_response["data"]["text"]  # 相手の送ってきた内容

                        # 投稿フォーマットのバリデーション

                        # DB（SpreadSheet）にデータを追加する

                        # DB（SpreadSheet）走査して集計
                        # count == 5 -> "NFTをgiveawayします"
                        # count == 10 -> "のれんがグレードアップします"
                        # else -> "ナイスTOTONOTTA♨️！"

                        text = "ナイスTOTONOTTA♨️！"

                        print(text)
                        Client.create_tweet(
                            text=text,
                            in_reply_to_tweet_id=tweet_id
                        )
        except ChunkedEncodingError as chunkError:
            print(traceback.format_exc())
            time.sleep(6)
            continue
        except ConnectionError as e:
            print(traceback.format_exc())
            run += 1
            if run < 10:
                time.sleep(6)
                print("再接続します", str(run) + "回目")
                continue
            else:
                run = 0
        except Exception as e:
            # some other error occurred.. stop the loop
            print("Stopping loop because of un-handled error")
            print(traceback.format_exc())
            run = 0


def retweet(tweetId):
    print("TODO: retweet処理を行う")


def validation_tweet_format():
    print("投稿データのバリデーションを行う")


class ChunkedEncodingError(Exception):
    pass
