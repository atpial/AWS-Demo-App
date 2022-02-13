# powertool depencies for logger and middleware
from aws_lambda_powertools import Logger
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.event_handler.api_gateway import ApiGatewayResolver
from aws_lambda_powertools.middleware_factory import lambda_handler_decorator

app = ApiGatewayResolver()

'''logger initializer as service named "Demo-app-Logger"'''
logger = Logger(service = "Demo-app-Logger")

'''middleware logic, logic that will execute before lambda execution'''
@lambda_handler_decorator(trace_execution= True)
def middleware_factory(handler, event, context):
    #logic_before_handler_execution()
    print("Detecting the source of trigger...")
    response = handler(event, context)
    # return response
    print(response)

'''api routing, api code block will be exucuted when lambda is called from api endpoint'''
@app.get("/activity")
def display():
    logger.info("Request for displaying message received...")
    return{
        "message": "Saying Hello from API Gateway"
    }

@middleware_factory
@logger.inject_lambda_context(correlation_id_path = correlation_paths.API_GATEWAY_REST, log_event = True)
def lambda_handler(event, context):
    print("Invoking the Lambda function")
    print(event)
    return{
        "status code": 200,
        "body": "Lambda invoked successfully"
    }