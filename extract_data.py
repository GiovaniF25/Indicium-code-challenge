import subprocess
import os
from datetime import datetime
import config

def extract_data_task():
    source_postgres_info = config.source_postgres_info
    csv_file_path = config.csv_file_path 
    output_directory = "/data/"
    current_date = datetime.now().strftime("%Y-%m-%d")
    output_directory = os.path.join(output_directory, current_date)
    os.makedirs(output_directory, exist_ok=True)

    meltano_postgres_command = f"meltano elt tap-postgres target-csv \
        --host {source_postgres_info['host']} \
        --user {source_postgres_info['user']} \
        --password {source_postgres_info['password']} \
        --database {source_postgres_info['database']} \
        --output {output_directory}/postgres_output"

    meltano_csv_command = f"meltano elt tap-csv target-csv \
        --file {csv_file_path} \
        --output {output_directory}/csv_output"

    try:
        subprocess.run(meltano_postgres_command, shell=True, check=True)
        subprocess.run(meltano_csv_command, shell=True, check=True)
        move_command = f"mv {output_directory}/* /data/csv/{current_date}/"
        subprocess.run(move_command, shell=True, check=True)
        print("Data extraction completed successfully!")

    except subprocess.CalledProcessError as e:
        print(f"Error executing Meltano: {e}")
        raise

if __name__ == "__main__":
    extract_data_task()
