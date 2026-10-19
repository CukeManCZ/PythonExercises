import tkinter as tk
from enum import Enum
from pathlib import Path
import time

class PlantState(Enum):
    NONE = 1
    PLANTED = 2
    GROWING_1 = 3
    GROWING_2 = 4
    GROWING_3 = 5
    FINISHED = 6


GROWINGTIME = 5.0
UPDATE_INTERVAL = 100
NUMBER_OF_PLOTS = 10


# ============================================================
# GAME LOGIC - LIST EXERCISES
# ============================================================

def update_list(farmlands : list[PlantState], planted_at : list[float]) -> bool:
    """
    Update the growth of every plant in the farm.

    For each plot:
    - Skip empty plots and finished plants.
    - Calculate growth progress using planted_at and GROWINGTIME.
    - Update the plant's state according to its growth progress.

    Both lists use the same index for each plot.

    Return True if any plant changes state, otherwise False.
    """

    pass


def on_farm_click(index : int, farmlands : list[PlantState], planted_at :  list[float | None]) -> bool:
    """
    Handle a click on the plot at the given index.

    - If the plot is empty, plant a seed and record the current time.
    - If the plant is finished, harvest it and reset the plot.
    - Otherwise, leave the plot unchanged.

    Return True if a plant was harvested, otherwise False.
    """

    pass


# ============================================================
# TKINTER VIEW
# ============================================================

class FarmView:
    def __init__(
        self,
        root,
        farmlands,
        planted_at,
        update_function,
        click_function,
    ):
        self.root = root
        self.farmlands = farmlands
        self.planted_at = planted_at
        self.update_function = update_function
        self.click_function = click_function
        self.harvested = 0

        images_dir = Path("images")

        self.images = {
            PlantState.NONE: tk.PhotoImage(
                file=images_dir / "none.png"
            ),
            PlantState.PLANTED: tk.PhotoImage(
                file=images_dir / "seed.png"
            ),
            PlantState.GROWING_1: tk.PhotoImage(
                file=images_dir / "growing1.png"
            ),
            PlantState.GROWING_2: tk.PhotoImage(
                file=images_dir / "growing2.png"
            ),
            PlantState.GROWING_3: tk.PhotoImage(
                file=images_dir / "growing3.png"
            ),
            PlantState.FINISHED: tk.PhotoImage(
                file=images_dir / "finished.png"
            ),
        }

        self.tile_width = self.images[PlantState.NONE].width()
        self.tile_height = self.images[PlantState.NONE].height()

        self.frame = tk.Frame(root)
        self.frame.pack(fill="both", expand=True)

        self.farm_frame = tk.Frame(self.frame)
        self.farm_frame.pack(anchor="nw")

        self.tiles = []
        self.draw()

        self.score_label = tk.Label(
            self.frame,
            text="Harvested: 0",
            font=("Arial", 14),
        )
        self.score_label.pack(anchor="se", padx=10, pady=10)

        self.update_game()

    def draw(self):
        for index in range(len(self.farmlands)):
            tile = tk.Canvas(
                self.farm_frame,
                width=self.tile_width,
                height=self.tile_height,
                highlightthickness=0,
                cursor="hand2",
            )
            tile.grid(row=0, column=index)

            tile.create_image(
                0, 0,
                image=self.images[PlantState.NONE],
                anchor="nw",
            )

            tile.bind(
                "<Button-1>",
                lambda event, i=index: self.handle_click(i),
            )

            self.tiles.append(tile)

        self.refresh()

    def handle_click(self, index):
        harvested = self.click_function(
            index,
            self.farmlands,
            self.planted_at,
        )

        if harvested:
            self.harvested += 1
            self.score_label.config(
                text=f"Harvested: {self.harvested}"
            )

        self.refresh()

    def update_game(self):
        changed = self.update_function(
            self.farmlands,
            self.planted_at,
        )

        if changed:
            self.refresh()

        self.root.after(UPDATE_INTERVAL, self.update_game)

    def refresh(self):
        for index in range(len(self.farmlands)):
            tile = self.tiles[index]
            tile.delete("plant")

            state = self.farmlands[index]

            if state != PlantState.NONE:
                tile.create_image(
                    0, 0,
                    image=self.images[state],
                    anchor="nw",
                    tags="plant",
                )


# ============================================================
# MAIN PROGRAM
# ============================================================

def main():
    # Each index represents one plot in the farm.
    farmlands = [PlantState.NONE] * NUMBER_OF_PLOTS
    planted_at = [None] * NUMBER_OF_PLOTS

    root = tk.Tk()
    root.title("Farm Game")

    FarmView(
        root,
        farmlands,
        planted_at,
        update_function=update_list,
        click_function=on_farm_click,
    )

    root.mainloop()


if __name__ == "__main__":
    main()