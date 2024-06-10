## **Prerequisites:**  
Install 'Docker' in your local PC or have an account in Docker Cloud.
## Commands:
>> Run the following commands from the directory where you loaded the above image (here, exmaple for Windows CMD prompt is shown):\
  *docker load -i genevic-v1.tar*\
  This command loads the Docker image from the tar file into your local Docker repository. \
  *docker run -p 8501:8501 streamlit-app*\
  This command runs the container, mapping port 8501 on your local machine to port 8501 in the container.
