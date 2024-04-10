#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Input validation function for gender
def validate_gender(gender):
    if gender not in [0, 1]:  # Assuming 0 is male, 1 is female
        return False
    return True


# Input validation function for date of birth (dob)
def validate_dob(dob):
    try:
        datetime.strptime(dob, '%Y-%m-%d')
        return True
    except ValueError:
        return False


# Input validation function for biography (bio)
def validate_bio(bio):
    if bio is None or not isinstance(bio, str) or len(bio) > 300: # 300 max length can be changed
        return False
    return True


# update: this updates the user's top tracks/artists
@app.route('/update', methods=['POST'])
def update():
    user_id = request.form.get("id")
    auth_token = request.form.get("token")

    if not validate_user_id(user_id):
        return api.response(jsonify({"status": "fail", "message": "Invalid user ID"}))

    if not validate_auth_token(auth_token):
        return api.response(jsonify({"status": "fail", "message": "Invalid authentication token"}))

    response = {}

    # Fetch other fields from request
    name = request.form.get("name")
    gender = request.form.get("gender")
    dob = request.form.get("dob")
    bio = request.form.get("bio")
    image = request.form.get("image")

    # Validate gender
    if not validate_gender(gender):
        return api.response(jsonify({"status": "fail", "message": "Invalid gender"}))

    # Validate dob
    if not validate_dob(dob):
        return api.response(jsonify({"status": "fail", "message": "Invalid date of birth"}))

    # Validate bio
    if not validate_bio(bio):
        return api.response(jsonify({"status": "fail", "message": "Invalid biography"}))

    # Proceed with update logic

    return api.response(jsonify(response))

