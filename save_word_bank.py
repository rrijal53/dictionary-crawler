import requests
def save():
    url = "http://testghana.org:5984/wordbank/_all_docs"

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic dGVzdGFkbWluOkdoQG5ANzMkNw=='
    }

    response = requests.request("GET", url, headers=headers)
    with open("words.json", "a+" ) as f:
        f.write(response.text.encode('utf8'))


if __name__ == '__main__':
    save()