import os
import time
import logging

logfile_path = 'logfile.txt'
statusfile_path = 'status.txt'

# Configure logging
logging.basicConfig(filename=logfile_path, level=logging.INFO,
                    format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

last_error_content = None
shutdown_error_flag = 0

def readFile():
    global last_error_content, shutdown_error_flag
    try:
        with open(statusfile_path, 'r') as file:
            content_str = file.read().strip()
            content_int = int(content_str)
            if content_int == 1 or content_int == 0:
                return content_int
            elif content_str == last_error_content:
                return
            else:
                shutdown_error_flag = 0
                logging.error(f"Error: The content of {statusfile_path} is not the expected integer value")

    except FileNotFoundError:
        print(f"The file at {statusfile_path} does not exist.")
        logging.error(f"The file at {statusfile_path} does not exist.")

    except IOError:
        print(f"Error reading the file at {statusfile_path}: {e}")
        logging.error(f"Error reading the file at {statusfile_path}: {e}")

    except ValueError:
        print(f"Error: The content of {statusfile_path} is not a valid integer.")
        logging.error(f"Error: The content of {statusfile_path} is not a valid integer.")
        
    last_error_content = content_str 
    return


def shutdownSystem():
    global shutdown_error_flag
    if shutdown_error_flag ==0:
        logging.info(f"System shutting down")
    shutdown_status = os.system("sudo /sbin/shutdown now")
    # Check shutdown status
    if shutdown_status != 0 and shutdown_error_flag == 0:
        print("flag", shutdown_error_flag)
        logging.error("System shutdown failed")
        print("System shutdown failed")
        shutdown_error_flag = 1


def main():
    while(1):
        status = readFile()
        print(status)
        if status == 0:
            shutdownSystem()
        elif status == 1:
            shutdown_error_flag = 0
            print("System status found & expected to be running")
        time.sleep(1)


if __name__ == '__main__':
    main()