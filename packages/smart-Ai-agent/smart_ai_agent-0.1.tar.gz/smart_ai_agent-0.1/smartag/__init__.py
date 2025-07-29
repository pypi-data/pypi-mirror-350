import random
import requests
class user_agent:

    def user_agent_iphone():
        apple_user_agents = [
            "Mozilla/5.0 (iPhone; CPU iPhone OS 16_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.2 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_8 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.8 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 13_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.7 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (iPad; CPU OS 14_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.5 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (iPad; CPU OS 15_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.3 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (iPad; CPU OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.3 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (iPad; CPU OS 15_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Mobile/15E148 Safari/604.1"
        ]
        random_apple_user_agent = random.choice(apple_user_agents)
        return random_apple_user_agent
    
    def user_agent_samsung():
        
        samsung_user_agents = [
            "Mozilla/5.0 (Linux; Android 12; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 13; SM-S901B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 11; SM-N986B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 12; SM-F926B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.74 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 11; SM-G781B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 12; SM-A525F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.105 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 11; SM-A325F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.210 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 12; SM-T870) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
            "Mozilla/5.0 (Linux; Android 10; SM-F700F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.111 Mobile Safari/537.36"
        ]
        random_samsung_user_agent = random.choice(samsung_user_agents)
        return random_samsung_user_agent

class All:
    def random_user_agent_phone():
        rand1 = user_agent.user_agent_iphone()
        rand2 = user_agent.user_agent_samsung()
        rand_all = [rand1,rand2]

        random_all_user_agent = random.choice(rand_all)
        return random_all_user_agent




class Proxy:
    def __init__(self, number):
        self.number = int(number)
    
    def lsit_proxies(self):
        proxies = []
        
        for i in range(self.number):

            part1 = random.randint(1, 255)
            part2 = random.randint(1, 255)
            part3 = random.randint(1, 255)
            part4 = random.randint(1, 255)
        

            proxy = f"{part1}.{part2}.{part3}.{part4}:8080"
            
            proxies.append(proxy)
        
        return proxies
    @staticmethod
    def check(proxy):
        try:
            before_ip = requests.get("https://api64.ipify.org?format=json", proxies={'https': f'{proxy}'},timeout=10).json()
            with open('proxy_my.txt', 'a') as file:
                file.write(f'{proxy}\n')
            return True,before_ip['ip']
        except requests.exceptions.RequestException:
            return None


 




    