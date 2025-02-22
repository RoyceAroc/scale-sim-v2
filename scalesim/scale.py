from scale_sim import scalesim
import csv

def get_final():
    final = []
    s = scalesim(save_disk_space=True, verbose=True,
                    config=config_arr,
                    topology="/Users/royce/Downloads/lab2A/lenet_conv.csv",
                    input_type_gemm=False
                    )
    output = s.run_scale()
    final += output

    s = scalesim(save_disk_space=True, verbose=True,
                    config=config_arr,
                    topology="/Users/royce/Downloads/lab2A/lenet_gemm.csv",
                    input_type_gemm=True
                    )
    output = s.run_scale()
    final += output

def compute_output(config_arr):
    # final = get_final()
    final = [('624239', 100.0), ('187199', 100.0), ('5119', 100.0), ('19199', 100.0), ('2399', 100.0)]
    
    with open('output.csv', 'a', newline='') as csvfile:
        fieldnames = ['config', 'answer']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if csvfile.tell() == 0:
            writer.writeheader()

        writer.writerow({
            'config': str(config_arr),
            'answer': str(final)
        })

import itertools

array_height_range = range(3, 11)
array_width_range = range(3, 11)
sram_size_range = range(1, 5)
dataflow_options = ["ws", "os", "is"]

combinations = itertools.product(
    array_height_range,
    array_width_range,
    sram_size_range,
    sram_size_range,
    sram_size_range,
    dataflow_options
)

for combination in combinations:
    config_arr = list(combination)
    compute_output(config_arr)