from flask import Flask, request, jsonify
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
import sqlite3, time, multiprocessing, timeit, socket, json, random, threading

student_name = "Lam Yu Chun"
student_id = "13086781"

app = Flask(__name__)
JSON_CONTENT_TYPE = "application/json; charset = UTF-8"

db_str = [] # A list of strings
FILENAME = "req_stats.json"

def load_file(): # Create a file from JSON
    global db_str
    try:
        with open(FILENAME) as file:
            db_str = json.load(file)
    except FileNotFoundError:
        db_str = []

def save_file():
    with open(FILENAME, "w") as file:
        json.dump(db_str, file)

def validate_user_file(username, password):
    # Check the validation of username
    if username == None or len(username) != 4 or not username.isnumeric() or not isinstance(username, str):
        return False

    # Check the validation of password
    if password == None or not isinstance(password, str) or password[4:] == "-pw":
        return False
    
    else:
        return True

def partition(n, p):
    # Function to partition a range into p partitions
    size = n // p  # partition size, except for last partition
    starts = list(range(0, n + 1, size))[0:p]  # p start values
    stops = list(range(0, n + 1, size))[1:p] + [n + 1]  # p stop values
    return list(zip(starts, stops))

def count_in_circle(size):
    count = 0
    for i in range(size):
        x = random.random()
        y = random.random()
        if x * x + y * y < 1:
            count += 1
    return count

def pi_processes(n, p):
    start_time = timeit.default_timer()
    sizes = [stop - start for start, stop in partition(n, p)]
    with ProcessPoolExecutor() as executor:
        res = executor.map(count_in_circle, sizes)
    pi = sum(res) / n * 4
    end_time = timeit.default_timer()
    return pi, end_time - start_time

@app.post("/pi")
def pi_web_service():
    start_time = timeit.default_timer()

    # Get variables from client
    data = request.get_json()

    # Check the validation of simulations and concurrency
    if data["simulations"] is None:
        # Error handling
        return jsonify({ "error": "Missing field simulations" }), 400 # Error code 400
    if not isinstance(data["simulations"], int) or data["simulations"] not in range(100, 100000001):
        # Error handling
        return jsonify({ "error": "Invalid field simulations" }), 400 # Error code 400
    if not isinstance(data["concurrency"], int) or data["concurrency"] not in range(1, 9):
        # Error handling
        return jsonify({ "error": "Invalid field concurrency" }), 400 # Error code 400
    if not validate_user_file(data["simulations"], data["concurrency"]):
        # Error handling
        return jsonify({ "error": "user info error" }), 401 # Error code 401

    # Calculate the pi using process pools
    with ProcessPoolExecutor(max_workers=data["concurrency"]) as executor:
        result_pi = executor.submit(pi_processes, data["simulations"], data["concurrency"])

    end_time = timeit.default_timer()
    process_dur = end_time - start_time

    results = { "simulations": data["simulations"], 
               "concurrency": data["concurrency"], 
               "pi": result_pi, 
               "processing_time": process_dur }
    
    return jsonify(results)

def tcp_server_connection():
    # Connects to a TCP server and receives a quote.
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as ss:
        ss.connect(("localhost", 1700))
        quote = ss.recv(1024).decode()
        return quote

def udp_server_connection():
    # Connects to a UDP server and receives a quote.
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as ss:
        ss.sendto(("localhost", 1700))
        quote, addr = ss.recvfrom(1024)
        return quote.decode()

@app.post("/quote")
def quote_web_service():
    start_time = timeit.default_timer()

    # Get variables from client
    data = request.get_json()
    # protocol = data.get("protocol")
    # concurrency = data.get("concurrency", 1)

    # Check the validation of protocol and concurrency
    if data["protocol"] is None:
        print("hello")
        return jsonify({ "error": "Missing field protocol" }), 400 # Error code 400
    if not isinstance(data["protocol"], str) or data["protocol"] not in ["tcp", "udp"]:
        # Error handling
        return jsonify({ "error": "Invalid field protocol" }), 400 # Error code 400
    if not isinstance(data["concurrency"], int) or data["concurrency"] not in range(1, 9):
        # Error handling
        return jsonify({ "error": "Invalid field concurrency" }), 400 # Error code 400
    if not validate_user_file(data["simulations"], data["concurrency"]):
        # Error handling
        return jsonify({ "error": "user info error" }), 401 # Error code 401

    quotes = [] # A list of strings

    with ThreadPoolExecutor(max_workers=data["concurrency"]) as executor:
        if data["protocol"] == "tcp":
            def tcp_connection(): # Define a function to execute in a thread
                return tcp_server_connection()
            
            # Pass the tasks to the thread pools
            futures = [executor.submit(tcp_connection) for addr in range(data["concurrency"])]

        if data["protocol"] == "udp":
            def udp_connection(): # Define a function to execute in a thread
                return udp_server_connection()
            
            # Pass the tasks to the thread pools
            futures = [executor.submit(udp_connection) for addr in range(data["concurrency"])]
        
        # https://superfastpython.com/threadpoolexecutor-as-completed/
        # get results for tasks as they are completed with the ThreadPoolExecutor by calling the as_completed() module function
        for future in as_completed(futures):
            quotes.append(future.result())

    end_time = timeit.default_timer()
    process_dur = end_time - start_time

    results = { "protocol": data["protocol"], 
               "concurrency": data["concurrency"], 
               "quotes": quotes, 
               "processing_time": process_dur }
    
    return jsonify(results)

if __name__ == "__main__":
    app.run()