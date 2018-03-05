import json
import urllib
import urllib2
import os



def main():
    query_terms = raw_input("What would you like to search?")
    results = run_query(query_terms)
    for result in results:
        print(result['title'] + ":" + result['summary'] + "\n").encode("utf-8")


def read_webhose_key():
    #Read in webhose API key
    webhose_api_key = None

    
    if os.path.isfile('search.key'):
        search_location = 'search.key'
    else:
        search_location = '../search.key'

    try:
        with open(search_location,'r') as f:
            webhose_api_key = f.readline().strip()
    except:
        raise IOError('search.key file not found')

    return webhose_api_key

def run_query(search_terms, size=10):
    # Given search terms as a string and number of results to fetch (10 as default),
    #returns list of results from Webhose API

    webhose_api_key = read_webhose_key()

    if not webhose_api_key:
        raise KeyError('Webhose key not found')

    #Give root url for API
    root_url = 'http://webhose.io/search'

    #Format query string
    query_string = urllib.quote(search_terms)

    #Use string formatting to construct the API URL
    # search_url will be a string of multiple lines
    search_url = ('{root_url}?token={key}&format=json&q={query}'
                  '&sort=relevancy&size={size}').format(
                      root_url=root_url,
                      key=webhose_api_key,
                      query=query_string,
                      size=size)

    results = []

    try:
            # Connect to API and turn response into a Python dictionary
        response = urllib2.urlopen(search_url).read()
        json_response = json.loads(response)

            #iterate over posts, and convert to dictionary
        for post in json_response['posts']:
            
            results.append({'title': post['title'],'link': post['url'],'summary': post['text'][:200]})
    
    except:
        print("Error when querying the Webhose API")

    return results

if __name__ == '__main__':
    main()
