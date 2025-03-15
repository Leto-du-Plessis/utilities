import torch # Note torch must be installed with CUDA support
import time

# Main loop
device = "cuda" 
num_megabytes = 512.0                        # Set to appropriate number of megabytes
vram_size = 1024 * 1024 * num_megabytes 
pause = 0.1                                  # Set to appropriate pause time
iterations = 100                             # Set to appropriate number of iterations 

for i in range(iterations):
    try:

        # Readout to the user
        print(f"Iteration {i+1}: Allocating {num_megabytes} MB")

        # Allocate a tensor on the vram
        arr = torch.zeros(vram_size // 4, dtype=torch.float32, device=device)
        time.sleep(pause)

        # Free the tensor and clear the cache
        del arr  
        torch.cuda.empty_cache() 
        time.sleep(pause)

    except Exception as e:

        print(f"Error: {e}")
        break

print("Done")