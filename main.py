import os
import tweepy


def main():
    while True:
        os.system('cls||clear')
        option = input('1.) To clean tweets \n2.) Clean favorites \n3.) Clean followers \n')

        if option == '1':
            clear_tweets()
            break
        elif option == '2':
            clean_favorites()
            break
        elif option == '3':
            clean_followers()
            break


def clear_tweets():
    api = get_api()
    count = 0
    for tweet in tweepy.Cursor(api.user_timeline).items():
        api.destroy_status(tweet.id)
        count += 1
    print("Deleted " + str(count) + " tweets!")


def clean_favorites():
    api = get_api()
    count = 0
    for tweet in tweepy.Cursor(api.favorites).items():
        api.destroy_favorite(tweet.id)
        count += 1
    print("Deleted " + str(count) + " favorites!")


def clean_followers():
    api = get_api()
    ids = []
    for page in tweepy.Cursor(api.followers_ids, screen_name=api.me().screen_name).pages():
        ids.extend(page)

    print(str(len(ids)) + " followers found....")

    for follower in ids:
        api.create_block(follower)

    for block in api.blocks_ids():
        api.destroy_block(block)

    print("cleaned all followers!")


def get_api():
    auth = tweepy.OAuthHandler(os.environ.get('key'), os.environ.get('secret'))
    auth.set_access_token(os.environ.get('token'), os.environ.get('token_secret'))
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)
    return api


main()
