import pandas as pd
import plotly.graph_objects as go
import redis

db = redis.Redis(
    host="localhost", port=6379, db=0, decode_responses=True, health_check_interval=30
)

key = "num_agents=200,width=800,height=400,p_stationary=0.75,speed=5"

dtype = {
    "unique_id": int,
    "step": int,
    "state": "category",
    "x": float,
    "y": float,
    "social_distancing": bool,
    "recovery_time": int,
}

df = pd.DataFrame((i[1] for i in db.xrange(key))).astype(dtype)

state_by_step = (
    df.groupby(["step", "state"]).size().reset_index().rename(columns={0: "count"})
)

healthy_counts = state_by_step.query("state == 'healthy'").loc[:, "count"].tolist()
infected_counts = state_by_step.query("state == 'infected'").loc[:, "count"].tolist()
recovered_counts = state_by_step.query("state == 'recovered'").loc[:, "count"].tolist()


x = list(sorted(df["step"].unique()))
fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=x,
        y=infected_counts,
        mode="lines",
        line=dict(width=0.5, color="#bb641e"),
        stackgroup="one",
        groupnorm="percent",
        name="infected",
    )
)
fig.add_trace(
    go.Scatter(
        x=x,
        y=healthy_counts,
        mode="lines",
        line=dict(width=0.5, color="#a9c6ca"),
        stackgroup="one",
        name="healthy",
    )
)
fig.add_trace(
    go.Scatter(
        x=x,
        y=recovered_counts,
        mode="lines",
        line=dict(width=0.5, color="#cc8ac0"),
        stackgroup="one",
        name="recovered",
    )
)

fig.write_html("test-redis-fig.html")
