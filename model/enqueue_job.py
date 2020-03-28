import redis
from rq import Queue
from job import run_model

db = redis.Redis(
    host="localhost", port=6379, db=0, decode_responses=True, health_check_interval=30
)
q = Queue(connection=db)


result = q.enqueue(
    run_model,
    kwargs=dict(N=200, width=800, height=400, p_stationary=0.75, speed=5, steps=300),
)

print(result.id)
