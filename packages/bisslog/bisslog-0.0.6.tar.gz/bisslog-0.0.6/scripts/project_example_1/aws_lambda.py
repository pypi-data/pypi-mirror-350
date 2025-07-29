from scripts.project_example_1.usecases.my_first_use_case import sumar_use_case


def lambdaHandler(event, context):
    a = event.get("pathParameters").get("a")
    b = event.get("pathParameters").get("b")
    user_id = event.get("headers").get("user-id")
    return sumar_use_case(a, b, user_id)
