import boto3
from datetime import datetime
import pprint

##############################################
stream_name         = 'your-stream-name-here'
shard_id            = '000000000001'
shard_iterator_type = 'TRIM_HORIZON'
timestamp           = datetime(2016, 12, 15)
##############################################


client = boto3.client('kinesis')
pp = pprint.PrettyPrinter(indent=4)

def get_shard_iterator(shard_iterator):
	return client.get_records(
    	ShardIterator=shard_iterator,
    	Limit=123
)

shard_iterator = client.get_shard_iterator(
    StreamName        = stream_name,
    ShardId           = shard_id,
    ShardIteratorType = shard_iterator_type,
    Timestamp         = timestamp
)

shard_iterator = shard_iterator['ShardIterator']

flag = True
while (flag):
	new_shard_iterator = get_shard_iterator(shard_iterator)
	if len(new_shard_iterator['NextShardIterator']) > 15 and new_shard_iterator['MillisBehindLatest'] > 0:
		if len(new_shard_iterator['Records']) is 0:
			shard_iterator = get_shard_iterator(shard_iterator)['NextShardIterator']
			print pp.pprint(new_shard_iterator)
		else: 
			print "::::: RECEIVED DATA FROM THE STREAM ::::::"
			print pp.pprint(new_shard_iterator['Records'])
			flag = False
	else:
		print "::::::::::::::::::::::::::: NO MORE SHARDS TO LOOK INTO :::::::::::::::::::::::::::::::::"
		print "::::: THE NEXT SHARD ITERATOR IS %s ::::::" % str(new_shard_iterator['NextShardIterator'])
		print "::::: THE NEXT MILLIS-BEHIND-LATEST IS %s ::::::" % str(new_shard_iterator['MillisBehindLatest'])
		flag = False
