import time


def send_request():
    with open('request.txt', 'w') as file:
        file.write("Get Top Recipes")
    print("Request sent. Waiting for response...")

    while True:
        try:
            with open('response.txt', 'r') as file:
                response = file.read().strip()
                if response:
                    print("Top 10 Recipe Recommendations:")
                    print(response)
                    break
        except FileNotFoundError:
            print("Response file not found. Retrying...")

        time.sleep(2)


if __name__ == "__main__":
    send_request()
