import torch
from utils.torch_utils import select_device
from utils.autobatch import check_train_batch_size

def find_optimal_batch(weights, imgsz=640, amp=True):
    # Select the device (GPU or CPU)
    device = select_device('')
    print(f"selected_device: {device}")
    # Load the model
    model = torch.load(weights, map_location=device)['model'].float()  # Load FP32 model
    model.fuse()  # Fuse Conv2d + BatchNorm2d layers
    if amp:
        model.half()  # Convert model to FP16 if amp (automatic mixed precision) is enabled

    # Find optimal batch size
    return check_train_batch_size(model, imgsz=imgsz, amp=amp)

if __name__ == '__main__':
    weights = '/content/yolov5/weights/yolov5l-cls.pt'  # Path to your weights file
    imgsz = 640  # Image size
    amp = True  # Automatic Mixed Precision (AMP)

    optimal_batch_size = find_optimal_batch(weights, imgsz, amp)
    print(f"Optimal batch size: {optimal_batch_size}")
