from aws_cdk import (
    core,
    aws_lambda as _lambda,
    aws_dynamodb,
    aws_apigateway as _apigw
)


class SoyalProxyStackStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # The code that defines your stack goes here
        # create dynamo table
        events_table = aws_dynamodb.Table(
            self, "events_table",
            partition_key=aws_dynamodb.Attribute(
                name="id",
                type=aws_dynamodb.AttributeType.STRING
            )
        )

        # Defines an AWS Lambda resource
        get_all_event_lambda = _lambda.Function(
            self, 'AllHandler',
            runtime=_lambda.Runtime.PYTHON_3_8,
            code=_lambda.Code.asset('lambda'),
            handler='allevent.handler',
        )

        get_all_event_lambda.add_environment("TABLE_NAME", events_table.table_name)

        get_event_lambda = _lambda.Function(
            self, 'GetEventHandler',
            runtime=_lambda.Runtime.PYTHON_3_8,
            code=_lambda.Code.asset('lambda'),
            handler='getevent.handler',
        )
        get_event_lambda.add_environment("TABLE_NAME", events_table.table_name)

        add_event_lambda = _lambda.Function(
            self, 'AddEventHandler',
            runtime=_lambda.Runtime.PYTHON_3_8,
            code=_lambda.Code.asset('lambda'),
            handler='addevent.handler',
        )
        add_event_lambda.add_environment("TABLE_NAME", events_table.table_name)

        # grant permission to lambda to read to children table
        events_table.grant_read_data(get_all_event_lambda)
        events_table.grant_read_data(get_event_lambda)
        events_table.grant_write_data(add_event_lambda)

        base_api = _apigw.RestApi(self, 'soyal',
        rest_api_name='soyal')

        event_entity = base_api.root.add_resource('event')
        all_entity = base_api.root.add_resource('allevents')
        
        event_entity_lambda_integration = _apigw.LambdaIntegration(get_event_lambda,proxy=True, integration_responses=[
                    {
                        'statusCode': '200',
                        'responseParameters': {
                        'method.response.header.Access-Control-Allow-Origin': "'*'",
                        }
                    }
                ])
        
        add_event_entity_lambda_integration = _apigw.LambdaIntegration(add_event_lambda,proxy=True, integration_responses=[
                    {
                        'statusCode': '200',
                        'responseParameters': {
                        'method.response.header.Access-Control-Allow-Origin': "'*'",
                        }
                    }
                ])

        get_all_entity_lambda_integration = _apigw.LambdaIntegration(get_all_event_lambda,proxy=True, integration_responses=[
                    {
                        'statusCode': '200',
                        'responseParameters': {
                        'method.response.header.Access-Control-Allow-Origin': "'*'",
                        }
                    }
                ])
        


        event_entity.add_method('GET', event_entity_lambda_integration, 
                method_responses=[{
                    'statusCode': '200',
                    'responseParameters': {
                        'method.response.header.Access-Control-Allow-Origin': True,
                    }
                }]
        )

        event_entity.add_method('POST', add_event_entity_lambda_integration, 
                method_responses=[{
                    'statusCode': '200',
                    'responseParameters': {
                        'method.response.header.Access-Control-Allow-Origin': True,
                    }
                }]
        )

        all_entity.add_method('GET', get_all_entity_lambda_integration, 
                method_responses=[{
                    'statusCode': '200',
                    'responseParameters': {
                        'method.response.header.Access-Control-Allow-Origin': True,
                    }
                }]
        )