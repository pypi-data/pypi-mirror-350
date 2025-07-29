import requests
import os
import mimetypes
import boto3
from urllib.parse import urlencode, urlparse
import uuid
from io import BytesIO
import json


class EkaUploadError(Exception):
    """Upload related errors for Eka File Uploader"""
    pass

class EkaFileUploader:
    """
    Eka File Uploader SDK
    A simple and efficient way to handle authenticated file uploads to S3
    """
    def __init__(self, client):
        self.client = client

    def get_s3_bucket_name(self, url):
        parsed = urlparse(url)
        # Example: 'm-prod-ekascribe-batch.s3.amazonaws.com' → 'm-prod-ekascribe-batch'
        domain_parts = parsed.netloc.split('.')
        if 's3' in domain_parts:
            return domain_parts[0]
        return None
    
    def get_upload_location(self, txn_id=None, action='ekascribe', extra_data={}):
        """
        Get S3 upload location
        
        Args:
            txn_id (str, optional): Transaction ID for grouping uploads
            
        Returns:
            dict: Upload location information
        """
        try:
            params = {}
            if txn_id:
                params['txn_id'] = txn_id
                params['action'] =  action
        
            response = self.client.request(
                method="POST",
                endpoint=f"/v1/file-upload?{urlencode(params)}",
                json=extra_data
            )
            return response
        except Exception as e:
            raise EkaUploadError(f"Error getting upload location: {str(e)}")
        
    def push_ekascribe_json(self, audio_files, txn_id, extra_data={}, upload_info={}, output_format = {}):
        s3_post_data = upload_info['uploadData']
        folder_path = upload_info['folderPath']
        s3_post_data['fields']['key'] = folder_path + txn_id + '.json'
        data = {
            "client-id": self.client.client_id,
            "transaction-id": txn_id,
            "audio-file": [],
            "transfer": "non-vaded"
        }
        for item in audio_files:
            data['audio-file'].append(item.split('/')[-1])
        data["additional_data"] = extra_data
        data["output_format"] = output_format
        data.update(extra_data)
        json_bytes = BytesIO(json.dumps(data, indent=2).encode('utf-8'))
        files = {'file': ('data.json', json_bytes.getvalue(), 'application/json')}

        response = requests.post(
            s3_post_data['url'],
            data=s3_post_data['fields'],
            files=files
        )
        if response.status_code != 204:
            raise EkaUploadError(f"Upload failed: {response.text}")
        return {
            'key': folder_path + txn_id + '.json',
            'contentType': 'application/json',
            'size': len(json_bytes.getvalue())
        }

    def upload(self, file_paths, txn_id=None, action='default',extra_data={}, output_format={}):
        """
        Upload a file to S3
        
        Args:
            file_path (str): Path to the file to upload
            txn_id (str, optional): Transaction ID for grouping uploads
            action (str, optional): Action to perform on the file, one of ['ekascribe', 'default']
            extra_data (dict, optional): Extra data to send with the upload request
            
        Returns:
            dict: Upload result containing key, content type, and size
        """
        try:
            return_list = []
            if not txn_id:
                txn_id = str(uuid.uuid4())
            upload_info = self.get_upload_location(txn_id, action=action, extra_data=extra_data)

            for file_path in file_paths: 
                file_size = os.path.getsize(file_path)
                if file_size > 100 * 1024 * 1024:  # 100MB threshold
                    return_list.append(self._upload_large_file(
                        upload_info['uploadData'],
                        upload_info['folderPath'],
                        file_path
                    ))
                else:
                    return_list.append(self._upload_single_file(
                        upload_info['uploadData'],
                        upload_info['folderPath'],
                        file_path
                ))
            if action == 'ekascribe':
                self.push_ekascribe_json(file_paths, txn_id, extra_data = extra_data, upload_info= upload_info, output_format=output_format)

            if action == 'ekascribe-v2':
                try:
                    self.push_ekascribe_json(file_paths, txn_id, extra_data = extra_data, upload_info= upload_info, output_format=output_format)
                    bucket_name = self.get_s3_bucket_name(upload_info['uploadData']['url'])
                    folder_path = upload_info['folderPath']
                    
                    s3_url = f"s3://{bucket_name}/{folder_path}"

                    s3_file_paths = []

                    for file in file_paths:
                        file_name = os.path.basename(file)
                        s3_file_paths.append(f"{s3_url}{file_name}")
                    
                    payload = {
                            "s3_url": s3_url,
                            "batch_s3_url": s3_url,
                            "additional_data": extra_data,
                            "mode": extra_data.get('mode'),
                            "input_language": output_format.get('input_language'),
                            "speciality": "speciality",
                            "Section": "section",
                            "output_format_template": output_format.get('output_template'),
                            "transfer": "non-vaded",
                            "client_generated_files": s3_file_paths
                        }
                    auth_headers = {
                            "Authorization": f"Bearer {self.client.access_token}",
                        }
                    resp = requests.post(
                        url=f"https://api.eka.care/voice/api/v2/transaction/init/{txn_id}",
                        headers=auth_headers,
                        json=payload
                    )
                    if resp.status_code != 201:
                        raise EkaUploadError(f"Upload initialisation failed: {resp.json()}")
                except Exception as e:
                    raise EkaUploadError(f"Upload failed: {str(e)}")

            return return_list
        except Exception as e:
            raise EkaUploadError(f"Upload failed: {str(e)}")

    def _upload_single_file(self, upload_data, folder_path, file_path):
        """Internal method to handle single file upload"""
        file_name = os.path.basename(file_path)
        content_type = mimetypes.guess_type(file_path)[0] or 'application/octet-stream'
        
        s3_post_data = upload_data
        s3_post_data['fields']['key'] = folder_path + file_name
        
        with open(file_path, 'rb') as file:
            files = {
                'file': (file_name, file, content_type)
            }
            
            response = requests.post(
                s3_post_data['url'],
                data=s3_post_data['fields'],
                files=files
            )
            
            if response.status_code != 204:
                raise EkaUploadError(f"Upload failed: {response.text}")
            
            return {
                'key': folder_path + file_name,
                'contentType': content_type,
                'size': os.path.getsize(file_path)
            }

    def _upload_large_file(self, upload_data, folder_path, file_path, part_size=10*1024*1024):
        """Internal method to handle large file upload using multipart"""
        s3_client = boto3.client('s3')
        file_name = os.path.basename(file_path)
        content_type = mimetypes.guess_type(file_path)[0] or 'application/octet-stream'
        
        key = folder_path + file_name
        
        response = s3_client.create_multipart_upload(
            Key=key,
            ContentType=content_type
        )
        upload_id = response['UploadId']
        
        try:
            file_size = os.path.getsize(file_path)
            part_count = (file_size + part_size - 1) // part_size
            parts = []
            
            with open(file_path, 'rb') as f:
                for part_number in range(1, part_count + 1):
                    f.seek((part_number - 1) * part_size)
                    data = f.read(part_size)
                    
                    response = s3_client.upload_part(
                        Key=key,
                        PartNumber=part_number,
                        UploadId=upload_id,
                        Body=data
                    )
                    
                    parts.append({
                        'PartNumber': part_number,
                        'ETag': response['ETag']
                    })
            
            s3_client.complete_multipart_upload(
                Key=key,
                UploadId=upload_id,
                MultipartUpload={'Parts': parts}
            )
            
            return {
                'key': key,
                'contentType': content_type,
                'size': file_size
            }
            
        except Exception as e:
            s3_client.abort_multipart_upload(
                Key=key,
                UploadId=upload_id
            )
            raise EkaUploadError(f"Multipart upload failed: {str(e)}")