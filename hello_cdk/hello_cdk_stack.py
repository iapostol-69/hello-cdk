import aws_cdk as cdk
import aws_cdk.aws_sqs as sqs
import aws_cdk.aws_lambda as lambda_
import aws_cdk.aws_lambda_event_sources as eventsources
import aws_cdk.aws_dynamodb as ddb

from constructs import Construct
#import aws_cdk.aws_s3 as s3


# Build a Stack with SQS -> lambda -> DDB
# events from sqs are picked up by a lambda, which saves them in a DDB table

class HelloCdkStack(cdk.Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        # bucket = s3.Bucket(self, "MyFirstBucket",
        #                    versioned=True,
        #                    removal_policy=cdk.RemovalPolicy.DESTROY,
        #                    auto_delete_objects=True)

        # create the SQS queue
        queue = sqs.Queue(
            self, "HelloCdkStackQueue",
            visibility_timeout=cdk.Duration.seconds(300),
        )

        # create the lambda function
        fn = lambda_.Function(self, "HelloCdkStackLambda",
                              runtime=lambda_.Runtime.PYTHON_3_8,
                              handler="handler.lambda_handler",
                              code=lambda_.Code.from_asset("src")
                              )

        # set up the queue as an event source to the lambda
        fn.add_event_source(eventsources.SqsEventSource(queue))

        # create the Dynamo DB table and grant r/w permission tot he lambda function
        table = ddb.Table(self, "HelloCdkStackDDB",
                                partition_key=ddb.Attribute(name="id", type=ddb.AttributeType.STRING))
        table.grant_read_write_data(fn)

        # the actual table name is not known until deployment, create a token and pass it as an env var to the lambda
        fn.add_environment("ddb_table", table.table_name)
