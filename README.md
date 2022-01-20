# Twitter parser 

Parser first 10 posts from Elon Musk's Twitter page and first 3 comments for every post

## Configurating 

Fill in ~config.ini~ your autentification data
For example 
``` 
[Proxy]
login = "your_proxy_login"
password = "your_proxy_password"
ip = "your_proxy_ip"
port = "your_proxy_port"
type = "http" # or "https"
```

## Running 

```
pip3 install -r requirements.txt
python3 parser_tweet.py
```
