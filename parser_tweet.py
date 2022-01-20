import requests, json, time, random, configparser
from requests.auth import HTTPProxyAuth

session_headers = {
  "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0"  
}

config = configparser.ConfigParser()
config.read("config.ini")

auth = HTTPProxyAuth(config["Proxy"]["login"], config["Proxy"]["password"])
proxy = {config["Proxy"]["type"]: f'{config["Proxy"]["type"]}://{config["Proxy"]["ip"]}:{config["Proxy"]["port"]}'}

def added_comments(session, tweet, cursor="", amount=3, comments_old=[]):
  params = json.dumps({
    "focalTweetId":tweet["id"],
    "cursor":cursor,
    "rux_context":"HHwWgsC-uePaoZcpAAAA",
    "with_rux_injections":True, 
    "includePromotedContent":True,
    "withCommunity":True,
    "withQuickPromoteEligibilityTweetFields":True,
    "withTweetQuoteCount":True,
    "withBirdwatchNotes":False,
    "withSuperFollowsUserFields":True,
    "withBirdwatchPivots":False,
    "withDownvotePerspective":False,
    "withReactionsMetadata":False,
    "withReactionsPerspective":False,
    "withSuperFollowsTweetFields":True,
    "withVoice":True,
    "withV2Timeline":False,
    "__fs_interactive_text":False,
    "__fs_dont_mention_me_view_api_enabled":False
  })
  
  response = session.get("https://twitter.com/i/api/graphql/s2RO46g9Rhw53GX2BEMfiA/TweetDetail?variables=" + 
    params,
    proxies=proxy,
    auth=auth,
    headers=session_headers)
  time.sleep(random.uniform(0.5, 1.5))
  tweet_coment_all = response.json()["data"]["threaded_conversation_with_injections"]["instructions"][0]["entries"]
  tweets_coment_filt = list(filter(lambda tweet: ("conversationthread" in tweet["entryId"]) and
    ("TimelineTweet" in tweet["content"]["items"][0]["item"]["itemContent"]["itemType"]), tweet_coment_all))[:amount]
  
  tweet_coments = list(map(lambda tweet: "https://twitter.com/" + 
      tweet["content"]["items"][0]["item"]["itemContent"]["tweet_results"]["result"]["core"]["user_results"]["result"]["legacy"]["screen_name"],
      tweets_coment_filt
    ))
  tweets_coment_full = comments_old + tweet_coments
  
  if len(tweets_coment_full) == 3:
    tweet["comments"] = tweets_coment_full
  else:
    tweets_cursor = list(filter(lambda tweet: "cursor" in tweet["entryId"], tweet_coment_all))
    cursor = list(map(lambda tweet: tweet["content"]["itemContent"]["value"], tweets_cursor))
    a = 3-len(tweets_coment_filt)
    added_comments(session, tweet, cursor[0], a, tweets_coment_full)

def main():
  session = requests.Session()
  session.get("https://twitter.com", 
    proxies=proxy,
    auth=auth,
    headers=session_headers)
  time.sleep(random.uniform(0.5, 1.5))

  session_headers["authorization"] = "Bearer " \
  "AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA"
  session_headers["Content-Type"] = "application/x-www-form-urlencoded"

  response = session.post("https://api.twitter.com/1.1/guest/activate.json",
    proxies=proxy,
    auth=auth,
    headers=session_headers)
  time.sleep(random.uniform(0.5, 1.5))

  session_headers["x-guest-token"] = response.json()["guest_token"]
  session_headers["Content-Type"] = "application/json"
  session_headers["Referer"] = "https://twitter.com/elonmusk"
  session_headers["x-csrf-token"] = "a8171a3417956f5b3751f7c5ef919877"

  session.cookies["gt"] = response.json()["guest_token"]

  params = json.dumps({
    "userId":"44196397",
    "count":40,
    "withTweetQuoteCount":True,
    "includePromotedContent":True,
    "withQuickPromoteEligibilityTweetFields":True,
    "withSuperFollowsUserFields":True,
    "withBirdwatchPivots":False,
    "withDownvotePerspective":False,
    "withReactionsMetadata":False,
    "withReactionsPerspective":False,
    "withSuperFollowsTweetFields":True,
    "withVoice":True,
    "withV2Timeline":False,
    "__fs_interactive_text":False,
    "__fs_dont_mention_me_view_api_enabled":False
  })

  response = session.get(
    "https://twitter.com/i/api/graphql/jFdWt4I2nKXWbke-306dfQ/UserTweets?variables=" + params,
    proxies=proxy,
    auth=auth,
    headers=session_headers
    )
  time.sleep(random.uniform(0.5, 1.5))

  tweets_all = response.json()["data"]["user"]["result"]["timeline"]["timeline"]["instructions"][0]["entries"]
  tweets_filt = list(filter(lambda tweet: "tweet" in tweet["entryId"], tweets_all))[:10]
  tweets = list(map(lambda tweet:
    {
      "id": tweet["sortIndex"],
      "text": tweet["content"]["itemContent"]["tweet_results"]["result"]["legacy"]["full_text"]
    }, tweets_filt))

  for tweet in tweets:
    added_comments(session, tweet)

  for idx, tweet in enumerate(tweets):
    tweet_coments = "\n".join(tweet["comments"])
    print(f'\n\n{idx+1}. Tweet ID: {tweet["id"]}\n'
          f'Text: {tweet["text"]}\n' 
          f'Comments:\n{tweet_coments}')

if __name__== "__main__":
    main()
