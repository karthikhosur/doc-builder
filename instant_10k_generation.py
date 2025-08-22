#!/usr/bin/env python3
"""
Instant 10,000 offer letters generation using multiple parallel streams
"""

import os
import time
import json
import shutil
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
from multiprocessing import cpu_count
import subprocess
import threading
import psutil
from datetime import datetime

class Instant10KGenerator:
    """Generate 10,000 offer letters using multiple parallel streams"""
    
    def __init__(self):
        self.total_documents = 10000
        self.base_json_file = Path("offer-letters/data.json")
        self.output_dir = Path("instant_10k_output")
        self.cpu_cores = cpu_count()
        
        # Create output directory
        self.output_dir.mkdir(exist_ok=True)
        
        # Calculate optimal configuration
        self.num_streams = min(self.cpu_cores // 2, 8)  # Number of parallel streams
        self.docs_per_stream = self.total_documents // self.num_streams
        self.workers_per_stream = self.cpu_cores * 2  # Workers per stream
        
        print(f"⚡ INSTANT 10K GENERATION CONFIGURATION")
        print(f"🖥️  CPU Cores: {self.cpu_cores}")
        print(f"🔄 Parallel Streams: {self.num_streams}")
        print(f"📊 Documents per Stream: {self.docs_per_stream}")
        print(f"👥 Workers per Stream: {self.workers_per_stream}")
        print(f"🚀 Total Parallel Workers: {self.num_streams * self.workers_per_stream}")
    
    def generate_stream(self, stream_id: int, start_doc_id: int, end_doc_id: int) -> dict:
        """Generate documents for a single stream"""
        import subprocess
        import json
        from datetime import datetime
        
        stream_start_time = time.time()
        
        # Create stream-specific output directory
        stream_output_dir = self.output_dir / f"stream_{stream_id}"
        stream_output_dir.mkdir(exist_ok=True)
        
        # Create a temporary script for this stream
        script_content = f'''
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
        output_dir = Path("instant_10k_output/stream_{stream_id}/doc_{{doc_id:06d}}".format(doc_id=doc_id))
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create unique data
        unique_data = base_data.copy()
        unique_data['document_id'] = f"OL-{{doc_id:06d}}"
        unique_data['employee_id'] = f"EMP-{{doc_id:06d}}"
        
        if 'employee_name' in unique_data:
            unique_data['employee_name'] = f"{{unique_data['employee_name']}} {{doc_id:06d}}"
        
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
doc_ids = range({start_doc_id}, {end_doc_id + 1})
successful = 0
failed = 0

with ThreadPoolExecutor(max_workers={self.workers_per_stream}) as executor:
    futures = {{executor.submit(generate_single_doc, doc_id): doc_id for doc_id in doc_ids}}
    
    for future in as_completed(futures):
        doc_id, success, error = future.result()
        if success:
            successful += 1
        else:
            failed += 1

end_time = time.time()
total_time = end_time - start_time

# Save stream results
results = {{
    "stream_id": {stream_id},
    "start_doc_id": {start_doc_id},
    "end_doc_id": {end_doc_id},
    "total_docs": {end_doc_id - start_doc_id + 1},
    "successful": successful,
    "failed": failed,
    "total_time": total_time,
    "docs_per_second": (successful + failed) / total_time if total_time > 0 else 0
}}

with open("instant_10k_output/stream_{stream_id}/results.json", 'w') as f:
    json.dump(results, f, indent=2)

print(f"Stream {stream_id} completed: {{successful}}/{{successful + failed}} documents in {{total_time:.2f}}s")
'''
        
        # Write temporary script
        script_file = stream_output_dir / f"stream_{stream_id}_script.py"
        with open(script_file, 'w') as f:
            f.write(script_content)
        
        # Execute the script
        try:
            result = subprocess.run([
                'python', str(script_file)
            ], capture_output=True, text=True, cwd=os.getcwd())
            
            # Load results
            results_file = stream_output_dir / "results.json"
            if results_file.exists():
                with open(results_file, 'r') as f:
                    stream_results = json.load(f)
                return stream_results
            else:
                return {
                    "stream_id": stream_id,
                    "error": "No results file generated",
                    "stdout": result.stdout,
                    "stderr": result.stderr
                }
        except Exception as e:
            return {
                "stream_id": stream_id,
                "error": str(e)
            }
    
    def run_instant_generation(self):
        """Run the instant generation using multiple parallel streams"""
        print(f"\n🚀 STARTING INSTANT 10K GENERATION")
        print(f"⏰ Start time: {datetime.now().strftime('%H:%M:%S')}")
        print("="*80)
        
        # Record initial system state
        initial_memory = psutil.virtual_memory().used / 1024 / 1024  # MB
        start_time = time.time()
        
        # Create stream ranges
        streams = []
        for i in range(self.num_streams):
            start_doc = i * self.docs_per_stream + 1
            end_doc = min((i + 1) * self.docs_per_stream, self.total_documents)
            streams.append((i, start_doc, end_doc))
        
        print(f"📊 Stream Configuration:")
        for i, start_doc, end_doc in streams:
            print(f"   Stream {i}: Documents {start_doc:,} - {end_doc:,} ({end_doc - start_doc + 1:,} docs)")
        
        # Launch all streams in parallel
        print(f"\n🔥 LAUNCHING {self.num_streams} PARALLEL STREAMS...")
        
        with ProcessPoolExecutor(max_workers=self.num_streams) as executor:
            future_to_stream = {
                executor.submit(self.generate_stream, stream_id, start_doc, end_doc): stream_id
                for stream_id, start_doc, end_doc in streams
            }
            
            # Wait for all streams to complete
            stream_results = []
            for future in as_completed(future_to_stream):
                stream_result = future.result()
                stream_results.append(stream_result)
                
                if 'error' not in stream_result:
                    print(f"✅ Stream {stream_result['stream_id']} completed: "
                          f"{stream_result['successful']} docs in {stream_result['total_time']:.2f}s "
                          f"({stream_result['docs_per_second']:.2f} docs/sec)")
                else:
                    print(f"❌ Stream {stream_result['stream_id']} failed: {stream_result['error']}")
        
        end_time = time.time()
        total_time = end_time - start_time
        final_memory = psutil.virtual_memory().used / 1024 / 1024  # MB
        
        # Calculate overall statistics
        total_successful = sum(r.get('successful', 0) for r in stream_results if 'error' not in r)
        total_failed = sum(r.get('failed', 0) for r in stream_results if 'error' not in r)
        total_processed = total_successful + total_failed
        
        overall_docs_per_second = total_processed / total_time if total_time > 0 else 0
        memory_used = final_memory - initial_memory
        
        # Print final results
        print("\n" + "="*80)
        print("🎯 INSTANT 10K GENERATION RESULTS")
        print("="*80)
        print(f"⏰ Total Time: {total_time:.2f} seconds ({total_time/60:.2f} minutes)")
        print(f"📊 Total Documents: {total_processed:,}")
        print(f"✅ Successful: {total_successful:,}")
        print(f"❌ Failed: {total_failed:,}")
        print(f"📈 Success Rate: {(total_successful/total_processed)*100:.1f}%")
        print(f"🚀 Overall Speed: {overall_docs_per_second:.2f} docs/second")
        print(f"💾 Memory Used: {memory_used:.1f} MB")
        print(f"🔄 Parallel Streams: {self.num_streams}")
        print(f"👥 Total Workers: {self.num_streams * self.workers_per_stream}")
        
        # Performance rating
        if total_time < 60:
            print(f"⚡ ACHIEVEMENT UNLOCKED: LIGHTNING SPEED (<1 minute)")
        elif total_time < 180:
            print(f"🚀 ACHIEVEMENT UNLOCKED: ROCKET SPEED (<3 minutes)")
        elif total_time < 300:
            print(f"✅ ACHIEVEMENT UNLOCKED: FAST SPEED (<5 minutes)")
        
        if overall_docs_per_second > 100:
            print(f"🏆 ACHIEVEMENT UNLOCKED: SPEED DEMON (>100 docs/sec)")
        elif overall_docs_per_second > 50:
            print(f"🥇 ACHIEVEMENT UNLOCKED: SPEED MASTER (>50 docs/sec)")
        elif overall_docs_per_second > 25:
            print(f"🥈 ACHIEVEMENT UNLOCKED: SPEED EXPERT (>25 docs/sec)")
        
        print(f"\n📁 All files saved to: {self.output_dir}")
        
        # Save overall results
        overall_results = {
            "total_time": total_time,
            "total_documents": total_processed,
            "successful": total_successful,
            "failed": total_failed,
            "success_rate": (total_successful/total_processed)*100,
            "docs_per_second": overall_docs_per_second,
            "memory_used_mb": memory_used,
            "num_streams": self.num_streams,
            "total_workers": self.num_streams * self.workers_per_stream,
            "stream_results": stream_results,
            "timestamp": datetime.now().isoformat()
        }
        
        with open(self.output_dir / "overall_results.json", 'w') as f:
            json.dump(overall_results, f, indent=2)
        
        return overall_results

def main():
    """Main function"""
    print("⚡ INSTANT 10,000 OFFER LETTERS GENERATION")
    print("="*60)
    
    generator = Instant10KGenerator()
    
    try:
        results = generator.run_instant_generation()
        
        print(f"\n🎉 GENERATION COMPLETE!")
        print(f"📊 Final Stats: {results['successful']:,} successful, {results['failed']:,} failed")
        print(f"⚡ Speed: {results['docs_per_second']:.2f} docs/second")
        
    except KeyboardInterrupt:
        print("\n⚠️  Generation interrupted by user")
    except Exception as e:
        print(f"\n❌ Generation failed: {e}")
        raise

if __name__ == "__main__":
    main() 