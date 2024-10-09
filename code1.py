import boto3

# Initialize EC2 and S3 clients
ec2 = boto3.resource('ec2', region_name='eu-north-1')
s3 = boto3.client('s3', region_name='eu-north-1')

# Create EC2 instance
instances = ec2.create_instances(
    ImageId='ami-097c5c21a18dc59ea',  
    MinCount=1,
    MaxCount=1,
    InstanceType='t3.micro',
    KeyName='test',
    SecurityGroupIds=['sg-08dc18918d1ddad45']
)
print(f'EC2 instance created: {instances[0].id}')

# Create S3 bucket
bucket_name = 'bucketchakri'
s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={
    'LocationConstraint': 'eu-north-1'})  # Specify your AWS region
print(f'S3 bucket created: {bucket_name}')