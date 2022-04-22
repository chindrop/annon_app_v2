import os
from app.s3_helpers import configure_boto
from botocore.errorfactory import ClientError

def upload_files_from_subsample_wavs(s3bucket, directory):
    total = len(os.listdir(directory))
    done = 0
    error = 0
    count = 0 
    couldn_upload = []
    while count < total:
        for wav_file in os.listdir(directory):
            key = wav_file.split('.')[0]
            print(f"Uploading {wav_file} to S3 with the name {key}")
            f = os.path.join(directory, wav_file)
            if os.path.isfile(f):
                try:
                    s3bucket.Object(key).load()
                    done += 1
                    count += 1
                    print(f"{key} already exists in S3")
                    pass
                except ClientError:
                    try:
                        s3bucket.upload_file(f, key, ExtraArgs={'ContentType': 'audio/wav'})
                        done += 1
                        count += 1
                        print(f"{key} uploaded to S3")
                    except Exception as e:
                        print(f"Error uploading {wav_file} to S3: {e}")
                        error += 1
                        count += 1
                        couldn_upload.append(wav_file)
                        pass
        if error > 10:
            print("Too many errors, exiting")
            break
    print(f"Done: {done} Errors: {error} Count: {count}")
    
        

upload_files_from_subsample_wavs(configure_boto()[1], os.path.abspath('./app/static/subsample_wavs')) # bucket, directory