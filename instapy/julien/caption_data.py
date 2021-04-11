"""
Class to store the intermidiate caption Data



"""
import textwrap

class PostData:

    def __init__(self):
        self.post_id = None
        self.short_link = None
        self.caption = None
        self.creation_timestamp = None
        self.owner_account = None

    def __str__(self):
        return 'Post id : ' + str(self.post_id) + '\n' + \
                'Link : ' + str(self.short_link) + '\n' +\
                'Creation timestamp : ' + str(self.short_link) + '\n' + \
                'Owner Account : ' + str(self.owner_account) + '\n' + \
                'Description : ' + '\n' + \
                textwrap.fill(self.caption, 64) + '\n'





#taken_at_timestamp
#link
#Description
#owner account