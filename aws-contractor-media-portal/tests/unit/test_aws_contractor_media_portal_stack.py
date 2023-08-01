import aws_cdk as core
import aws_cdk.assertions as assertions

from aws_contractor_media_portal.aws_contractor_media_portal_stack import AwsContractorMediaPortalStack

# example tests. To run these tests, uncomment this file along with the example
# resource in aws_contractor_media_portal/aws_contractor_media_portal_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = AwsContractorMediaPortalStack(app, "aws-contractor-media-portal")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
