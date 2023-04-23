FROM apache/airflow:2.5.1

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container at /app
COPY . .

# Set environment variables
ENV AIRFLOW_HOME=/app
ENV AIRFLOW__CORE__EXECUTOR=SequentialExecutor

# Expose the webserver and scheduler ports
EXPOSE 8080 8793

# Start the Airflow webserver and scheduler
CMD ["bash", "-c", "airflow db init && airflow webserver --port 8080 & airflow scheduler"]