# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {}
# META }

# MARKDOWN ********************

# ## Install EventHub Python Dependency

# CELL ********************

%pip install azure-eventhub

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## Helper functions that facilitate sending data to the EventStream

# CELL ********************

import json, random, time
from datetime import datetime, timezone
from azure.eventhub import EventHubProducerClient, EventData

# Paste from Eventstream -> Custom endpoint -> Event Hub -> Connection string
CONNECTION_STR = "Endpoint=sb://...."

producer = EventHubProducerClient.from_connection_string(conn_str=CONNECTION_STR)

from datetime import datetime, timezone
import uuid

def base_event(truck_id):
    return {
        "event_id": str(uuid.uuid4()),               #
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "source": "telematics-unit",
        "truck_id": truck_id,
        "trip_id": "<paste a trip id to simulate>",
        "driver_id": "<paste a driver id UUID to simulate>",
        "spn": 1,
        "fmi": 1,
        "severity": "Critical",
        "occurrenc_count": 2,
        "latitude": 39.2005,
        "longitude": -94.2942
    }

def inject_engine_fault(e, fault_description, action):
    e["fault_description"] = fault_description
    e["action"] = action
    return e

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## Send a stream of simulated engine overheated event to the Event Stream

# CELL ********************

import time
import random
import json
from datetime import datetime, timezone
from azure.eventhub import EventData

FAULTS = [
    "Engine Overheated",
    "Tire Pressure Low",
    "High Oil Temp",
    "Poor Fuel Economy",
    "Oxygen Sensor",
    "Load Limit Exceeded",
]

ACTIONS = [
    "Divert fro Service",
    "Schedule Maintenance",
    "Call Driver"
]

producer.__enter__()
try:
    truck_id = "<paste a truck id to simulate>"

    # Run for 5 minutes (300 seconds)
    end_time = time.time() + 300

    while time.time() < end_time:
        # Pick a random fault each iteration
        fault_description = random.choice(FAULTS)
        action = random.choice(ACTIONS)

        evt = inject_engine_fault(
            base_event(truck_id),
            fault_description=fault_description,
            action = action
        )

        producer.send_batch([EventData(json.dumps(evt))])

        # Nice UTC timestamp for logging
        now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        print(f"[{now}] Injected fault '{fault_description}': {evt}")

        # Sleep random interval between 4 and 15 seconds
        time.sleep(random.uniform(4, 15))

finally:
    producer.__exit__(None, None, None)
    

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
