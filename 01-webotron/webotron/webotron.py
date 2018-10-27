#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Webotron: Deploy Websites with AWS.

Webotron automate process of deploying website using aws

- Configure AWS s3 Buckets
    - Create them
    - Set them up for static website hosting
    -  Deploy Local Files to them
- Configure DNS with AWS Route 53
- Configure a Content Delievery Network and SSL with AWS cloudfront
"""

import boto3
import click
from bucket import BucketManager


session=  None
bucket_manager = None
@click.group()
@click.option('--profile', default=None, help="User a Given AWS Service")
def cli(profile):
    """Deploys websites to AWS."""
    global session, bucket_manager
    
    session_cfg = {}
    if profile:
        session_cfg['profile_name'] = profile
    session = boto3.Session(**session_cfg)
    bucket_manager = BucketManager(session)



@cli.command('list-buckets')
def list_buckets():
    """List all s3 buckets."""
    for bucket in bucket_manager.all_buckets():
        print(bucket)


@cli.command('list-bucket-objects')
@click.argument('bucket')
def list_bucket_objects(bucket):
    """List Objects in S3 Bucket."""
    for obj in bucket_manager.all_objects(bucket):
        print(obj)


@cli.command('setup-bucket')
@click.argument('bucket')
def setup_bucket(bucket):
    """Create and Configure S3 Bucket."""
    s3_bucket = bucket_manager.init_bucket(bucket)
    bucket_manager.set_policy(s3_bucket)
    bucket_manager.configure_website(s3_bucket)

    return


@cli.command('sync')
@click.argument('pathname', type=click.Path(exists=True))
@click.argument('bucket')
def sync(pathname, bucket):
    """Sync Contents of PATHNAME to Bucket."""
    bucket_manager.sync(pathname, bucket)


if __name__ == '__main__':
    cli()
