import requests
from .utils import check_internet
import base64
import os
class UrlLink:
    def __init__(self):
        if not check_internet():
            raise ConnectionError("Internet is not available. Please connect your device to the internet.")

    def shorten_url(self, long_url):
        try:
            headers = {"Content-Type": "application/json"}
            payload = {"url": long_url}

            response = requests.post("https://urllink.site/api/url.php", json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()

            if data.get("status") == "success":
                return data["short_url"]
            else:
                return f"Error shortening URL: {data}"
        except requests.RequestException as e:
            return f"Failed to shorten URL: {e}"

    def generate_qrcode(self, data, save_path=None, size=500):
        try:
            response = requests.post(
                "https://urllink.site/api/qrcode.php",
                json={"content": data, "size": size},
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            result = response.json()
            image_data = result.get("image")

            if image_data and image_data.startswith("data:image/png;base64,"):
                base64_data = image_data.split(",")[1]
                image_bytes = base64.b64decode(base64_data)

                # If no save path provided, use current directory
                if not save_path:
                    save_path = os.path.join(os.getcwd(), "qrcode.png")
                else:
                    # Ensure the directory exists
                    os.makedirs(os.path.dirname(save_path), exist_ok=True)

                with open(save_path, "wb") as f:
                    f.write(image_bytes)

                return save_path
            else:
                return "Invalid QR code data received"

        except requests.RequestException as e:
            return f"Failed to generate QR code: {e}"
