# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED True
ENV APP_HOME /app
ENV PORT 8000
# Set the working directory in the container
WORKDIR $APP_HOME

# Copy the requirements file into the container at /app
COPY . ./

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# Copy the rest of the application code into the container at /app
COPY . /app/

# Define the command to run your application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "rental_site.wsgi:application"]
