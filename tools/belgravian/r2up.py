import os, sys, boto3, mimetypes
from concurrent.futures import ThreadPoolExecutor
env = dict(l.strip().split('=',1) for l in open(sys.argv[1]) if '=' in l)
s3 = boto3.client('s3', endpoint_url=env['R2_ENDPOINT'], aws_access_key_id=env['AWS_ACCESS_KEY_ID'],
                  aws_secret_access_key=env['AWS_SECRET_ACCESS_KEY'], region_name='auto')
root = sys.argv[2]; prefix = sys.argv[3]   # e.g. belgravian/
files = []
for sub in sys.argv[4:]:
    for d, _, fs in os.walk(os.path.join(root, sub)):
        for f in fs: files.append(os.path.join(d, f))
existing = set()
for p in s3.get_paginator('list_objects_v2').paginate(Bucket='belgravian-archive', Prefix=prefix):
    for o in p.get('Contents', []): existing.add((o['Key'], o['Size']))
def up(f):
    key = prefix + os.path.relpath(f, root)
    if (key, os.path.getsize(f)) in existing: return 0
    ct = mimetypes.guess_type(f)[0] or ('image/webp' if f.endswith('.webp') else 'application/octet-stream')
    s3.upload_file(f, 'belgravian-archive', key, ExtraArgs={'ContentType': ct, 'CacheControl': 'public, max-age=31536000'})
    return 1
with ThreadPoolExecutor(16) as ex: n = sum(ex.map(up, files))
print(len(files), 'files,', n, 'uploaded')
