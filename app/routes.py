""" This file contains the definition of the endpoints for the webserver """
from flask import request, jsonify
from app import webserver

def send_job_to_thread_pool(req, api_endpoint):
    """ Send the job to the thread pool for processing """
    # Check if ThreadPool is still accepting jobs
    if not webserver.tasks_runner.accepting_jobs:
        return jsonify({
            "status": "error",
            "reason": "Server is shutting down"
        })

    # Get request data
    data = req.json

    # Register job. Don't wait for task to finish
    job_id = webserver.job_counter
    webserver.tasks_runner.register_job(job_id, data, api_endpoint)

    # Increment job_id counter
    webserver.job_counter += 1

    # Return associated job_id
    return jsonify({"job_id": "job_id_" + str(job_id)})

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
    webserver.logger.info(f"Received request for states_mean with data: {request.json}")
    return send_job_to_thread_pool(request, "/api/states_mean")

@webserver.route('/api/state_mean', methods=['POST'])
def state_mean_request():
    """ Get the mean of the Data_Value column for a given state and question """
    webserver.logger.info(f"Received request for state_mean with data: {request.json}")
    return send_job_to_thread_pool(request, "/api/state_mean")

@webserver.route('/api/best5', methods=['POST'])
def best5_request():
    """ Get the best 5 states for the given question """
    webserver.logger.info(f"Received request for best5 with data: {request.json}")
    return send_job_to_thread_pool(request, "/api/best5")

@webserver.route('/api/worst5', methods=['POST'])
def worst5_request():
    """ Get the worst 5 states for the given question """
    webserver.logger.info(f"Received request for worst5 with data: {request.json}")
    return send_job_to_thread_pool(request, "/api/worst5")

@webserver.route('/api/global_mean', methods=['POST'])
def global_mean_request():
    """ Get the global mean of the Data_Value column """
    webserver.logger.info(f"Received request for global_mean with data: {request.json}")
    return send_job_to_thread_pool(request, "/api/global_mean")

@webserver.route('/api/diff_from_mean', methods=['POST'])
def diff_from_mean_request():
    """ Get the difference between global mean and
        the mean of the Data_Value column for each state, for the given question"""
    webserver.logger.info(f"Received request for diff_from_mean with data: {request.json}")
    return send_job_to_thread_pool(request, "/api/diff_from_mean")

@webserver.route('/api/state_diff_from_mean', methods=['POST'])
def state_diff_from_mean_request():
    """ Get the difference between global mean and
        the mean of the Data_Value column for a given state and question """
    webserver.logger.info(f"Received request for state_diff_from_mean with data: {request.json}")
    return send_job_to_thread_pool(request, "/api/state_diff_from_mean")

@webserver.route('/api/mean_by_category', methods=['POST'])
def mean_by_category_request():
    """ Get the mean of the Data_Value column for each category, for each state,
        for the given question """
    webserver.logger.info(f"Received request for mean_by_category with data: {request.json}")
    return send_job_to_thread_pool(request, "/api/mean_by_category")

@webserver.route('/api/state_mean_by_category', methods=['POST'])
def state_mean_by_category_request():
    """ Get the mean of the Data_Value column for each category, for a given state and question """
    webserver.logger.info(f"Received request for state_mean_by_category with data: {request.json}")
    return send_job_to_thread_pool(request, "/api/state_mean_by_category")

@webserver.route('/api/graceful_shutdown', methods=['GET'])
def graceful_shutdown_request():
    """ Gracefully shutdown the server """
    webserver.logger.info("Received request for graceful_shutdown")
    # Signal the tasks_runner to stop accepting new jobs
    if not webserver.tasks_runner.accepting_jobs:
        return jsonify({
            "status": "error",
            "reason": "Server is already shutting down"
        })

    webserver.tasks_runner.stop()

    # Return a response
    return jsonify({"status": "shutting down"})

@webserver.route('/api/jobs', methods=['GET'])
def jobs_request():
    """ Get the list of all jobs and their status """
    webserver.logger.info("Received request for jobs")
    jobs = []
    for job in webserver.tasks_runner.job_list:
        jobs.append({
            "job_id": job.job_id,
            "status": job.status
        })

    return jsonify(jobs)

@webserver.route('/api/num_jobs', methods=['GET'])
def num_jobs_request():
    """ Get the number of jobs that are currently running - in the job_queue """
    webserver.logger.info("Received request for num_jobs")
    # Get the number of jobs in the job_queue
    num_jobs = webserver.tasks_runner.job_queue.qsize()
    return jsonify({"num_jobs": num_jobs})

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
