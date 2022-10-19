import tweepy
import configparser
import pandas as pd
import click
import re

@click.command()
@click.option('--username', prompt = 'Twitter username (no @)')
@click.option('--retweets', prompt = 'Include retweets? (y/n)', default = 'n')
def gcm_twitter_bot(username, retweets):

    """Creates csv file of 10 most recent tweets from given twitter handler
        Args:
            username (String): Twitter handle (no @)
            retweets (String): 'y' or 'n' that enables user to choose whether csv should have retweets
        Return:
            None
    """

    # Read config file
    config = configparser.RawConfigParser()
    config.read('config.ini')

    # Fetch API Access Keys
    api_key = config['twitter']['API_KEY']
    api_key_secret = config['twitter']['API_KEY_SECRET']
    access_token = config['twitter']['ACCESS_TOKEN']
    access_token_secret = config['twitter']['ACCESS_TOKEN_SECRET']

    # Authenticate Twitter API
    auth = tweepy.OAuthHandler(api_key, api_key_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    #Call Twitter API
    if retweets == 'y':
        retweets  = True
    else:
        retweets = False

    try:    
        tweets = api.user_timeline(screen_name = username, include_rts = retweets)
    except Exception as e:
        print(e)
        return

    #Parse tweets for a max of 10 most recent tweets
    tweets_to_export = []
    username = '@' + username    
    for i in range(min(10, len(tweets))):
            tweet = remove_emojis(tweets[i].text)
            hashtag_num = len(tweets[i].entities.get('hashtags'))
            tweets_to_export.append([username, tweet, hashtag_num])

    #Format Data to CSV
    columns = ['Twitter Username', 'Tweet', 'Hashtags']    
    df = pd.DataFrame(tweets_to_export, columns=columns)
    df.to_csv(username + '.csv', index=False)

    #Print information on CSV before returning
    print('CSV file created: ' + username + '.csv')
    return

def remove_emojis(text):

    """Removes emojis from string
        Args:
            text (String): String with emojis + other undesirable characters
        Return:
            String with removed emojis
    """

    regex_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002702-\U000027B0"  # additional undesirable characters
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U00010000-\U0010ffff"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u200d"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\ufe0f"  # dingbats
                               u"\u3030"
                               "]+", flags=re.UNICODE)
    return regex_pattern.sub(r'', text)

if __name__ == '__main__':
    gcm_twitter_bot()