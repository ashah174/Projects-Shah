import numpy as np
import time


def load_data(file_path): # Loads dataset from the specified file path
   return np.loadtxt(file_path)


def classifier(data, feat): # Implements the nearest neighbor classifier using selected features
   correct = 0
   for i in range(data.shape[0]): # Loop through each instance in the dataset
       current = data[i, 1:][feat] # Extracts the feature values for the current instance
       label = data[i, 0]    # Extract the true label
       best_dist = float('inf')
       best_label = -1
      
       for k in range(data.shape[0]):  # Compare with all other instances
           if k != i:                   # Avoid comparing an instance to itself            
               neighbor = data[k, 1:][feat]   # Extract neighbor's feature values
               dist = np.sqrt(np.sum((current - neighbor) ** 2))   # Compute Euclidean distance
               if dist < best_dist:
                   best_dist = dist
                   best_label = data[k, 0]  # Assign the label of the closest neighbor
      
      
       if label == best_label:
           correct += 1  # Count correct classifications
  
   accuracy = (correct / data.shape[0]) * 100  # Convert to percentage
   return accuracy


def forward_select(data):   # forward selection to find the best subset of features
   num_feat = data.shape[1] - 1 
   best_set = []           # Store the best feature subset
   best_acc = 0.0          # Track the highest accuracy
  
   print("\nStarting Forward Selection...")
   for i in range(num_feat):
       add_feature = -1
       local_acc = 0.0
      
       for feature in range(num_feat):
           if feature not in best_set:  # Check if feature is already selected
               current_set = best_set + [feature]   # Test with the new feature added
               acc = classifier(data, current_set)  # Compute accuracy
               print(f"Using features {current_set}, accuracy is {acc:.1f}%")
              
               if acc > local_acc:
                   local_acc = acc
                   add_feat = feature   # Store the best feature to add
      
       if local_acc > best_acc:
           best_acc = local_acc
           best_set.append(add_feat)
           print(f"Feature set {best_set} is best, accuracy is {best_acc:.1f}%")
       else:
           print("Accuracy did not improve. Stopping.")
           break
  
   print("\nForward Selection Complete!")
   print(f"Best feature set: {best_set} with accuracy {best_acc:.1f}%")
   return best_acc

def backward_eliminate(data):  # backward elimination to find the best subset of features
   num_feat = data.shape[1] - 1 
   best_set = list(range(num_feat))  # Start with all features
   best_acc = classifier(data, best_set) # Compute initial accuracy
  
   print("\nStarting Backward Elimination...")
   print(f"Using all features {best_set}, accuracy is {best_acc:.1f}%")
  
   for i in range(num_feat):
       remove_feature = -1
       local_acc = 0.0
      
       for feature in best_set:
           current_set = best_set.copy()
           current_set.remove(feature)   # Test with one feature removed
           acc = classifier(data, current_set)
           print(f"Using features {current_set}, accuracy is {acc:.1f}%")
          
           if acc > local_acc:
               local_acc = acc
               remove_feat = feature   # Store the feature to remove
      
       if local_acc > best_acc:
           best_acc = local_acc
           best_set.remove(remove_feat)    # Update the best feature set
           print(f"Feature set {best_set} is best, accuracy is {best_acc:.1f}%")
       else:
           print("Accuracy did not improve. Stopping.")
           break
  
   print("\nBackward Elimination Complete!")
   print(f"Best feature set: {best_set} with accuracy {best_acc:.1f}%")
   return best_acc

def main():
  
   print("Welcome to Anokhee's Feature Selection Algorithm!")
   file_path = input("Enter the datat set that you would like to you. \nWe have a large data set or a small data set: ")
   data = load_data(file_path)
  
   num_feat = data.shape[1] - 1  # Exclude the label column
   num_instances = data.shape[0]
   print(f"\nThis dataset has {num_feat} features and {num_instances} instances.")
  
   # Test accuracy using all features
   start_time = time.time()
   all_acc = classifier(data, list(range(num_feat)))
   end_time = time.time()
   print(f"\nUsing all features, accuracy is {all_acc:.1f}%")
   print(f"Time taken: {end_time - start_time:.4f} seconds")
  
   print("\nChoose an algorithm:")
   print("1) (Forward Selection")
   print("2) (Backward Elimination")
   choice = int(input("Enter your choice (1 or 2): "))
  
   start_time = time.time()
  
   if choice == 1:
       print("\nRunning Forward Selection...")
       accuracy = forward_select(data)
   elif choice == 2:
       print("\nRunning Backward Elimination...")
       accuracy = backward_eliminate(data)
   else:
       print("Invalid choice. Exiting.")
       return
  
   end_time = time.time()
  
   print(f"\nTotal time taken: {end_time - start_time:.4f} seconds")


if __name__ == "__main__":
   main()
