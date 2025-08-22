
import os
import time
import json
import shutil
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from latex_generator import LaTeXGenerator

def generate_single_doc(doc_id):
    try:
        generator = LaTeXGenerator()
        
        # Load base data
        with open("offer-letters/data.json", 'r') as f:
            base_data = json.load(f)
        
        # Create output directory
        output_dir = Path("instant_10k_output/stream_0/doc_{doc_id:06d}".format(doc_id=doc_id))
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create unique data
        unique_data = base_data.copy()
        unique_data['document_id'] = f"OL-{doc_id:06d}"
        unique_data['employee_id'] = f"EMP-{doc_id:06d}"
        
        if 'employee_name' in unique_data:
            unique_data['employee_name'] = f"{unique_data['employee_name']} {doc_id:06d}"
        
        # Save data file
        with open(output_dir / "data.json", 'w') as f:
            json.dump(unique_data, f, indent=2)
        
        # Copy template
        shutil.copy2("offer-letters/template.tex", output_dir / "template.tex")
        
        # Copy resources if exists
        if Path("offer-letters/resources").exists():
            shutil.copytree("offer-letters/resources", output_dir / "resources", dirs_exist_ok=True)
        
        # Generate document
        pdf_path = generator.generate_document_from_folder(
            json_file=output_dir / "data.json",
            template_name="template.tex",
            output_dir=output_dir
        )
        
        return (doc_id, True, "")
    except Exception as e:
        return (doc_id, False, str(e))

# Generate documents for this stream
start_time = time.time()
doc_ids = range(1, 1429)
successful = 0
failed = 0

with ThreadPoolExecutor(max_workers=28) as executor:
    futures = {executor.submit(generate_single_doc, doc_id): doc_id for doc_id in doc_ids}
    
    for future in as_completed(futures):
        doc_id, success, error = future.result()
        if success:
            successful += 1
        else:
            failed += 1

end_time = time.time()
total_time = end_time - start_time

# Save stream results
results = {
    "stream_id": 0,
    "start_doc_id": 1,
    "end_doc_id": 1428,
    "total_docs": 1428,
    "successful": successful,
    "failed": failed,
    "total_time": total_time,
    "docs_per_second": (successful + failed) / total_time if total_time > 0 else 0
}

with open("instant_10k_output/stream_0/results.json", 'w') as f:
    json.dump(results, f, indent=2)

print(f"Stream 0 completed: {successful}/{successful + failed} documents in {total_time:.2f}s")
