import torch
import segmentation_models_pytorch as smp

# Match these to your original training setup
encoder = "xception"
num_classes = 4
checkpoint_in = "Unet-xception_25_original.pt"
checkpoint_out = "Unet-xception_25_weights_only.pt"

# Rebuild the model architecture
model = smp.Unet(
    encoder_name=encoder,
    encoder_weights=None,  # or "imagenet" if used in training
    classes=num_classes,
    activation=None,
)

# Load full model that was saved with torch.save(model)
model_full = torch.load(checkpoint_in, map_location="cpu")

# Copy weights from full model to new instance
model.load_state_dict(model_full.state_dict())

# Save only the state_dict
torch.save(model.state_dict(), checkpoint_out)

print(f"✔ Model successfully converted and saved to '{checkpoint_out}'")
