import facebook
from keys import *
import json


# Get Graph
graph = facebook.GraphAPI(access_token=access_token_pg)

FILE_NAME = 'last_post_id.txt'


# Retrive last post id
def retrieve_last_post_id(file_name):
    f_read = open(file_name, 'r')
    last_post_id = str(f_read.read())
    f_read.close()
    return last_post_id


# Store Last Post Id
def store_last_post_id(last_post_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_post_id))
    f_write.close()
    return


# Get the active user's page posts
def get_posts():

    # get post data for current page , fields contain the required post fields
    # set limit to n to get last n posts
    posts = graph.get_connections(id='me', connection_name='feed', limit=5, fields='message,link,created_time')

    # Reversed to get posts in the order/time created i.e older first and newest last
    for post in reversed(posts['data']):
        # Print data from Post
        print(json.dumps(post, sort_keys=False, indent=4))
        # print(post['id'])

        # To like,delete, comment on multiple posts together call the like,delete comment Functions here
        # And Pass the post id and message(for comment)
        # eg. like_post(post['id'])
        last_post_id = post['id']

    # To get id of last post id
    store_last_post_id(last_post_id, FILE_NAME)


# Create New Post On Page
def post_to_fb():
    graph.put_object(
       parent_object="me",
       connection_name="feed",
       message="This is a great website. Everyone should visit it.",
       link="https://example.com")
    print("Posted On facebook")


# Create Multiple New Posts On Page
def multiple_post_to_fb():
    messages = ["Test message 1", "Test message 2", "Test message 3", "Test message 4"]
    for message in messages:
        graph.put_object(
           parent_object="me",
           connection_name="feed",
           message=message,
           link="https://example.com")
        print("Posted " + message + " On facebook")


# Delete Post By Id
def delete_post(post_id):
    # last_seen_id = retrieve_last_seen_id(FILE_NAME)
    # to get last stored post id (Use get_posts to store latest post id)
    graph.delete_object(id=post_id)
    print("Post with ID " + post_id + " Deleted")


# Comment On Post By Id
def comment_on_post(post_id, message):
    graph.put_comment(object_id=post_id, message=message)
    print("Commented On the Post")


# Like Post
def like_post(post_id):
    graph.put_like(object_id=post_id)
    print("Liked Post")


print("Current Post Ids:")
get_posts()


# Example Delete Post

# post_to_fb()
# id = retrieve_last_post_id(FILE_NAME)

# delete_post(id)

# print("Remaining Post IDs:")
# get_posts()
