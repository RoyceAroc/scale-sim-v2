from scale_sim import scalesim
import csv
import itertools
from multiprocessing import Pool, Lock
import os

def get_final(config_arr):
    """Run both GEMM and non-GEMM simulations for given config"""
    final = []
    
    # First simulation - non-GEMM
    s = scalesim(save_disk_space=True, verbose=True,
                config=config_arr,
                topology="/home/ubuntu/scale-sim-v2/scalesim/lenet_conv.csv",
                input_type_gemm=False
                )
    output = s.run_scale()
    final += output

    # Second simulation - GEMM
    s = scalesim(save_disk_space=True, verbose=True,
                config=config_arr,
                topology="/home/ubuntu/scale-sim-v2/scalesim/lenet_gemm.csv",
                input_type_gemm=True
                )
    output = s.run_scale()
    final += output
    return final

def compute_output_worker(config_arr):
    """Worker function for each process"""
    try:
        final = get_final(config_arr)
        return (config_arr, final)
    except Exception as e:
        return (config_arr, f"Error: {str(e)}")

def write_results(results, output_file='output.csv'):
    """Write results to CSV with lock to prevent concurrent writes"""
    with Lock():
        with open(output_file, 'a', newline='') as csvfile:
            fieldnames = ['config', 'answer']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Write header if file is empty
            if os.path.getsize(output_file) == 0:
                writer.writeheader()

            writer.writerow({
                'config': str(results[0]),  # config_arr
                'answer': str(results[1])   # final results
            })

def main():
    # Generate all combinations
    array_height_range = range(3, 11)
    array_width_range = range(3, 11)
    sram_size_range = range(5, 11)
    dataflow_options = ["ws", "os", "is"]

    combinations = itertools.product(
        array_height_range,
        array_width_range,
        sram_size_range,
        sram_size_range,
        [10],
        dataflow_options,
        [1]
    )
    
    # Convert to list to get length
    combinations_list = list(combinations)
    total_combinations = len(combinations_list)
    
    
    # Create output file if it doesn't exist
    if not os.path.exists('output.csv'):
        with open('output.csv', 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['config', 'answer'])
            writer.writeheader()

    # Initialize pool with 96 processes
    with Pool(processes=96) as pool:
        # Process combinations in chunks
        for i, result in enumerate(pool.imap_unordered(compute_output_worker, combinations_list)):
            write_results(result)
            
            # Print progress
            if (i + 1) % 100 == 0:
                print(f"Processed {i + 1}/{total_combinations} combinations ({((i + 1)/total_combinations)*100:.2f}%)")

if __name__ == '__main__':
    main()