# model.py

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import numpy as np
from collections import OrderedDict
import time
from tqdm.auto import tqdm
import warnings

def _explain_multi_batch(x_np, w_contrib_np, probabilities_np, num_classes, feature_names, class_names, top_n, print_output):
    """Processes explanations for a batch in the multi-class case."""
    batch_size, n_features = x_np.shape
    explanations = []

    for i in range(batch_size): # Iterate through samples in the batch
        sample_probs = probabilities_np[i] # Probabilities for this sample
        sample_explanation = {
            'sample_index': i,
            'features': {name: val for name, val in zip(feature_names, x_np[i])},
            'predicted_probabilities': {cn: p for cn, p in zip(class_names, sample_probs)}, # Add probs to output
            'classes': {}
        }

        if print_output:
            prob_str = ", ".join([f"'{cn}': {p:.2%}" for cn, p in zip(class_names, sample_probs)])
            print("=" * 5)
            print(f"\n--- Sample {i} (Predicted Probs: {prob_str}) ---")
            print("=" * 5)

        for j in range(num_classes): # Iterate through classes
            class_name = class_names[j]
            class_prob = sample_probs[j]
            class_contributions = w_contrib_np[i, j, :]
            abs_contributions = np.abs(class_contributions)
            sorted_indices = np.argsort(abs_contributions)[::-1]

            top_features_for_class = []
            if print_output:
                print(f"  --- Top Contributions towards Class '{class_name}' with Probability {class_prob:.2%} ---")

            for k in range(min(top_n, n_features)):
                feature_idx = sorted_indices[k]
                feature_name = feature_names[feature_idx]
                feature_value = x_np[i, feature_idx]
                contribution = class_contributions[feature_idx]
                top_features_for_class.append({
                    'feature_index': feature_idx,
                    'feature_name': feature_name,
                    'feature_value': feature_value,
                    'contribution': contribution
                })
                if print_output:
                     print(f"    Rank {k+1}: Feature '{feature_name}' (value={feature_value:.4f}) -> Contribution={contribution:.4f}")

            sample_explanation['classes'][class_name] = top_features_for_class
        explanations.append(sample_explanation)
    return explanations


def _explain_binary_batch(x_np, w_contrib_np, probabilities_np, feature_names, class_names, top_n, print_output):
    """
    Processes explanations for a batch in the binary class case.
    Expects class_names to be a list/tuple of length 2: [name_for_class_0, name_for_class_1].
    """
    batch_size, n_features = x_np.shape
    explanations = []

    if len(class_names) != 2:
         raise ValueError("For binary explanation, class_names must have exactly two elements.")
    class_0_name = class_names[0]
    class_1_name = class_names[1]


    for i in range(batch_size): # Iterate through samples in the batch
        # probabilities_np has shape (batch_size, 1) for binary (sigmoid output)
        prob_class_1 = probabilities_np[i, 0]
        prob_class_0 = 1.0 - prob_class_1
        sample_explanation = {
            'sample_index': i,
            'features': {name: val for name, val in zip(feature_names, x_np[i])},
            'predicted_probabilities': {class_0_name: prob_class_0, class_1_name: prob_class_1}, # Add probs
            'classes': {}
        }

        if print_output:
            print("=" * 5)
            print(f"\n--- Sample {i} (Predicted Probs: '{class_0_name}': {prob_class_0:.2%}, '{class_1_name}': {prob_class_1:.2%}) ---")
            print("=" * 5)

        # Class 1 (Positive)
        class_1_contributions = w_contrib_np[i, :]
        abs_contributions_1 = np.abs(class_1_contributions)
        sorted_indices_1 = np.argsort(abs_contributions_1)[::-1]
        top_features_class_1 = []
        if print_output:
            print(f"  --- Top Contributions towards Class '{class_1_name}' (Positive)  with Probability {prob_class_1:.2%} ---")
        for k in range(min(top_n, n_features)):
            feature_idx = sorted_indices_1[k]
            feature_name = feature_names[feature_idx]
            feature_value = x_np[i, feature_idx]
            contribution = class_1_contributions[feature_idx]
            top_features_class_1.append({
                'feature_index': feature_idx, 'feature_name': feature_name,
                'feature_value': feature_value, 'contribution': contribution
            })
            if print_output:
                print(f"    Rank {k+1}: Feature '{feature_name}' (value={feature_value:.4f}) -> Contribution={contribution:.4f}")
        sample_explanation['classes'][class_1_name] = top_features_class_1

        # Class 0 (Negative)
        class_0_contributions = -w_contrib_np[i, :]
        sorted_indices_0 = sorted_indices_1
        top_features_class_0 = []
        if print_output:
            print(f"  --- Top Contributions towards Class '{class_0_name}' (Negative)  with Probability {prob_class_0:.2%} ---")
        for k in range(min(top_n, n_features)):
            feature_idx = sorted_indices_0[k]
            feature_name = feature_names[feature_idx]
            feature_value = x_np[i, feature_idx]
            contribution = class_0_contributions[feature_idx]
            top_features_class_0.append({
                 'feature_index': feature_idx, 'feature_name': feature_name,
                 'feature_value': feature_value, 'contribution': contribution
            })
            if print_output:
                 print(f"    Rank {k+1}: Feature '{feature_name}' (value={feature_value:.4f}) -> Contribution={contribution:.4f}")
        sample_explanation['classes'][class_0_name] = top_features_class_0

        explanations.append(sample_explanation)
    return explanations


