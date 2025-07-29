import io

import patronus
from patronus.datasets import Dataset

patronus.init()

ds = Dataset.from_records(
    [
        {"task_input": "What is the capital of France?", "gold_answer": "Paris"},
        {"task_input": "How tall is Mount Everest?", "gold_answer": "8,849 meters"}
    ]
)


api = patronus.get_api_client()

buf = io.BytesIO()
ds.to_csv(buf, index=False)
buf.seek(0)

print("uploading...")
api.upload_dataset_from_buffer_sync(buf, "simple-2")
print("done")