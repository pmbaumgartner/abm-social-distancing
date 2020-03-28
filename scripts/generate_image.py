from pathlib import Path

import imageio
import matplotlib.pyplot as plt
import pandas as pd

import shutil

shutil.rmtree("./animation/")
animation_dir = Path("./animation/")
animation_dir.mkdir()

agent_df = pd.read_csv("test-df.csv", index_col=0)

colormap = {"healthy": "green", "sick": "red", "recovered": "blue"}


def generate_plot_save(step):
    step_df = agent_df.query("Step == @step")
    plt.figure(figsize=(8, 4), dpi=144)

    for state in step_df["state"].unique():
        state_step_df = step_df.query("state == @state")
        plt.scatter(
            state_step_df["x"], state_step_df["y"], c=colormap[state], label=state
        )

    plt.xlim([0, 800])
    plt.ylim([0, 400])
    plt.legend(loc="upper right")
    plt.savefig(animation_dir / f"{str(step).zfill(3)}.png")
    plt.close()


for s in range(300):
    generate_plot_save(s)


image_list = Path("./animation/").glob("*.png")

with imageio.get_writer("abmv1.gif", mode="I") as writer:
    for filename in image_list:
        image = imageio.imread(filename)
        writer.append_data(image)
