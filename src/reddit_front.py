import praw
import os
import logging
import datetime

class RedditFront:
    LOG = logging.getLogger(__name__)

    def __init__(self, test=False):
        user_agent = "desktop:com.halfdane.gamestopOfficial_tweet_bot:v0.0.1 (by u/half_dane)"
        self.LOG.debug("Logging in..")

        self.reddit = praw.Reddit(username=os.environ["reddit_username"],
                                  password=os.environ["reddit_password"],
                                  client_id=os.environ["reddit_client_id"],
                                  client_secret=os.environ["reddit_client_secret"],
                                  user_agent=user_agent)
        self.LOG.info(f"Logged in as {self.reddit.user.me()}")

        self.reddit.validate_on_submit = True
        self.subreddit = self.reddit.subreddit(os.environ["target_subreddit"])
        self.LOG.info(f'submitting to {self.subreddit.display_name}')

        self.test = test

    def find_tweet_post(self):
        for submission in self.reddit.user.me().submissions.new():
            if "TweetCollection" in submission.title:
                self.LOG.info(f'using {submission.title}')
                return submission
            else:
                self.LOG.info(f'ignoring {submission.title}')

    def amend_tweet_post(self, data):
        tweet_post = self.find_tweet_post()
        delimiter = "-----------------------------------------------------\n"

        parts = tweet_post.selftext.split(delimiter)
        print(parts)
        p1 = parts[0]
        if len(parts) > 1:
            p2 = parts[1]
        else:
            p2 = ""

        url = data['url']
        description = f" {data['created_at'].strftime('%Y-%m-%d %H:%M')} {url} "

        edited_body = p1 + delimiter + "\n- " + description + "  \n" + p2
        tweet_post.edit(edited_body)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    reddit_front = RedditFront(test=False)
    reddit_front.amend_tweet_post({'url': "https://twitter.com/TheRoaringKitty/status/1300164892570333186", 'created_at': datetime.datetime.now()})
