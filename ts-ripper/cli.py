import clibb
import random
import time
import requests
import os
import datetime


class Media:
    def __init__(self):
        self.url_video = clibb.Mutable(None)
        self.url_audio = clibb.Mutable(None)
        self.url_subtitles = clibb.Mutable(None)
        self.start_index = clibb.Mutable(None)
        self.end_index = clibb.Mutable(None)
        self.output_dir = (
            f"ts-ripper-output_{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"
        )

    def download_chunk(self, url: str, name: str):
        try:
            response = requests.get(url)
            response.raise_for_status()
            with open(name, "wb") as file:
                file.write(response.content)
        except requests.HTTPError as e:
            raise Exception(
                f"Failed to download {url}. HTTP status code: {e.response.status_code}"
            )

    def run(self):
        if not self.url_video.unwrap():
            print("'URL Video' must be provided!")
            input("\nPress RETURN to exit... ")
            return

        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        counter = self.start_index.unwrap() or 1

        while True:
            wait_time = random.uniform(2, 4)
            time.sleep(wait_time)
            try:
                video_url = self.url_video.unwrap().format(number=counter)
                self.download_chunk(
                    video_url, os.path.join(self.output_dir, f"video_{counter}.ts")
                )
                if self.url_audio.unwrap():
                    audio_url = self.url_audio.unwrap().format(number=counter)
                    self.download_chunk(
                        audio_url, os.path.join(self.output_dir, f"audio_{counter}.ts")
                    )
                if self.url_subtitles.unwrap():
                    subtitles_url = self.url_subtitles.unwrap().format(number=counter)
                    self.download_chunk(
                        subtitles_url,
                        os.path.join(self.output_dir, f"subtitle_{counter}.vtt"),
                    )
            except Exception as e:
                print(f"Error: {e}")
                break

            print(
                f"{datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')}: Successfully downloaded chunk {counter} after waiting {wait_time:.2f} seconds ..."
            )

            if counter == self.end_index.unwrap():
                break
            counter += 1

        input("\nPress RETURN to exit... ")


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
        clibb.Display(
            "Info", "Leave 'URL Audio' empty if video and audio are not split."
        ),
        clibb.Display(
            "",
            "Leave 'URL Subtitles' empty if you don't need subtitles.",
        ),
        clibb.Display(
            "",
            "Leave indexes empty to download everything.",
        ),
        clibb.Separator("filled"),
        clibb.Separator("empty"),
        clibb.Input("URL Video", media.url_video),
        clibb.Separator("empty"),
        clibb.Input("URL Audio", media.url_audio),
        clibb.Separator("empty"),
        clibb.Input("URL Subtitles", media.url_subtitles),
        clibb.Separator("empty"),
        clibb.Input("Start Index", media.start_index),
        clibb.Separator("empty"),
        clibb.Input("End Index", media.end_index),
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
