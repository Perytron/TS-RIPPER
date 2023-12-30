import clibb
import random
import time
import requests


# Example class
class Media:
    def __init__(self) -> None:
        self.url = clibb.Mutable("")
        self.split = clibb.Mutable(True)
        self.start_index = clibb.Mutable(21)
        self.end_index = clibb.Mutable(22)
        self.options = clibb.Mutable("Merge")

    def run(self) -> None:
        for i in range(self.start_index.unwrap(), self.end_index.unwrap() + 1):
            file_url = self.url.unwrap().format(number=i)
            file_name = f"chunk{i}.ts"

            # Random wait between 1 and 3 seconds
            wait_time = random.randint(1, 3)
            print(f"Waiting {wait_time} seconds...")
            time.sleep(wait_time)

            # Downloading the file
            print(f"Downloading {file_url}...")
            response = requests.get(file_url)
            if response.status_code == 200:
                with open(file_name, "wb") as file:
                    file.write(response.content)
            else:
                print(
                    f"Failed to download {file_url}. HTTP status code: {response.status_code}"
                )

        input("\nPress RETURN ... ")


media = Media()


window_1 = {
    "name": "Home",
    "width": 100,
    "colors": {
        "text": clibb.Color(255, 255, 255),
        "background": clibb.Color(254, 0, 0),
        "pass": clibb.Color(6, 215, 27),
        "fail": clibb.Color(255, 0, 0),
        "alert": clibb.Color(255, 255, 0),
    },
    "elements": [
        clibb.Title("TS-RIPPER", "by Perytron with <3"),
        clibb.Separator("empty"),
        clibb.Input("URL", media.url),
        clibb.Separator("empty"),
        clibb.Input("Start Index", media.start_index),
        clibb.Separator("empty"),
        clibb.Input("End Index", media.end_index),
        clibb.Separator("empty"),
        clibb.Configuration(
            media.options,
            "Options",
            "Merge",
            "Download only",
        ),
        clibb.Separator("empty"),
        clibb.Action("r", "Run TS-RIPPER", action=media.run, stealth=False),
        clibb.Separator("filled"),
        clibb.Separator("empty"),
    ],
}

console = clibb.Application()
console.add(window_1)
console.activate(window_1)
console.run()
