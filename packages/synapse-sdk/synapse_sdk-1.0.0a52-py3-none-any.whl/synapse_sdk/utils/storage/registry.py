from synapse_sdk.utils.storage.providers.gcp import GCPStorage
from synapse_sdk.utils.storage.providers.s3 import S3Storage
from synapse_sdk.utils.storage.providers.sftp import SFTPStorage

STORAGE_PROVIDERS = {
    's3': S3Storage,
    'amazon_s3': S3Storage,
    'minio': S3Storage,
    'gcp': GCPStorage,
    'sftp': SFTPStorage,
}
