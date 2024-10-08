import subprocess
import os
from datetime import datetime
import config

def load_data_task():
    dest_postgres_info = config.dest_postgres_info

    output_directory = "/data/"
    current_date = datetime.now().strftime("%Y-%m-%d")
    output_directory = os.path.join(output_directory, current_date)
    
    os.makedirs(output_directory, exist_ok=True)

    meltano_load_dest_command = f"meltano elt {output_directory}/postgres_output target-postgres \
        --host {dest_postgres_info['host']} \
        --user {dest_postgres_info['user']} \
        --password {dest_postgres_info['password']} \
        --database {dest_postgres_info['database']} \
        --port {dest_postgres_info['port']} \
        --output {output_directory}/dest_postgres_output"

    try:
        subprocess.run(meltano_load_dest_command, shell=True, check=True)
        print("Data loading completed successfully!")

    except subprocess.CalledProcessError as e:
        print(f"Error executing Meltano: {e}")
        raise

if __name__ == "__main__":
    load_data_task()
