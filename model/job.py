from social_distancing import SocialDistanceModel
import redis


db = redis.Redis(
    host="localhost", port=6379, db=0, decode_responses=True, health_check_interval=30
)


def run_model(
    N=200, width=800, height=400, p_stationary=0.75, speed=5, steps: int = 300
):
    model = SocialDistanceModel(
        db=db, N=N, width=width, height=height, p_stationary=p_stationary, speed=speed,
    )
    for _ in range(steps):
        model.step()
