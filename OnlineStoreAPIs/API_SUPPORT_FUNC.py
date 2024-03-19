from flask import Response
import json

# Error handling


def resource_not_found():
    error_message = {"Message": "Resource not found."}
    msg_json = json.dumps(error_message)
    return Response(msg_json, mimetype='application/json', status=404)


def bad_request(details="No details"):
    error_message = {"Message": "Bad request.", "Details": details}
    msg_json = json.dumps(error_message)
    return Response(msg_json, mimetype='application/json', status=400)


def server_error(details="No details"):
    error_message = {"Message": "Server error.", "Details": details}
    msg_json = json.dumps(error_message)
    return Response(msg_json, mimetype='application/json', status=500)

# Resource getters and setters


def get_resource_response(resource):
    # print(resource)
    if resource:
        return Response(json.dumps(resource), mimetype='application/json')
    return resource_not_found()


def delete_resource_response(response, resourceType):
    if response:
        msg_json = json.dumps({"Message": resourceType + " successfully deleted.", "Data": response})
        return Response(msg_json, mimetype='application/json', status=200)
    else:
        return resource_not_found()


def convert_resource_from_json(resource):
    if type(resource) is str:
        resource = json.loads(resource)
    return resource


def set_resource_response(response, resourceType, create=True):
    if create:
        status_code = 201
        action = "created"
    else:
        status_code = 200
        action = "updated"
    if response:
        msg_json = json.dumps({"Message": resourceType + " successfully " + action + ".", "Data": response})
        resp = Response(msg_json, mimetype='application/json', status=status_code)
    else:
        msg_json = json.dumps({"Message": resourceType + " not " + action + "."})
        resp = Response(msg_json, mimetype='application/json', status=500)
    return resp


def stringify_data_for_update(dict):
    '''This converts the data in a dictionary to a string format
    suitable for use in an update sql statement'''
    keys = list(dict.keys())
    data_string = ""
    for i in range(len(dict)):
        if i != 0:
            data_string += ", "
        data_string += "[" + keys[i] + "]" + " = " + format_value(dict[keys[i]])
    return data_string


def format_value(val):
    '''Use this to correctly format values for sql update statements'''
    if type(val) is str:
        val = val.replace("'", "''")
        val = "'" + val + "'"
    else:
        if type(val) is bool:
            val = int(val)
        elif val is None:
            val = "NULL"
        val = str(val)
    return val
