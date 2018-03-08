import oci
import argparse
import os
from oci.config import validate_config
import json
from multiprocessing import Process
from glob import glob


# config = {
#    "user": "ocid1.user.oc1..******************************************************",
#    "key_file": "/Users/****/Documents/oci_api_key.pem",
#    "fingerprint": "88:df:**:**:**:**:**:**:**:**:**:",
#    "pass_phrase":"****",
#    "tenancy": "ocid1.tenancy.oc1..***********************************",
#    "region": "us-ashburn-1"
# }


if __name__ == "__main__":

    description = "\n".join(["This utility is meant to pull files from a directory in a OCI bucket"])

    parser = argparse.ArgumentParser(description=description,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(dest='bucket_name',
                        help="Name of object storage bucket")
    parser.add_argument(dest='directory',
                        help="Path to local directory containing files to upload. Do not include trailing path delimiter.")
    parser.add_argument('config')
    args = parser.parse_args()

    bucket_name = args.bucket_name

    directory = args.directory
    config = args.config
    if not os.path.isdir(directory):
        parser.usage()
    else:
        dir = directory + os.path.sep + "*"

    print("Opening Config")
    with open(config, 'r') as file:
        configFile = eval(file.read())

    validate_config(configFile)
    object_storage = oci.object_storage.ObjectStorageClient(configFile)
    namespace = object_storage.get_namespace().data

    data = object_storage.list_objects(namespace, bucket_name)
    for obj in data.data.objects:
        print(obj.name)
        get_obj = object_storage.get_object(namespace, bucket_name, obj.name)
        with open(directory+'/'+obj.name, 'wb') as f:
            for chunk in get_obj.data.raw.stream(1024 * 1024, decode_content=False):
                f.write(chunk)

