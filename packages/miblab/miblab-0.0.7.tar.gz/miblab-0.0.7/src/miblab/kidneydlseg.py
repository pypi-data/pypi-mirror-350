import os
import tempfile
import numpy as np
from data import zenodo_fetch
import scipy.ndimage as ndi

try:
    from monai.networks.nets.unetr import UNETR
    from monai.inferers import sliding_window_inference
    monai_installed = True

except ImportError:
    monai_installed = False

try:
    import torch
    torch_installed = True
except ImportError:
    torch_installed = False

MODEL = 'UNETR_kidneys_v2.pth'
MODEL_DOI = "14237436"

def kidney_pc_dixon(input_array,overlap=0.3, postproc=True):
    
    """
    Run MONAI UNETR from within Python.

    Args:
        input_image (numpy.ndarray): A 4D NumPy array of shape [contrast, x, y, z] 
                                     representing the input medical image volume.

    Returns:
        dict: A dictionary with the keys 'leftkidney' and 'rightkidney', 
              each containing a NumPy array representing the respective kidney mask.

    If post-processing is enabled, only the largest connected component of each kidney 
    (left/right) is extracted from the UNETR output.
    """
    if not torch_installed:
        raise ImportError(
            'vreg is not installed. Please install it with "pip install vreg".'
            'To install all dlseg options at once, install miblab as pip install miblab[dlseg].'
        )
    if not monai_installed:
        raise ImportError(
            'totalsegmentator is not installed. Please install it with "pip install totalsegmentator".'
            'To install all dlseg options at once, install miblab as pip install miblab[dlseg].'
        )


    with tempfile.TemporaryDirectory() as temp_dir:
        print("Downloading " + MODEL + " to temporary directory:", temp_dir)
        zenodo_fetch(MODEL, temp_dir, MODEL_DOI)
        print(MODEL + " was successfully downloaded to temporary directory:", temp_dir)

        weights_path = os.path.join(temp_dir,'UNETR_kidneys_v2.pth')

        # Setup device
        os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
        device_str = "cuda" if torch.cuda.is_available() else "cpu"
        device = torch.device(device_str)

        # Define model architecture
        model = UNETR(
            in_channels=4,
            out_channels=3, # BACKGROUND, RIGHT KIDNEY (left on image), LEFT KIDNEY (right on image)
            img_size=(80, 80, 80),
            feature_size=16,
            hidden_size=768,
            mlp_dim=3072,
            num_heads=12,
            proj_type="perceptron",
            norm_name="instance",
            res_block=True,
            dropout_rate=0.0,
        ).to(device)

        # Normalize data
        input_array_out   = (input_array[0,...]-np.average(input_array[0,...]))/np.std(input_array[0,...])
        input_array_in    = (input_array[1,...]-np.average(input_array[1,...]))/np.std(input_array[1,...])
        input_array_water = (input_array[2,...]-np.average(input_array[2,...]))/np.std(input_array[2,...])
        input_array_fat   = (input_array[3,...]-np.average(input_array[3,...]))/np.std(input_array[3,...])

        input_array = np.stack((input_array_out, input_array_in, input_array_water, input_array_fat), axis=0)
        # Convert to NCHW[D] format: (1,c,y,x,z)
        # NCHW[D] stands for: batch N, channels C, height H, width W, depth D
        input_array = input_array.transpose(0,2,1,3) # from (x,y,z) to (y,x,z)
        input_array = np.expand_dims(input_array, axis=(0))

        # Convert to tensor
        input_tensor = torch.tensor(input_array)

        # Load model weights
        weights = torch.load(weights_path, map_location=device)
        model.load_state_dict(weights)
        model.eval() 

        with torch.no_grad():
            output_tensor = sliding_window_inference(input_tensor, (80,80,80), 4, model, overlap=overlap, device=device_str, progress=True) 

    # From probabilities for each channel to label image
    output_tensor = torch.argmax(output_tensor, dim=1)

    # Convert to numpy
    output_array = output_tensor.numpy(force=True)[0,:,:,:]
        
    # Transpose to original shape
    output_array = output_array.transpose(1,0,2) #from (y,x,z) to (x,y,z)

    if postproc == True:
        left_kidney, right_kidney = _kidney_masks(output_array)

    else:
        left_kidney=output_array[output_array == 2]
        right_kidney=output_array[output_array == 1]

    kidneys = {
        "leftkidney": left_kidney,
        "rightkidney": right_kidney
    }
    return kidneys  

def _largest_cluster(array:np.ndarray)->np.ndarray:
    """Given a mask array, return a new mask array containing only the largesr cluster.

    Args:
        array (np.ndarray): mask array with values 1 (inside) or 0 (outside)

    Returns:
        np.ndarray: mask array with only a single connect cluster of pixels.
    """
    # Label all features in the array
    label_img, cnt = ndi.label(array)
    # Find the label of the largest feature
    labels = range(1,cnt+1)
    size = [np.count_nonzero(label_img==l) for l in labels]
    max_label = labels[size.index(np.amax(size))]
    # Return a mask corresponding to the largest feature
    return label_img==max_label

def _kidney_masks(output_array:np.ndarray)->tuple:
    """Extract kidney masks from the output array of the UNETR

    Args:
        output_array (np.ndarray): 3D numpy array (x,y,z) with integer labels (0=background, 1=right kidney, 2=left kidney)

    Returns:
        tuple: A tuple of 3D numpy arrays (left_kidney, right_kidney) with masks for the kidneys.
    """
    left_kidney = _largest_cluster(output_array == 2)
    right_kidney = _largest_cluster(output_array == 1)

    return left_kidney, right_kidney