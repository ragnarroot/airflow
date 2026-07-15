"""Shared Airflow Assets for cross-DAG, data-aware scheduling.

Every DAG that produces or consumes one of these tables must import the SAME
Asset object from here. Airflow keys assets by URI, so a shared definition keeps
producers and consumers pointing at the exact same asset.
"""

from airflow.sdk import Asset

# Produced by run_merge_verdbref once the merge AND its validation check succeed.
# Downstream DAGs schedule on this instead of a cron time, so they only run after
# a successful merge and never run on a day the merge fails or hangs.
verdbref_ready = Asset("mssql://risk/am/verdbref")
