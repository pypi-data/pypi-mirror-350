from torch import nn




# Define model
class NeuralNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        
        # Add transformer encoder layer
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=768,
            nhead=8,
            dim_feedforward=2048,
            dropout=0.1
        )
        
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=2)
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(768, 256),
            nn.ReLU(),
            nn.Linear(256, 64),
            nn.ReLU(),
            nn.Linear(64, 5),
        )

    def forward(self, x):
        # Reshape input: [batch_size, features] -> [1, batch_size, features]
        if x.dim() == 1:
            x = x.unsqueeze(0).unsqueeze(0)  # Add sequence and batch dimensions
        elif x.dim() == 2:
            x = x.unsqueeze(0)  # Add sequence dimension
            
        # Apply transformer
        x = self.transformer(x)
        
        # Remove sequence dimension and apply linear layers
        x = x.squeeze(0)
        logits = self.linear_relu_stack(x)
        return logits
