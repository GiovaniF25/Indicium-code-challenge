# Code Challenge
Resolution of Indicium Code challenge for Lighthouse Program - Data Engineer

More info about the challenge can be found at: https://github.com/techindicium/code-challenge

## The Challenge Synopsis
This project implements a data pipeline using the Airflow and Meltano tools to extract, transform and load (ETL) data from two distinct sources: a PostgreSQL database and a CSV file. The ultimate goal is to store this data in a second PostgreSQL database.
Create a pipeline that extracts data from two sources and writes it first to local disk and then to a database daily. using airflow for the scheduler and Meltano for the data loader
             ![image](https://github.com/GiovaniF25/Indicium-code-challenge/assets/106926901/f15ba856-84f4-42f6-81dd-6f54ae8e2b6f)


Step 1: Perform data extraction from the CSV file and the PostgreSQL database using Meltano, moving the results to my local filesystem:

```python
    import subprocess
    import os
    from datetime import datetime
    import config
    
    def extract_data_task():
        # Source PostgreSQL information
        source_postgres_info = config.source_postgres_info
        
        # CSV file path
        csv_file_path = config.csv_file_path 
    
        # Output directory for files
        output_directory = "/data/"
    
        # Create a subdirectory with the current date
        current_date = datetime.now().strftime("%Y-%m-%d")
        output_directory = os.path.join(output_directory, current_date)
    
        # Ensure the output directory exists
        os.makedirs(output_directory, exist_ok=True)
    
        # Meltano command for PostgreSQL extraction
        meltano_postgres_command = f"meltano elt tap-postgres target-csv \
            --host {source_postgres_info['host']} \
            --user {source_postgres_info['user']} \
            --password {source_postgres_info['password']} \
            --database {source_postgres_info['database']} \
            --output {output_directory}/postgres_output"
    
        # Meltano command for CSV extraction
        meltano_csv_command = f"meltano elt tap-csv target-csv \
            --file {csv_file_path} \
            --output {output_directory}/csv_output"
    
        try:
            # Execute Meltano commands
            subprocess.run(meltano_postgres_command, shell=True, check=True)
            subprocess.run(meltano_csv_command, shell=True, check=True)
    
            # Example: move files to the correct directory according to challenge guidelines
            move_command = f"mv {output_directory}/* /data/csv/{current_date}/"
            subprocess.run(move_command, shell=True, check=True)
    
            print("Data extraction completed successfully!")
    
        except subprocess.CalledProcessError as e:
            print(f"Error executing Meltano: {e}")
            raise
    
    if __name__ == "_main_":
        extract_data_task() 
```

Step 2: Loading data into a PostgreSQL database using Meltano:
```python
    import subprocess
    import os
    from datetime import datetime
    import config
    
    def load_data_task():
        # Destination PostgreSQL information
        dest_postgres_info = config.dest_postgres_info
    
        # Output directory for files
        output_directory = "/data/"
    
        # Create a subdirectory with the current date
        current_date = datetime.now().strftime("%Y-%m-%d")
        output_directory = os.path.join(output_directory, current_date)
    
        # Ensure the output directory exists
        os.makedirs(output_directory, exist_ok=True)
    
        # Meltano command to load data into the destination PostgreSQL
        meltano_load_dest_command = f"meltano elt {output_directory}/postgres_output target-postgres \
            --host {dest_postgres_info['host']} \
            --user {dest_postgres_info['user']} \
            --password {dest_postgres_info['password']} \
            --database {dest_postgres_info['database']} \
            --port {dest_postgres_info['port']} \
            --output {output_directory}/dest_postgres_output"
    
        try:
            # Load data into the destination PostgreSQL
            subprocess.run(meltano_load_dest_command, shell=True, check=True)
    
            print("Data loading completed successfully!")
    
        except subprocess.CalledProcessError as e:
            print(f"Error executing Meltano: {e}")
            raise
    
    if __name__ == "_main_":
        load_data_task()
```
Information about extraction and connection to the destination PostgreSQL database, where the extracted data will be loaded:

```python
  # PostgreSQL source (extract)
  source_postgres_info = {
      "host": "172.21.0.2",  
      "user": "northwind_user",
      "password": "thewindisblowing",
      "database": "northwind",
      "port": 5432 
  }
  
  # CSV file path (extract)
  csv_file_path = "data/order_details.csv"
  
  # PostgreSQL destiny (load)
  dest_postgres_info = {
      "host": "id-container",  
      "user": "id_indicium",
      "password": "password",
      "database": "indicium",
      "port": 5440  
  }
  
  ```

## **DAG**
Repository containing an Airflow DAG designed to orchestrate a data pipeline using Meltano for data extraction and loading tasks. The pipeline extracts this data and writes it to local disk and then loads it to a database daily.

```python
    from datetime import datetime, timedelta
    from airflow import DAG
    from airflow.operators.python_operator import PythonOperator
    from pathlib import Path
    
    # Defining default DAG parameters
    default_args = {
        'owner': 'GIOVANI M FERRARI',
        'depends_on_past': False,
        'start_date': datetime(2024, 2, 25),
        'retries': 1,
        'retry_delay': timedelta(minutes=5),
    }
    
    # Creating the DAG object
    dag = DAG(
        'indicium_data_pipeline',
        default_args=default_args,
        schedule_interval=timedelta(days=1),  # Run daily
    )
    
    # Function encapsulating the data extraction logic
    def extract_data(**kwargs):
        from extract_data import extract_data_task
        extract_data_task()
    
    # Function encapsulating the data loading logic
    def load_data(**kwargs):
        from load_data import load_data_task
        load_data_task()
    
    # Creating PythonOperator tasks to execute the extraction and loading functions
    extract_task = PythonOperator(
        task_id='extract_data',
        python_callable=extract_data,
        provide_context=True,
        dag=dag,
    )
    
    load_task = PythonOperator(
        task_id='load_data',
        python_callable=load_data,
        provide_context=True,
        dag=dag,
    )
    
    # Defining the execution order of tasks
    extract_task >> load_task

```

## **Setup of the Solution**
  I used Docker to containerize my solution. The source code can be set up using docker compose.
  
  You can install following the instructions at https://docs.docker.com/compose/install/ With docker compose installed simply run:

docker-compose up -d

        
## **Testing the Pipeline**

After you set up my code, it is possible to test each task or the whole pipeline in the past. Access the Airflow container:

docker exec -it airflow-container bash

        
## **To run the pipeline at docker-desktop**

airflow run indicium_data_pipeline extract_data '{currente_date}'

airflow run indicium_data_pipeline load_data '{currente_date}'

  ![image](https://github.com/GiovaniF25/Indicium-code-challenge/assets/106926901/3adf4548-9f5d-4318-a0f9-3f706b24b76a)

  
        
## **Monitor and Troubleshoot**

Airflow provides a web service to monitor and troubleshoot in pipelines. To start the web server:

airflow webserver -p 8080

And Access by address 

http://0.0.0.0:8080.

It is possible to verify if the pipeline failed there.

Thanks for reading!


    Written with Online Markdown 
    https://dillinger.io/


