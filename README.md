# Twitter-Automation

This serves a few purposes:
-Login to Twitter automatically
-To scrape users' twitter handle from a specific page and store them as pickle
-Read the pickle file and follow those users
-Unfollow your own followers
-Tweet images at scheduled time intervals

The whole system requires 2 pickle files. One is used for storing users' handle as never followed or followed (0 or 1). The other is used to store uploaded pictures' name to not tweet them twice.

Both those pickle files must be created manually by dumping an empty list into them. (This is not included in the current repository)

Careful not to follow more than 200-250 users a day.
Also unfollowing should be done very sparsely if at all.
