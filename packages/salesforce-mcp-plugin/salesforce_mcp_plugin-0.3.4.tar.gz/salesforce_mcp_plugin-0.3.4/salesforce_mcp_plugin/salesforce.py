import requests

def query_accounts(access_token, instance_url, name_part):
    query = f"SELECT Id, Name FROM Account WHERE Name LIKE '%{name_part}%' LIMIT 5"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    url = f"{instance_url}/services/data/v58.0/query"
    params = {
        "q": query
    }
    res = requests.get(url, headers=headers, params=params)
    res.raise_for_status()
    records = res.json().get("records", [])
    return [f"{r['Name']} (Id: {r['Id']})" for r in records]
