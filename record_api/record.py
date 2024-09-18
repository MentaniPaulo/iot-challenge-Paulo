from flask import Flask, request, jsonify
import requests
import redis
from datetime import datetime
import sys
import json
import os 
import time

app = Flask(__name__) 
redis_host = os.getenv('REDIS', '127.0.0.1') 
cache = redis.Redis(host=f'{redis_host}', port=6379, decode_responses=True)

CAMERA_API_URL = 'http://camera_container:5000'  


def check_time_integrity(month: int, day: int) -> bool:
    """
    Checks if the provided month and day are within valid ranges.

    Args:
        month (int): The month to check.
        day (int): The day to check.

    Returns:
        bool: True if the month or day is out of valid range, False otherwise.
    """
    if(month > 12 or month < 1):
        return True
    if(day > 31 or day < 1):
        return True

    return False

def check_parameters_integrity(start_time: str, end_time: str) -> bool: 
    """
    Validates the start and end times to ensure they are in the correct format and that start time is less than end time.

    Args:
        start_time (str): Start time in the format "HH:MM:SS".
        end_time (str): End time in the format "HH:MM:SS".

    Returns:
        bool: True if there is a format error or if start time is not less than end time, False otherwise.
    """
    time_format = "%H:%M:%S"
    
    try: 
        start = datetime.strptime(start_time, time_format)
        end = datetime.strptime(end_time, time_format) 
        if( start < end):
            return False # valid time
        else:
            return True
    except ValueError: 
        return True

def filter_camera_data(data, start_time:str, end_time:str, type_record:int) -> list:
    """
    Filters camera data based on record type and time range.

    Args:
        data (dict): The camera data to filter.
        start_time (str): Start time in the format "HH:MM:SS".
        end_time (str): End time in the format "HH:MM:SS".
        type_record (int): The type of record to filter.

    Returns:
        list: A list of records that match the criteria.
    """
    if data.get("result") != "success":
        return []
    
    records = data.get("data").get("record")[0]

    found_records = []
    for each_record in records:  
        if each_record.get("record_type") != int(type_record): 
            continue

        data_begin = datetime.strptime(each_record.get("start_time"), "%H:%M:%S")
        data_end = datetime.strptime(each_record.get("end_time"), "%H:%M:%S")
        begin_request = datetime.strptime(start_time, "%H:%M:%S")
        end_request = datetime.strptime(end_time, "%H:%M:%S")

        # check time inside range user asked for
        # 
        if(( begin_request >= data_begin and begin_request < data_end) or 
            ( end_request >= data_begin and end_request < data_end)    or
            ( begin_request < data_begin and end_request >= data_end )) :
            found_records.append(each_record)
        

    return found_records

def get_data_by_day(month, day): 
    """
    This function first checks if the data for the specified month and day is available in the cache. 
    
    If the data is found in the cache, it is returned immediately. If not, the function makes an API request 
    to retrieve the data and then stores this data in the cache for future requests. 
    The cached data will expire after 24 hours (86400 seconds).

    Args:
        month (int): The month of the data to retrieve.
        day (int): The day of the data to retrieve.

    Returns:
        dict: The data retrieved from the cache or API.
    """
    cache_check = cache.get(f'/month/{month}/day/{day}')
    get_day_dump = {}

    if(cache_check):
        get_day_dump = json.loads(cache_check)
    else:
        get_day_dump = requests.get(f'{CAMERA_API_URL}/month/{month}/day/{day}') 
        
        if get_day_dump.status_code != 404: 
            cache.setex(f"/month/{month}/day/{day}", 86400,  json.dumps(get_day_dump))
        else: 
            cache.setex(f"/month/{month}/day/{day}", 86400,  json.dumps({"result":"error"}))
            get_day_dump = None

   
    return get_day_dump 
 
@app.route('/record_data/month/<int:month>/day/<int:day>', methods=['GET'])
def get_record_data(month, day):
    """
    Handles the endpoint to get record data for a specific month and day, filtered by start time, end time, and record type.

    Args:
        month (int): The month of the records to retrieve.
        day (int): The day of the records to retrieve.

    Returns:
        Response: JSON response with the filtered records or an error message.
    """
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')
    record_type = request.args.get('record_type')
     
    #avoid unnecessary API calls
    if(
       check_time_integrity(month, day) or
       check_parameters_integrity(start_time, end_time)):
        response = jsonify({
            "error": "Invalid Parameters", 
        })
        response.status_code = 404
        return response
     
    data = get_data_by_day(month, day)
    
    if(data == None):
        response = jsonify({
            "error": "Not Found", 
        })
        response.status_code = 404
        return response
    
    if(data.get("error")):
        return data
    
    result = filter_camera_data(data, start_time, end_time, record_type)
            
    response_json = {"results": result}
        
    if response_json:
        return jsonify(response_json)
    else:
        return ('', 404)

@app.errorhandler(404)
def not_found(error):
    """
    Custom handler for 404 errors.
    Args:
        error: The error object.
    Returns:
        Response: JSON response with error details.
    """

    response = jsonify({
        "error": "Not Found",
        "message": error.description
    })
    response.status_code = 404
    return response

    
if __name__ == '__main__': 
    app.run(debug=True)
