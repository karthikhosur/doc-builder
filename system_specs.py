#!/usr/bin/env python3
"""
System specifications checker for optimal parallelism
"""

import psutil
import os
from multiprocessing import cpu_count
from pathlib import Path
import subprocess

def check_system_specs():
    """Check system specifications and recommend optimal settings"""
    print("🖥️  SYSTEM SPECIFICATIONS")
    print("="*50)
    
    # CPU Information
    cpu_cores = cpu_count()
    print(f"🔧 CPU Cores: {cpu_cores}")
    
    # Memory Information
    memory = psutil.virtual_memory()
    total_memory_gb = memory.total / (1024**3)
    available_memory_gb = memory.available / (1024**3)
    print(f"💾 Total Memory: {total_memory_gb:.1f} GB")
    print(f"💾 Available Memory: {available_memory_gb:.1f} GB")
    
    # Disk Space
    disk_usage = psutil.disk_usage('/')
    free_space_gb = disk_usage.free / (1024**3)
    print(f"💽 Free Disk Space: {free_space_gb:.1f} GB")
    
    # System Load
    load_avg = psutil.getloadavg()
    print(f"📊 System Load: {load_avg[0]:.2f}, {load_avg[1]:.2f}, {load_avg[2]:.2f}")
    
    print("\n" + "="*50)
    print("🚀 PERFORMANCE RECOMMENDATIONS")
    print("="*50)
    
    # Recommend parallel workers based on system specs
    if cpu_cores >= 16:
        recommended_workers = min(cpu_cores * 6, 300)
        performance_tier = "🏆 HIGH-END"
    elif cpu_cores >= 8:
        recommended_workers = min(cpu_cores * 4, 200)
        performance_tier = "🥈 MEDIUM-HIGH"
    elif cpu_cores >= 4:
        recommended_workers = min(cpu_cores * 3, 100)
        performance_tier = "🥉 MEDIUM"
    else:
        recommended_workers = min(cpu_cores * 2, 50)
        performance_tier = "⚠️  LOW-END"
    
    print(f"🖥️  System Tier: {performance_tier}")
    print(f"👥 Recommended Workers: {recommended_workers}")
    
    # Memory-based recommendations
    if total_memory_gb >= 32:
        memory_tier = "🏆 EXCELLENT"
        batch_size = 100
    elif total_memory_gb >= 16:
        memory_tier = "🥈 GOOD"
        batch_size = 50
    elif total_memory_gb >= 8:
        memory_tier = "🥉 ADEQUATE"
        batch_size = 25
    else:
        memory_tier = "⚠️  LIMITED"
        batch_size = 10
    
    print(f"💾 Memory Tier: {memory_tier}")
    print(f"📦 Recommended Batch Size: {batch_size}")
    
    # Disk space check
    estimated_size_gb = 10000 * 0.1  # Rough estimate: 100KB per document
    if free_space_gb >= estimated_size_gb * 2:
        disk_status = "✅ SUFFICIENT"
    elif free_space_gb >= estimated_size_gb:
        disk_status = "⚠️  MINIMAL"
    else:
        disk_status = "❌ INSUFFICIENT"
    
    print(f"💽 Disk Status: {disk_status}")
    print(f"📊 Estimated Space Needed: {estimated_size_gb:.1f} GB")
    
    # Performance predictions
    print("\n" + "="*50)
    print("⏱️  PERFORMANCE PREDICTIONS")
    print("="*50)
    
    # Based on system tier, estimate performance
    if performance_tier == "🏆 HIGH-END":
        estimated_docs_per_sec = 25-50
        estimated_time_min = 3.5-7
    elif performance_tier == "🥈 MEDIUM-HIGH":
        estimated_docs_per_sec = 15-25
        estimated_time_min = 7-11
    elif performance_tier == "🥉 MEDIUM":
        estimated_docs_per_sec = 8-15
        estimated_time_min = 11-20
    else:
        estimated_docs_per_sec = 3-8
        estimated_time_min = 20-55
    
    print(f"🚀 Estimated Speed: {estimated_docs_per_sec} docs/second")
    print(f"⏰ Estimated Time: {estimated_time_min} minutes for 10,000 documents")
    
    return {
        'cpu_cores': cpu_cores,
        'total_memory_gb': total_memory_gb,
        'available_memory_gb': available_memory_gb,
        'free_space_gb': free_space_gb,
        'recommended_workers': recommended_workers,
        'batch_size': batch_size,
        'performance_tier': performance_tier,
        'memory_tier': memory_tier,
        'disk_status': disk_status,
        'estimated_docs_per_sec': estimated_docs_per_sec,
        'estimated_time_min': estimated_time_min
    }

def check_current_test_progress():
    """Check progress of current running test"""
    output_dir = Path("scale_test_output")
    
    if not output_dir.exists():
        print("❌ No current test running (scale_test_output not found)")
        return None
    
    # Count generated PDFs
    pdf_count = 0
    for doc_dir in output_dir.glob("doc_*"):
        if doc_dir.is_dir():
            pdf_file = doc_dir / "data.pdf"
            if pdf_file.exists():
                pdf_count += 1
    
    progress = (pdf_count / 10000) * 100
    
    print(f"📊 Current Test Progress: {pdf_count:,}/10,000 ({progress:.1f}%)")
    
    return pdf_count

def main():
    """Main function"""
    print("🔍 SYSTEM ANALYSIS FOR OFFER LETTERS GENERATION")
    print("="*60)
    
    # Check system specs
    specs = check_system_specs()
    
    print("\n" + "="*60)
    
    # Check current test progress
    current_progress = check_current_test_progress()
    
    if current_progress is not None:
        remaining = 10000 - current_progress
        if remaining > 0:
            print(f"⏳ Remaining documents: {remaining:,}")
            
            # Estimate completion time based on current progress
            if current_progress > 0:
                # This is a rough estimate - would need more sophisticated timing
                print("💡 Consider running the ultra-fast version in parallel for faster completion")
        else:
            print("✅ Current test appears to be complete!")
    
    print("\n" + "="*60)
    print("🚀 NEXT STEPS")
    print("="*60)
    print("1. Run ultra_fast_offer_letters_test.py for maximum speed")
    print("2. Use the recommended settings above")
    print("3. Monitor progress with monitor_scale_test.py")
    print("4. Consider running multiple tests in parallel if you have the resources")

if __name__ == "__main__":
    main() 