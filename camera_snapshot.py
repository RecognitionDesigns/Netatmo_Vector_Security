
#!/usr/bin/python3

import sys
from sys import exit
import lnetatmo
import os
import sys
import time
import anki_vector
from anki_vector.util import degrees

MY_CAMERA = "Driveway"

authorization = lnetatmo.ClientAuth()

homeData = lnetatmo.HomeData(authorization)

snapshot = homeData.getLiveSnapshot( camera=MY_CAMERA )

try:
    from PIL import Image
except ImportError:
    sys.exit("Cannot import from PIL: Do `pip3 install --user Pillow` to install")

def main():
    args = anki_vector.util.parse_command_args()

    with anki_vector.Robot(args.serial) as robot:
        robot.behavior.set_head_angle(degrees(45.0))
        robot.behavior.set_lift_height(0.0)
        robot.behavior.say_text("Alert! Motion Detected Outside!")

        current_directory = os.path.dirname(os.path.realpath(__file__))

        for _ in range(60):
            snapshot = homeData.getLiveSnapshot( camera=MY_CAMERA )
            if not snapshot :
                exit(1)
            #You may ave to create a folder called images in the directory the script is saved in.
            with open("images/driveway_snapshot.jpg", "wb") as f: f.write(snapshot)

            image = Image.open('images/driveway_snapshot.jpg')
            new_image = image.resize((184, 96))
            new_image.save('images/driveway_snapshot_vector.jpg')


            image_path = os.path.join(current_directory, "images", "driveway_snapshot_vector.jpg")

            image_file = Image.open(image_path)

            print("Display image on Vector's face...")
            screen_data = anki_vector.screen.convert_image_to_screen_data(image_file)
            robot.screen.set_screen_with_image_data(screen_data, 20.0)
            
            #this is the time between each snapshot
            time.sleep(0.6)

if __name__ == "__main__":
    main()
