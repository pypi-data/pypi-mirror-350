import boto3

class ConnectionS3:
    def __init__(
        self, 
        bucket: str, 
        service_name: str, 
        aws_access_key_id: str, 
        aws_secret_access_key: str, 
        endpoint_url: str, 
        **kwargs
    ) -> None:
        self.bucket = self.S3_CONFIGURATION.get('bucket')

        self.client = boto3.client(
            service_name=self.S3_CONFIGURATION.get('service_name'),
            aws_access_key_id= self.S3_CONFIGURATION.get('aws_access_key_id'), 
            aws_secret_access_key=self.S3_CONFIGURATION.get('aws_secret_access_key'), 
            endpoint_url=self.S3_CONFIGURATION.get('endpoint_url'),
            config=self.config
        )