class IFFNN(nn.Module):
    """
    Interpretable Feedforward Neural Network (IFFNN).

    Achieves interpretability by dynamically computing feature weights based on the input
    and using them in a final linear combination step, similar to logistic/softmax regression.

    Args:
        input_size (int): Number of features in the input data.
        num_classes (int): Number of output classes. Use 1 for binary classification
                           with BCEWithLogitsLoss. Use >= 2 for multi-class classification
                           with CrossEntropyLoss.
        hidden_sizes (list[int], optional): List of integers specifying the size of each
            hidden layer in the weight-generating network. If None, defaults to
            a heuristic: [input_size, input_size // 2, input_size // 2, input_size].
            Defaults to None.
        feature_names (list[str], optional): List of names for the input features.
            If None, names like 'feature_0', 'feature_1',... are generated.
            Defaults to None.
        class_names (list[str], optional): List of names for the output classes.
            - If None (default): Names like 'class_0', 'class_1', ... are generated.
                                For binary classification (num_classes=1), defaults
                                to ['class_0', 'class_1'].
            - If provided for multi-class (num_classes > 1): Must contain exactly
                                `num_classes` strings.
            - If provided for binary classification (num_classes = 1): Must contain
                                exactly 2 strings (e.g., ['Negative', 'Positive'] or
                                ['Benign', 'Malicious']). The first name corresponds to
                                class 0, the second to class 1.
        activation (str, optional): Activation function for hidden layers ('relu' or 'tanh').
            Defaults to 'relu'.
        device (str or torch.device, optional): Device to run the model on ('cpu', 'cuda', 'auto').
            'auto' selects CUDA if available, otherwise CPU. Defaults to 'auto'.
    """
    def __init__(self, input_size, num_classes, hidden_sizes=None, feature_names=None,
                 class_names=None, activation='relu', device='auto'): # Added class_names
        super(IFFNN, self).__init__()

        if input_size <= 0:
            raise ValueError("input_size must be positive")
        if num_classes <= 0:
            raise ValueError("num_classes must be positive")

        self.input_size = input_size
        self.num_classes = num_classes
        self.bicls = (num_classes == 1) # True for binary classification setup

        # --- Feature Names ---
        if feature_names is None:
            self.feature_names = [f'feature_{i}' for i in range(input_size)]
        else:
            if not isinstance(feature_names, (list, tuple)):
                 raise TypeError("feature_names must be a list or tuple of strings.")
            if len(feature_names) != input_size:
                raise ValueError(f"Length of feature_names ({len(feature_names)}) must match input_size ({input_size})")
            if not all(isinstance(name, str) for name in feature_names):
                 raise TypeError("All elements in feature_names must be strings.")
            self.feature_names = list(feature_names) # Store as list

        # --- Class Names --- (New Section)
        if class_names is None:
            # Generate default names
            if self.bicls:
                self.class_names = ['class_0', 'class_1'] # Default for binary
            else:
                self.class_names = [f'class_{i}' for i in range(self.num_classes)]
        else:
            # Validate provided names
            if not isinstance(class_names, (list, tuple)):
                 raise TypeError("class_names must be a list or tuple of strings.")
            if not all(isinstance(name, str) for name in class_names):
                 raise TypeError("All elements in class_names must be strings.")

            if self.bicls:
                if len(class_names) != 2:
                    raise ValueError(f"For binary classification (num_classes=1), class_names must have exactly 2 elements (e.g., ['Negative', 'Positive']), but got {len(class_names)}.")
            else: # Multi-class
                if len(class_names) != self.num_classes:
                    raise ValueError(f"Length of class_names ({len(class_names)}) must match num_classes ({self.num_classes}) for multi-class classification.")
            self.class_names = list(class_names) # Store as list


        # --- Hidden Layer Sizes ---
        # (Keep existing logic)
        if hidden_sizes is None:
            hs1 = max(10, input_size // 2)
            hs2 = max(10, input_size // 2)
            self.hidden_sizes = [input_size, hs1, hs2, input_size]
            print(f"Using default hidden sizes: {self.hidden_sizes}")
        else:
             if not isinstance(hidden_sizes, (list, tuple)) or not all(isinstance(s, int) and s > 0 for s in hidden_sizes):
                 raise ValueError("hidden_sizes must be a list or tuple of positive integers.")
             self.hidden_sizes = hidden_sizes

        # --- Device ---
        # (Keep existing logic)
        if device == 'auto':
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        else:
            self.device = torch.device(device)
        print(f"Using device: {self.device}")

        # --- Activation Function ---
        # (Keep existing logic)
        if activation == 'relu':
            act_fn = nn.ReLU
        elif activation == 'tanh':
            act_fn = nn.Tanh
        else:
            raise ValueError("activation must be 'relu' or 'tanh'")

        # --- Build the Weight-Generating Network (iffnnpart1) ---
        # (Keep existing logic)
        dic = OrderedDict()
        previous_dim = self.input_size
        for i, dim in enumerate(self.hidden_sizes):
            dic[f'linear_{i}'] = nn.Linear(previous_dim, dim)
            dic[f'activation_{i}'] = act_fn()
            previous_dim = dim

        # --- Final Layer for Weights ---
        # (Keep existing logic)
        n_hid = len(self.hidden_sizes)
        if self.bicls:
            final_weight_layer = nn.Linear(previous_dim, self.input_size)
            self.last_bias = nn.Parameter(torch.zeros(1, device=self.device))
        else:
            final_weight_layer = nn.Linear(previous_dim, self.input_size * self.num_classes)
            self.last_bias = nn.Parameter(torch.zeros(self.num_classes, device=self.device))

        dic[f'linear_{n_hid}'] = final_weight_layer
        self.iffnnpart1 = nn.Sequential(dic)

        self.to(self.device)


    def forward(self, x):
        """Performs the forward pass (no changes needed here)."""
        # (Keep existing logic)
        x = x.to(self.device)
        w_latent = self.iffnnpart1(x)
        if self.bicls:
            weights = w_latent
            contributions = weights * x
            out = contributions.sum(dim=1, keepdim=True)
        else:
            weights = w_latent.view(-1, self.num_classes, self.input_size)
            features_broadcast = x.unsqueeze(1)
            contributions = weights * features_broadcast
            out = contributions.sum(dim=2)
        out = out + self.last_bias
        return out

    def explain(self, x, top_n=5, print_output=True):
        """
        Generates explanations for a batch of input samples, including predicted probabilities.

        Calculates the contribution of each feature to the prediction for each class.
        Contribution is defined as W_i(x) * x_i for binary or W_{j,i}(x) * x_i for multi-class.

        Args:
            x (torch.Tensor or np.ndarray): Input data batch of shape (batch_size, input_size).
            top_n (int, optional): Number of top contributing features to show per class.
                                   Defaults to 5.
            print_output (bool, optional): Whether to print the explanations to the console.
                                        Defaults to True.

        Returns:
            list[dict]: A list of dictionaries, one for each sample in the batch.
                        Each dictionary contains:
                        - 'sample_index': Index of the sample in the batch.
                        - 'features': Dictionary of feature names and their values for the sample.
                        - 'predicted_probabilities': Dictionary of class names and their predicted probabilities.
                        - 'classes': Dictionary where keys are the provided or default class names
                                     and values are lists of top contributing features for that class.
                                     Each feature entry is a dict with 'feature_index', 'feature_name',
                                     'feature_value', and 'contribution'.
        """
        if isinstance(x, np.ndarray):
            x_tensor = torch.from_numpy(x).float()
        elif isinstance(x, torch.Tensor):
            x_tensor = x.float()
        else:
            raise TypeError("Input x must be a NumPy array or PyTorch Tensor.")

        x_tensor = x_tensor.to(self.device)
        if x_tensor.ndim == 1:
             x_tensor = x_tensor.unsqueeze(0)
        if x_tensor.shape[1] != self.input_size:
             raise ValueError(f"Input tensor has {x_tensor.shape[1]} features, expected {self.input_size}")

        self.eval()
        with torch.no_grad():
            # --- Calculate Probabilities ---
            probabilities = self.predict_proba(x_tensor) # Calls predict_proba internally
            probabilities_np = probabilities.cpu().numpy() # Keep on CPU

            # --- Get the dynamic weights (output of iffnnpart1) ---
            w_latent = self.iffnnpart1(x_tensor)

            # --- Calculate Contributions: W(x) * x ---
            if self.bicls:
                 weights = w_latent
                 contributions = weights * x_tensor
                 w_contrib_np = contributions.cpu().numpy()
                 x_np = x_tensor.cpu().numpy()
                 # Pass probabilities to the helper
                 results = _explain_binary_batch(x_np, w_contrib_np, probabilities_np, self.feature_names, self.class_names, top_n, print_output)
            else:
                 weights = w_latent.view(-1, self.num_classes, self.input_size)
                 features_broadcast = x_tensor.unsqueeze(1)
                 contributions = weights * features_broadcast
                 w_contrib_np = contributions.cpu().numpy()
                 x_np = x_tensor.cpu().numpy()
                 # Pass probabilities to the helper
                 results = _explain_multi_batch(x_np, w_contrib_np, probabilities_np, self.num_classes, self.feature_names, self.class_names, top_n, print_output)

        return results

    # --- predict_proba, predict, train_model ---
    # No changes are needed in these methods as they don't directly interact
    # with class names beyond the number of classes.

    def predict_proba(self, x):
        """Predicts class probabilities (no changes needed)."""
        if isinstance(x, np.ndarray):
            x_tensor = torch.from_numpy(x).float()
        elif isinstance(x, torch.Tensor):
            x_tensor = x.float()
        else:
            raise TypeError("Input x must be a NumPy array or PyTorch Tensor.")

        x_tensor = x_tensor.to(self.device)
        if x_tensor.ndim == 1:
             x_tensor = x_tensor.unsqueeze(0)
        if x_tensor.shape[1] != self.input_size:
             raise ValueError(f"Input tensor has {x_tensor.shape[1]} features, expected {self.input_size}")


        self.eval()
        with torch.no_grad():
            logits = self.forward(x_tensor)
            if self.bicls:
                probabilities = torch.sigmoid(logits)
            else:
                probabilities = F.softmax(logits, dim=1)
        return probabilities.cpu()

    def predict(self, x):
        """Predicts class labels (no changes needed)."""
        probabilities = self.predict_proba(x)
        if self.bicls:
            predictions = (probabilities > 0.5).long().squeeze(-1)
        else:
            predictions = torch.argmax(probabilities, dim=1)
        return predictions


    def train_model(self, train_loader, valid_loader, num_epochs=50, learning_rate=1e-3,
                    criterion=None, optimizer=None, save_path=None, print_every=10, patience=5):
        """Trains the IFFNN model (no changes needed)."""
        t1 = time.time()
        history = {'train_loss': [], 'valid_loss': [], 'valid_acc': [], 'best_epoch': -1}

        if criterion is None:
            if self.bicls:
                criterion = nn.BCEWithLogitsLoss()
            else:
                criterion = nn.CrossEntropyLoss()
        else:
             if self.bicls and not isinstance(criterion, (nn.BCEWithLogitsLoss, nn.BCELoss)):
                 warnings.warn("Using a non-standard loss for binary classification.")
             elif not self.bicls and not isinstance(criterion, nn.CrossEntropyLoss):
                  warnings.warn("Using a non-standard loss for multi-class classification.")


        if optimizer is None:
            optimizer = optim.Adam(self.parameters(), lr=learning_rate)
        else:
             if not optimizer.param_groups or not any(p is param for group in optimizer.param_groups for p in group['params'] for param in self.parameters()):
                  warnings.warn("Provided optimizer does not seem to be linked to model parameters. Reinitializing Adam.")
                  optimizer = optim.Adam(self.parameters(), lr=learning_rate)


        best_valid_acc = -1.0
        print(f"Starting training for {num_epochs} epochs...")

        for epoch in range(num_epochs):
            self.train()
            train_loss_epoch = 0.0
            num_train_batches = 0
            for batch_x, batch_y in train_loader:
                batch_x = batch_x.to(self.device)
                batch_y = batch_y.to(self.device)
                if self.bicls:
                    batch_y = batch_y.float().view(-1, 1)
                else:
                    batch_y = batch_y.long()
                outputs = self.forward(batch_x)
                loss = criterion(outputs, batch_y)
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
                train_loss_epoch += loss.item()
                num_train_batches += 1
            avg_train_loss = train_loss_epoch / num_train_batches
            history['train_loss'].append(avg_train_loss)

            self.eval()
            valid_loss_epoch = 0.0
            n_correct = 0
            n_samples = 0
            num_valid_batches = 0
            with torch.no_grad():
                for batch_x, batch_y in valid_loader:
                    batch_x = batch_x.to(self.device)
                    batch_y_orig = batch_y
                    batch_y = batch_y.to(self.device)
                    if self.bicls:
                        batch_y_loss = batch_y.float().view(-1, 1)
                    else:
                        batch_y_loss = batch_y.long()
                    outputs = self.forward(batch_x)
                    loss = criterion(outputs, batch_y_loss)
                    valid_loss_epoch += loss.item()
                    num_valid_batches += 1
                    if self.bicls:
                        predicted = (torch.sigmoid(outputs) > 0.5).long()
                        n_correct += (predicted.cpu() == batch_y_orig.view(-1,1)).sum().item()
                        n_samples += batch_y_orig.size(0)
                    else:
                        _, predicted = torch.max(outputs.data, 1)
                        n_correct += (predicted.cpu() == batch_y_orig).sum().item()
                        n_samples += batch_y_orig.size(0)

            avg_valid_loss = valid_loss_epoch / num_valid_batches
            valid_acc = 100.0 * n_correct / n_samples
            history['valid_loss'].append(avg_valid_loss)
            history['valid_acc'].append(valid_acc)

            if print_every and (epoch + 1) % print_every == 0:
                print(f'Epoch [{epoch+1}/{num_epochs}], Train Loss: {avg_train_loss:.4f}, '
                      f'Valid Loss: {avg_valid_loss:.4f}, Valid Acc: {valid_acc:.2f}%')
            if patience > 0:
                if 'best_epoch' in history and history['best_epoch'] != -1:
                    if epoch - history['best_epoch'] >= patience:
                        print(f"Early stopping at epoch {epoch+1} (patience reached).")
                        break

            if valid_acc > best_valid_acc:
                best_valid_acc = valid_acc
                history['best_epoch'] = epoch
                if save_path:
                    try:
                         torch.save(self.state_dict(), save_path)
                         if print_every and (epoch + 1) % print_every == 0:
                             print(f"  Best model saved to {save_path} (Epoch {epoch+1}, Valid Acc: {valid_acc:.2f}%)")
                    except Exception as e:
                         print(f"  Error saving model: {e}")

        print(f"Training finished. Best validation accuracy: {best_valid_acc:.2f}% at epoch {history['best_epoch']+1}")
        print(f"Total training time: {time.time()-t1:.2f} seconds")

        if save_path and history['best_epoch'] != -1:
             try:
                 self.load_state_dict(torch.load(save_path, map_location=self.device))
                 self.eval()
                 print(f"Loaded best model weights from epoch {history['best_epoch']+1}")
             except Exception as e:
                  print(f"Error loading best model state from {save_path}: {e}")

        return history
    
    def evaluate_model(self, test_loader):
        """
        Evaluates the model on a test dataset.

        Args:
            test_loader (DataLoader): DataLoader for the test dataset.

        Returns:
            dict: A dictionary containing the test accuracy.
        """
        self.eval()
        n_correct = 0
        n_samples = 0

        with torch.no_grad():
            for batch_x, batch_y in test_loader:
                batch_x = batch_x.to(self.device)
                batch_y_orig = batch_y
                outputs = self.forward(batch_x)
                if self.bicls:
                    predicted = (torch.sigmoid(outputs) > 0.5).long()
                    n_correct += (predicted.cpu() == batch_y_orig.view(-1,1)).sum().item()
                    n_samples += batch_y_orig.size(0)
                else:
                    _, predicted = torch.max(outputs.data, 1)
                    n_correct += (predicted.cpu() == batch_y_orig).sum().item()
                    n_samples += batch_y_orig.size(0)
        test_acc = 100.0 * n_correct / n_samples
        print(f"Test Accuracy: {test_acc:.2f}%")
        return {'test_accuracy': test_acc}