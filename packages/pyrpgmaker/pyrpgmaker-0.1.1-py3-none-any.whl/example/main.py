from pyrpgmaker.interface.gui import GUI
from pyrpgmaker.implementation.main import main


main(
    GUI(
        title="RPG Maker",
        default_width=1280,
        default_height=800,
        max_frames_per_second=60,
        resizable=False,
    )
)
