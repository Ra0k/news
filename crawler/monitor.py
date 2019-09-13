import feedparser
import requests

headers = {}

ADD_ARTICLE = """
mutation ArticleCreate($feed: ID!, $title: String!, $description: String!, $url: String!) {
  createArticle(input: {feed: $feed, title: $title, description: $description, url: $url}) {
    article {
      id
      title
      description
    }
  }
}"""

def run_query(query, variables):
    request = requests.post('http://localhost:8001/graphql/', json={'query': query, 'variables': variables}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))


while(1):
  feed = feedparser.parse('http://feeds.bbci.co.uk/news/world/europe/rss.xml')

  for item in feed['items']:
    variables = {
      "feed": "RmVlZE5vZGU6MQ==",
      "title": item['title'],
      "description": item['summary'],
      "url": item['link']
    }

    run_query(ADD_ARTICLE, variables)
