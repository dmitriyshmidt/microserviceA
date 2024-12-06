import time
import os


def send_request():
    request_file = 'request.txt'
    response_file = 'response.txt'
    timeout = 30  # seconds
    retry_interval = 2  # seconds

    # Send request
    with open(request_file, 'w') as file:
        file.write("Get Top Recipes")
    print("Request sent. Waiting for response...")

    start_time = time.time()
    while True:
        try:
            # Check if timeout has been reached
            if time.time() - start_time > timeout:
                print("Timed out waiting for response.")
                break

            if os.path.exists(response_file):
                with open(response_file, 'r') as file:
                    response = file.read().strip()
                    if response:
                        print("Top 10 Recipe Recommendations:")
                        print(response)

                        # Cleanup response.txt after successful read
                        open(response_file, 'w').close()
                        break
                    else:
                        print("Empty response received. Retrying...")
            else:
                print("Response file not found. Retrying...")
        except Exception as e:
            print(f"An error occurred: {e}")

        time.sleep(retry_interval)


if __name__ == "__main__":
    send_request()
