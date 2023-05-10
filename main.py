from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import logging

import cv2
import easyocr


def is_number(n: str):
    return n.isnumeric()


def get_image_file_numbers(file):
    image = cv2.imread(file)
    reader = easyocr.Reader(lang_list=['pt'], gpu=True)

    text_list = reader.readtext(image, detail=0)
    numbers_list = list(filter(is_number, text_list))
    return numbers_list


class MyHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            image_data = self.rfile.read(content_length)
            body = get_image_file_numbers(image_data)
            json_string = json.dumps(body)
            self.wfile.write(json_string.encode())
            self.send_response(200)
        except Exception as e:
            logging.error("An error occurred: %s", e)


if __name__ == '__main__':
    server = HTTPServer(('localhost', 8000), MyHandler)
    print('Starting server, use <Ctrl-C> to stop')
    server.serve_forever()
