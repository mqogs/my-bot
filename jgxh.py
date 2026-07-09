def get_username():
    global email
    while True:
        try:
            LsD = ''.join(random.choices(string.ascii_letters + string.digits, k=32))            
            bol = json.dumps({"id": str(random.randrange(10000, 53186034340)), "render_surface": "PROFILE"})         
            response = requests.post("https://www.instagram.com/api/graphql", headers={"X-FB-LSD": LsD, 'User-Agent': str(UserAgentGenerator),}, data = {"lsd": LsD, "variables": bol, "doc_id": "25618261841150840"})
            username = response.json()['data']['user']['username']     
            
            email = username + "@gmail.com"    
            Ahmed(email)            
        except:
            pass
                   

threads = []
for i in range(10):
    t = threading.Thread(target=get_username)
    threads.append(t)
    t.start()
for t in threads:
    t.join()
