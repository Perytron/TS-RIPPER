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
        self.language_audio = clibb.Mutable(None)
        self.language_subtitles = clibb.Mutable(None)
        self.start_index = clibb.Mutable(None)
        self.end_index = clibb.Mutable(None)

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
        if not any(
            [
                self.url_video.unwrap(),
                self.url_audio.unwrap(),
                self.url_subtitles.unwrap(),
            ]
        ):
            print("At least one URL must be provided!")
            input("\nPress RETURN to exit... ")
            return

        counter = (
            int(self.start_index.unwrap())
            if self.start_index.unwrap() is not None
            else 1
        )

        output_dir = (
            f"ts-ripper-output-{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"
        )
        os.makedirs(output_dir, exist_ok=True)

        while True:
            wait_time = random.uniform(2, 4)
            time.sleep(wait_time)
            try:
                self.process_media(counter, output_dir)
            except Exception as e:
                print(f"Error: {e}")
                break

            counter += 1
            if self.end_index.unwrap() is not None and counter > int(
                self.end_index.unwrap()
            ):
                break

        input("\nPress RETURN to exit... ")

    def process_media(self, counter: int, output_dir: str):
        for media_type in ["video", "audio", "subtitles"]:
            url = getattr(self, f"url_{media_type}").unwrap()
            if url:
                file_name = self.generate_file_name(media_type, counter)
                self.download_chunk(
                    url.format(number=counter), os.path.join(output_dir, file_name)
                )
                print(
                    f"{datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')}: Chunk {counter} ({media_type}) successfully downloaded ..."
                )

    def generate_file_name(self, media_type, counter):
        if media_type == "audio" and self.language_audio.unwrap():
            return f"{media_type}_{self.language_audio.unwrap()}_{counter}.ts"
        elif media_type == "subtitles" and self.language_subtitles.unwrap():
            return f"{media_type}_{self.language_subtitles.unwrap()}_{counter}.vtt"
        return (
            f"{media_type}_{counter}.ts"
            if media_type != "subtitles"
            else f"{media_type}_{counter}.vtt"
        )


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
        clibb.Input("URL Video", media.url_video),
        clibb.Separator("empty"),
        clibb.Input("URL Audio", media.url_audio),
        clibb.Separator("empty"),
        clibb.Input("URL Subtitles", media.url_subtitles),
        clibb.Separator("filled"),
        clibb.Separator("empty"),
        clibb.Input("Audio Language", media.language_audio),
        clibb.Separator("empty"),
        clibb.Input("Subtitle Language", media.language_subtitles),
        clibb.Separator("filled"),
        clibb.Separator("empty"),
        clibb.Input("Start Index", media.start_index),
        clibb.Separator("empty"),
        clibb.Input("End Index", media.end_index),
        clibb.Separator("filled"),
        clibb.Separator("empty"),
        clibb.Action("r", "Run TS-RIPPER", action=media.run, stealth=False),
        clibb.Separator("empty"),
    ],
}

console = clibb.Application()
console.add(window_1)
console.activate(window_1)
console.run()
