import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tdsbrondata
from pyspark.sql import functions as F
from pyspark.sql.types import *
from delta.tables import DeltaTable

def writeItemList(itemList, itemListPath):
    if DeltaTable.isDeltaTable(tdsbrondata._spark, itemListPath):
        dt = DeltaTable.forPath(tdsbrondata._spark, itemListPath)
        itemList.createOrReplaceTempView("itemListTemp")
        dt.alias("existing").delete("""
            EXISTS (
                SELECT 1 FROM itemListTemp AS new
                WHERE existing.Dienst = new.Dienst
                  AND existing.Source = new.Source
                  AND existing.FacturatieMaand = new.FacturatieMaand
            )
        """)

    itemList.write \
        .format("delta") \
        .mode("append") \
        .save(itemListPath)
