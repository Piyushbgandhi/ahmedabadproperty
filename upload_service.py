

import boto3
from PIL import Image
import io

class UploadService:
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION")
        )
        self.bucket_name = os.getenv("S3_BUCKET_NAME")
    
    async def upload_property_image(self, file, property_id):
        """Upload and optimize property image to S3"""
        # Compress image
        # Upload to S3
        # Return image URL
    
    async def delete_property_image(self, image_url):
        """Delete image from S3"""

        