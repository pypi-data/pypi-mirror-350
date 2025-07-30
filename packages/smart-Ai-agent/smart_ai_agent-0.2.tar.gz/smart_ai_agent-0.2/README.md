# Smart AI Agent

This library is designed for professional anonymity. It is equipped with modern technologies to generate advanced user-agents. In addition, it can generate proxies, test them, and extract only the working proxies.

## Installation

```bash
pip install smart-Ai-agent
```
## Usage

Generate User-Agent for Various Operating Systems

```python
from smart_Ai_agent import RandUserAgent

user_agent = RandUserAgent.get_user_agent()
print(user_agent)
# can you use fixed divece
#   'iphone' ,  'windows', 'mac','linux' , 'tablet','random' 
# example used create iphone
user_agent = RandUserAgent.get_user_agent('iphone')
print(user_agent)

# Get a Random User-Agent for Phones Only

user_agent = RandUserAgent.get_random_mobile_ua()
print(user_agent)

```

## Create proxies
```python
from smart_Ai_agent import Proxy
# Bring the latest and best proxies
ip = Proxy(deep=False).get_proxy()    # deep=True    is used Deep Fetch Proxies
print(ip) # output list proxy
# To make a serial output
# use 
for i in ip:
    print(i)
    print('-'*40)

```
## CHECK PROXY

```python
from smart_Ai_agent import Proxy
ch , ip = Proxy.check('143.198.42.182:31280') # auto verify is True
print(ch,ip)
#Output  True , 143.198.42.182

# verify False
ch , ip = Proxy.check('143.198.42.182:31280',verify=False)


# verify True
ch , ip = Proxy.check('143.198.42.182:31280',verify=True)

```
# Extract and check proxies
```python
from smart_Ai_agent import Proxy
proxies = Proxy(deep=True).get_proxy()
for i in proxies:
    # print(i)
    ch,ip = Proxy.check(i)
    print(ch,ip)
    print('-'*40)
```