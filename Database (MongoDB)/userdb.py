# need: function that formats into a post properly
# payment info, personal details, password, username, history (carshareid list)


def new_user_post(usernm, password):
    post = {"username": usernm,
            "password": password,
            "history": []}
    return post


def add_to_user_history(usernm, newHistory):
    post = ({"username": usernm},
            {
                "$set": {
                    "history": newHistory
                },
            })
    return post
