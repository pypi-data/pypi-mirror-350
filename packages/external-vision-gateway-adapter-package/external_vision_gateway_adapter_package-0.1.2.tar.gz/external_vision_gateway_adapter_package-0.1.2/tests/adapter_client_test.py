import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from datetime import datetime, timezone
from external_vision_gateway_adapter.server_client_adapter import ServerClientAdapter

def load_image(image_path):
	"""Read an image file as binary data."""
	with open(image_path, "rb") as f:
		return f.read()


def send_image(image_path):
	# Load image data
	image_data = [load_image(img_path) for img_path in image_path]

	datetime_now = datetime.now(timezone.utc)

	response = ServerClientAdapter(port=50051, timeout=2).send_request(datetime=datetime_now, image_bytes_list=image_data, tool_name='ingrind')

	print(response)


if __name__ == '__main__':

	image_path = ["test.bmp", "test2.bmp"]  # Replace with your image file path
	send_image(image_path)