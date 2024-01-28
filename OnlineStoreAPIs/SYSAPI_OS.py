from flask import Flask, Response, request, render_template, send_file, redirect
import SYSAPI_OS_USER_FUNC as sysUser, json, API_SUPPORT_FUNC as api

port = 5016
app = Flask("SYSAPI_OS")


## USER
@app.route("/users")
def get_users():
    return api.get_resource_response(sysUser.get_users())


@app.route("/users/<id>")
def get_user(id):
    return api.get_resource_response(sysUser.get_users(id))

@app.route("/users", methods=["POST"])
def create_users():
    raw_resource = api.convert_resource_from_json(request.json)
    if type(raw_resource) == list:
        return api.set_resource_response(sysUser.create_users_from_array(raw_resource), "User")
    else:
        return api.set_resource_response(sysUser.create_user(raw_resource), "User")
    

@app.route("/users/<id>", methods=["PUT"])
def update_user_(id):
    raw_resource = api.convert_resource_from_json(request.json)
    return api.set_resource_response(sysUser.update_user_by_id(id, raw_resource), "User", False)

@app.route("/users/<id>", methods=["DELETE"])
def delete_user(id):
    return api.delete_resource_response(sysUser.delete_user_by_id(id), "User")

if __name__=="__main__":
    app.run(debug=True, port=port) 
    # When no port is specified, starts at default port 5000