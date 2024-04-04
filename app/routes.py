""" This file contains the definition of the endpoints for the webserver """
from flask import request, jsonify
from app import webserver

# Example endpoint definition
@webserver.route('/api/post_endpoint', methods=['POST'])
def post_endpoint():
    """ Example POST endpoint """
    if request.method == 'POST':
        # Assuming the request contains JSON data
        data = request.json
        print(f"got data in post {data}")

        # Process the received data
        # For demonstration purposes, just echoing back the received data
        response = {"message": "Received data successfully", "data": data}

        # Sending back a JSON response
        return jsonify(response)

    # Method Not Allowed
    return jsonify({"error": "Method not allowed"}), 405

@webserver.route('/api/get_results/<job_id>', methods=['GET'])
def get_response(job_id):
    """ Get the result of a job by job_id if exists """
    webserver.logger.info(f"Received request for job_id: {job_id}")
    # Check if job_id is valid
    job_id_nr = int(job_id.split("_")[-1])
    if job_id_nr > webserver.job_counter:
        return jsonify({
            "status": "error",
            "reason": "Invalid job_id"
        })

    # Check if job is still running
    for job in webserver.tasks_runner.job_list:
        if job.job_id == job_id_nr:
            if job.status == "running":
                return jsonify({
                    "status": "running"
                })
            return jsonify({
                "status": "done",
                "data": job.result
            })

    # If job is not found
    return jsonify({
        "status": "error",
        "reason": "Job not found"
    })

@webserver.route('/api/states_mean', methods=['POST'])
def states_mean_request():
    """ Get the mean of the Data_Value column for each state for the given question """
    webserver.logger.info("Received request for states_mean with data: {}".format(request.json))
    # Get request data
    data = request.json

    # Register job. Don't wait for task to finish
    job_id = webserver.job_counter
    webserver.tasks_runner.register_job(job_id, data, "/api/states_mean")

    # Increment job_id counter
    webserver.job_counter += 1

    # Return associated job_id
    return jsonify({"job_id": "job_id_" + str(job_id)})

@webserver.route('/api/state_mean', methods=['POST'])
def state_mean_request():
    """ Get the mean of the Data_Value column for a given state and question """
    webserver.logger.info(f"Received request for state_mean with data: {request.json}")
    # Get request data
    data = request.json

    # Register job. Don't wait for task to finish
    job_id = webserver.job_counter
    webserver.tasks_runner.register_job(job_id, data, "/api/state_mean")

    # Increment job_id counter
    webserver.job_counter += 1

    # Return associated job_id
    return jsonify({"job_id": "job_id_" + str(job_id)})

@webserver.route('/api/best5', methods=['POST'])
def best5_request():
    """ Get the best 5 states for the given question """
    webserver.logger.info(f"Received request for best5 with data: {request.json}")
    # Get request data
    data = request.json

    # Register job. Don't wait for task to finish
    job_id = webserver.job_counter
    webserver.tasks_runner.register_job(job_id, data, "/api/best5")

    # Increment job_id counter
    webserver.job_counter += 1

    # Return associated job_id
    return jsonify({"job_id": "job_id_" + str(job_id)})

@webserver.route('/api/worst5', methods=['POST'])
def worst5_request():
    """ Get the worst 5 states for the given question """
    webserver.logger.info(f"Received request for worst5 with data: {request.json}")
    # Get request data
    data = request.json

    # Register job. Don't wait for task to finish
    job_id = webserver.job_counter
    webserver.tasks_runner.register_job(job_id, data, "/api/worst5")

    # Increment job_id counter
    webserver.job_counter += 1

    # Return associated job_id
    return jsonify({"job_id": "job_id_" + str(job_id)})

