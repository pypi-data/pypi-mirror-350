"""JSON export script."""
import argparse
import json
import os
import sqlite3

from google.protobuf.json_format import MessageToDict

from dojo.external_data_providers.protobuf.dashboard.v1.data_pb2 import BlockData


def convert_db_file_to_json(db_file_path: str) -> None:
    """Run this function to convert db file to json format.

    :param db_file_path: The path of the db file
    :raises ValueError: If file path doesn't end in '.db'.
    """
    if not db_file_path.endswith(".db"):
        raise ValueError("The input file must have a .db extension")

    # Connect to the SQLite database
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()

    # read params
    cursor.execute(
        "SELECT environment, start_date, end_date, start_block, end_block, title, description FROM params"
    )
    params = cursor.fetchone()

    # read agents and data restructure
    cursor.execute("SELECT name, address FROM agents")
    agents_tuples = cursor.fetchall()

    agent_keys = ["name", "address"]

    agents = [dict(zip(agent_keys, values)) for values in agents_tuples]

    # read pools and data restructure
    cursor.execute("SELECT name, token0, token1, fee FROM pools")
    pools_tuples = cursor.fetchall()

    pool_keys = ["name", "token0", "token1", "fee"]

    pools = [dict(zip(pool_keys, values)) for values in pools_tuples]

    # read block data and data restructure
    cursor.execute("SELECT block, protobuf_serialized_data FROM blockdata")
    blockdata_tuples = cursor.fetchall()

    all_block_data = {}

    for block in blockdata_tuples:
        block_data = BlockData()
        block_data.ParseFromString(block[1])
        block_data_dict = MessageToDict(block_data)
        all_block_data[block[0]] = block_data_dict

    conn.close()

    params = {
        "environment": params[0],
        "start_date": params[1],
        "end_date": params[2],
        "start_block": params[3],
        "end_block": params[4],
        "title": params[5],
        "description": params[6],
        "agents": agents,
        "pools": pools,
    }

    json_data = {"params": params, "block_data": all_block_data}

    db_filename = os.path.basename(db_file_path)
    json_filename = os.path.splitext(db_filename)[0] + ".json"
    with open(json_filename, "w", encoding="utf-8") as json_file:
        json.dump(json_data, json_file, indent=4)

    print(f"Data successfully converted and saved to {json_filename}")


if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Convert SQLite .db file to JSON.")
    parser.add_argument(
        "--db",
        required=True,
        help="Path to the SQLite database file (must end with .db)",
    )

    # Parse the arguments
    args = parser.parse_args()

    # Convert the provided SQLite database file to JSON
    convert_db_file_to_json(args.db)

"""
ls landing_page/public/example-results/*.db | xargs -I {} \
python dojo/external_data_providers/exports/json_converter.py --db={}
"""
