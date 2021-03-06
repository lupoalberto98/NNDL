### This file contains useful functions for the homework
import torch
import torch.nn as nn


# Test the network on test dataset to check accuracy on mnist classification
def my_accuracy(net, device, dataloader):
    """
    Compute the classification accuracy of the model and confusion matrix
    ___________
    Parameters:
    net = network
    device = training device(cuda/cpu)
    dataloader = dataloader
  
    ________
    Returns:
    mismatched = list of all mismatched examples
    confusion_list = list whose elements are list of true labels and probabilities of the model
    accuracy = classification accuracy
    """
    # Set evaluation mode
    net.eval()

    total = 0
    correct = 0
    mismatched = []
    predictions = []
    trues = []
    
    with torch.no_grad():
        for  x_batch, label_batch in dataloader:
                
            # Move to device
            x_batch = x_batch.to(device)
            label_batch = label_batch.to(device)

            # Forward pass
            y_hat, _ , _ = net(x_batch)
            y_hat = y_hat.squeeze()

            # Apply softmax 
            softmax = nn.Softmax(dim=0)
            out_soft = softmax(y_hat)

            # Take the prediction
            predicted = out_soft.detach().cpu().argmax().item()
            
            # True value
            true = label_batch.detach().cpu().item()

            if predicted==true:
                correct += 1
            else:
                mismatched.append((x_batch.detach().cpu().numpy(), predicted, true))
                
            # Take probabilities
            prob = out_soft.detach().cpu().numpy()
            
            # Append to lists
            predictions.append(predicted)
            trues.append(true)
                                  
            total += 1

    return mismatched, [trues, predictions], 100.0*correct/total
    


