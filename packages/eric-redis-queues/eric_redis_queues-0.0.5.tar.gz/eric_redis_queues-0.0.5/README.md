Redis support for eric-sse

Example of usage:

    from eric_sse.prefabs import SSEChannel
    from eric_redis_queues.eric_redis_queues import RedisQueueFactory
    
    c = SSEChannel(queues_factory=RedisQueueFactory())
