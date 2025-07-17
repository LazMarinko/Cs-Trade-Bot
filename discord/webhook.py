import requests


class DiscordWebhook:
    def __init__(self, current_url):
        self.webhook_url = "https://discordapp.com/api/webhooks/1380885814363422922/OGm9-UDXdzEsDGG5Xlsp-iERbC5OQXgB2jGDrcoVAnCsLQgPOq2UPjbnOrvIhoZ5uRhJ"
        self.message = "Profitable trade found.\nUrl for trade:" + current_url
        self.image_path = "image.png"
        self.current_url = current_url

    def send_message(self, webhook_url, message, image_path):
        with open(image_path, "rb") as image_file:
            files = {
                'file': (image_path, image_file)
            }

            data = {
                "content": message,
                "flags": 4
            }
            response = requests.post(webhook_url, data=data, files=files)
        if response.status_code == 204:
            print("Image sent succsefully")
        else:
            print("Failed to send image")

    def run(self):
        self.send_message(self.webhook_url, self.message, self.image_path)