@webserver.route('/api/global_mean', methods=['POST'])
def global_mean_request():
    """ Get the global mean of the Data_Value column """
    webserver.logger.info(f"Received request for global_mean with data: {request.json}")
    # Get request data
    data = request.json

    # Register job. Don't wait for task to finish
    job_id = webserver.job_counter
    webserver.tasks_runner.register_job(job_id, data, "/api/global_mean")

    # Increment job_id counter
    webserver.job_counter += 1

    # Return associated job_id
    return jsonify({"job_id": "job_id_" + str(job_id)})

@webserver.route('/api/diff_from_mean', methods=['POST'])
def diff_from_mean_request():
    """ Get the difference between global mean and
        the mean of the Data_Value column for each state, for the given question"""
    webserver.logger.info(f"Received request for diff_from_mean with data: {request.json}")
    # Get request data
    data = request.json

    # Register job. Don't wait for task to finish
    job_id = webserver.job_counter
    webserver.tasks_runner.register_job(job_id, data, "/api/diff_from_mean")

    # Increment job_id counter
    webserver.job_counter += 1

    # Return associated job_id
    return jsonify({"job_id": "job_id_" + str(job_id)})

@webserver.route('/api/state_diff_from_mean', methods=['POST'])
def state_diff_from_mean_request():
    """ Get the difference between global mean and
        the mean of the Data_Value column for a given state and question """
    webserver.logger.info(f"Received request for state_diff_from_mean with data: {request.json}")
    # Get request data
    data = request.json

    # Register job. Don't wait for task to finish
    job_id = webserver.job_counter
    webserver.tasks_runner.register_job(job_id, data, "/api/state_diff_from_mean")

    # Increment job_id counter
    webserver.job_counter += 1

    # Return associated job_id
    return jsonify({"job_id": "job_id_" + str(job_id)})

@webserver.route('/api/mean_by_category', methods=['POST'])
def mean_by_category_request():
    """ Get the mean of the Data_Value column for each category, for each state,
        for the given question """
    webserver.logger.info(f"Received request for mean_by_category with data: {request.json}")
    # Get request data
    data = request.json

    # Register job. Don't wait for task to finish
    job_id = webserver.job_counter
    webserver.tasks_runner.register_job(job_id, data, "/api/mean_by_category")

    # Increment job_id counter
    webserver.job_counter += 1

    # Return associated job_id
    return jsonify({"job_id": "job_id_" + str(job_id)})

@webserver.route('/api/state_mean_by_category', methods=['POST'])
def state_mean_by_category_request():
    """ Get the mean of the Data_Value column for each category, for a given state and question """
    webserver.logger.info(f"Received request for state_mean_by_category with data: {request.json}")
    # Get request data
    data = request.json

    # Register job. Don't wait for task to finish
    job_id = webserver.job_counter
    webserver.tasks_runner.register_job(job_id, data, "/api/state_mean_by_category")

    # Increment job_id counter
    webserver.job_counter += 1

    # Return associated job_id
    return jsonify({"job_id": "job_id_" + str(job_id)})

@webserver.route('/api/graceful_shutdown', methods=['POST'])
def graceful_shutdown_request():
    """ Gracefully shutdown the server """
    webserver.logger.info("Received request for graceful_shutdown")
    # Signal the tasks_runner to stop accepting new jobs
    webserver.tasks_runner.stop()

# You can check localhost in your browser to see what this displays
@webserver.route('/')
@webserver.route('/index')
def index():
    """ Display the available routes on the webserver """
    routes = get_defined_routes()
    msg = "Hello, World!\n Interact with the webserver using one of the defined routes:\n"

    # Display each route as a separate HTML <p> tag
    paragraphs = "\n".join(f"<p>{route}</p>" for route in routes)

    msg += paragraphs
    return msg

def get_defined_routes():
    """ Get the defined routes for the webserver """
    routes = []
    for rule in webserver.url_map.iter_rules():
        methods = ', '.join(rule.methods)
        routes.append(f"Endpoint: \"{rule}\" Methods: \"{methods}\"")
    return routes
