# need: function that formats into a post properly
# payment info, personal details, password, username, history (carshareid list)

# create a new user for the db and define the fields that it has
def new_user_post(usernm, password):
    post = {"username": usernm,
            "password": password,
            "history": []}
    return post

# add something to that user's history
def add_to_user_history(usernm, newHistory):
    post = ({"username": usernm},
            {
                "$set": {
                    "history": newHistory
                },
            })
    return post
