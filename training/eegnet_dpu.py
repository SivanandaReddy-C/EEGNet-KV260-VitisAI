import torch
import torch.nn as nn


class EEGNetDPU(nn.Module):

    def __init__(self, num_classes=4):
        super().__init__()

        # ==================================================
        # Block 1: Temporal feature extraction
        # ==================================================

        self.temporal_conv1 = nn.Conv2d(
            in_channels=1,
            out_channels=16,
            kernel_size=(1, 16),
            stride=(1, 1),
            padding=(0, 0),
            bias=False
        )

        self.temporal_bn1 = nn.BatchNorm2d(16)
        self.temporal_relu1 = nn.ReLU()

        # Additional temporal filtering
        self.temporal_conv2 = nn.Conv2d(
            in_channels=16,
            out_channels=16,
            kernel_size=(1, 16),
            stride=(1, 1),
            padding=(0, 0),
            bias=False
        )

        self.temporal_bn2 = nn.BatchNorm2d(16)
        self.temporal_relu2 = nn.ReLU()

        # Additional temporal filtering
        self.temporal_conv3 = nn.Conv2d(
            in_channels=16,
            out_channels=16,
            kernel_size=(1, 16),
            stride=(1, 1),
            padding=(0, 0),
            bias=False
        )

        self.temporal_bn3 = nn.BatchNorm2d(16)
        self.temporal_relu3 = nn.ReLU()

        # ==================================================
        # Block 2: Spatial feature extraction
        #
        # 22 EEG channels
        #
        # 22 -> 12 -> 1
        #
        # Both kernels are <= 16.
        # No depthwise convolution is used.
        # ==================================================

        self.spatial_conv1 = nn.Conv2d(
            in_channels=16,
            out_channels=32,
            kernel_size=(11, 1),
            stride=(1, 1),
            padding=(0, 0),
            bias=False
        )

        self.spatial_bn1 = nn.BatchNorm2d(32)
        self.spatial_relu1 = nn.ReLU()

        self.spatial_conv2 = nn.Conv2d(
            in_channels=32,
            out_channels=32,
            kernel_size=(12, 1),
            stride=(1, 1),
            padding=(0, 0),
            bias=False
        )

        self.spatial_bn2 = nn.BatchNorm2d(32)
        self.spatial_relu2 = nn.ReLU()

        # ==================================================
        # Temporal downsampling
        # ==================================================

        self.pool1 = nn.AvgPool2d(
            kernel_size=(1, 4),
            stride=(1, 4)
        )

        # ==================================================
        # Block 3: Temporal feature extraction
        # ==================================================

        self.temporal_conv4 = nn.Conv2d(
            in_channels=32,
            out_channels=32,
            kernel_size=(1, 8),
            stride=(1, 1),
            padding=(0, 0),
            bias=False
        )

        self.temporal_bn4 = nn.BatchNorm2d(32)
        self.temporal_relu4 = nn.ReLU()

        # ==================================================
        # Block 4: Channel mixing
        # ==================================================

        self.pointwise_conv = nn.Conv2d(
            in_channels=32,
            out_channels=16,
            kernel_size=(1, 1),
            stride=(1, 1),
            padding=(0, 0),
            bias=False
        )

        self.pointwise_bn = nn.BatchNorm2d(16)
        self.pointwise_relu = nn.ReLU()

        # ==================================================
        # Temporal downsampling
        # ==================================================

        self.pool2 = nn.AvgPool2d(
            kernel_size=(1, 8),
            stride=(1, 8)
        )

        # ==================================================
        # Classifier
        # ==================================================

        self.classifier = nn.Linear(
            16 * 28,
            num_classes
        )

    def forward(self, x):

        # ==================================================
        # Block 1: Temporal filtering
        # ==================================================

        x = self.temporal_conv1(x)
        x = self.temporal_bn1(x)
        x = self.temporal_relu1(x)

        x = self.temporal_conv2(x)
        x = self.temporal_bn2(x)
        x = self.temporal_relu2(x)

        x = self.temporal_conv3(x)
        x = self.temporal_bn3(x)
        x = self.temporal_relu3(x)

        # ==================================================
        # Block 2: Spatial filtering
        # ==================================================

        x = self.spatial_conv1(x)
        x = self.spatial_bn1(x)
        x = self.spatial_relu1(x)

        x = self.spatial_conv2(x)
        x = self.spatial_bn2(x)
        x = self.spatial_relu2(x)

        # ==================================================
        # Pool 1
        # ==================================================

        x = self.pool1(x)

        # ==================================================
        # Block 3: Temporal filtering
        # ==================================================

        x = self.temporal_conv4(x)
        x = self.temporal_bn4(x)
        x = self.temporal_relu4(x)

        # ==================================================
        # Block 4: Channel mixing
        # ==================================================

        x = self.pointwise_conv(x)
        x = self.pointwise_bn(x)
        x = self.pointwise_relu(x)

        # ==================================================
        # Pool 2
        # ==================================================

        x = self.pool2(x)

        # ==================================================
        # Classifier
        # ==================================================

        x = torch.flatten(x, start_dim=1)

        x = self.classifier(x)

        return x


# ==========================================================
# Architecture verification
# ==========================================================

if __name__ == "__main__":

    model = EEGNetDPU(num_classes=4)
    model.eval()

    dummy_input = torch.randn(
        1, 1, 22, 1000
    )

    with torch.no_grad():

        x = dummy_input

        print("Input              :", tuple(x.shape))

        # Temporal block
        x = model.temporal_conv1(x)
        print("Temporal Conv 1    :", tuple(x.shape))

        x = model.temporal_bn1(x)
        x = model.temporal_relu1(x)

        x = model.temporal_conv2(x)
        print("Temporal Conv 2    :", tuple(x.shape))

        x = model.temporal_bn2(x)
        x = model.temporal_relu2(x)

        x = model.temporal_conv3(x)
        print("Temporal Conv 3    :", tuple(x.shape))

        x = model.temporal_bn3(x)
        x = model.temporal_relu3(x)

        # Spatial block
        x = model.spatial_conv1(x)
        print("Spatial Conv 1     :", tuple(x.shape))

        x = model.spatial_bn1(x)
        x = model.spatial_relu1(x)

        x = model.spatial_conv2(x)
        print("Spatial Conv 2     :", tuple(x.shape))

        x = model.spatial_bn2(x)
        x = model.spatial_relu2(x)

        # Pool
        x = model.pool1(x)
        print("Pool 1             :", tuple(x.shape))

        # Temporal block
        x = model.temporal_conv4(x)
        print("Temporal Conv 4    :", tuple(x.shape))

        x = model.temporal_bn4(x)
        x = model.temporal_relu4(x)

        # Pointwise
        x = model.pointwise_conv(x)
        print("Pointwise Conv     :", tuple(x.shape))

        x = model.pointwise_bn(x)
        x = model.pointwise_relu(x)

        # Pool
        x = model.pool2(x)
        print("Pool 2             :", tuple(x.shape))

        # Classifier
        x = torch.flatten(x, start_dim=1)
        print("Flatten            :", tuple(x.shape))

        x = model.classifier(x)
        print("Output             :", tuple(x.shape))

    # ======================================================
    # Parameter count
    # ======================================================

    total_params = sum(
        p.numel()
        for p in model.parameters()
    )

    trainable_params = sum(
        p.numel()
        for p in model.parameters()
        if p.requires_grad
    )

    print()
    print("Total parameters    :", total_params)
    print("Trainable parameters:", trainable_params)