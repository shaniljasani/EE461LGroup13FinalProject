# need: function that formats into a post properly
# password, username, history (carshareid list)


def add_new_user_to_collection(usernm, password, db):
    post = {"username": usernm,
            "password": password,
            "history": []}
    db.users.insert_one(post)


def edit_user_history(usernm, newCarshareID, user, db):
    userhist = user['history']
    # add newCarshareID to userhist
    if newCarshareID not in userhist:
        userhist.append(newCarshareID)
        # split the tuple that is returned
        id, history = ({"username": usernm},
                       {
                            "$set": {
                                "history": userhist
                            },
                       })
        # push to user collection
        db.users.update_one(id, history)
