import polars as pl
from iban_validation_polars import process_ibans
import os

inputfile = r"iban_validation_rs/data/IBAN Examples.txt"
outputfile = r"iban_validation_polars/examples/test_file.csv"

# generate a csv file for testing
df = pl.read_csv(inputfile).sample(10000000, with_replacement=True)
df.write_csv(outputfile)
print("writing to file complete")

df = (
    pl.scan_csv(outputfile)
    .with_columns(
        validated=process_ibans("IBAN Examples")
        .str.split_exact(",", 2)
        .struct.rename_fields(["valid_ibans", "bank_id", "branch_id"])
    )
    .unnest("validated")
    .sort(by="IBAN Examples", descending=True)
)

# trigger the processing
print(df.collect(streaming=True))

# cleanup
os.remove(outputfile)
