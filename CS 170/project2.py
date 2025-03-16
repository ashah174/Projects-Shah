import numpy as np
import os
import time

def load_data(file_path):
    """Load data from a file."""
    return np.loadtxt(file_path)

def nearest_neighbor_classifier(data, features):
    """Nearest Neighbor Classifier with selected features."""
    number_correctly_classified = 0
    
    for i in range(data.shape[0]):
        object_to_classify = data[i, features]
        label_object_to_classify = data[i, 0]
        nearest_neighbor_distance = np.inf
        nearest_neighbor_location = np.inf
        
        for k in range(data.shape[0]):
            if k != i:
                distance = np.sqrt(np.sum((object_to_classify - data[k, features]) ** 2))
                if distance < nearest_neighbor_distance:
                    nearest_neighbor_distance = distance
                    nearest_neighbor_location = k
                    nearest_neighbor_label = data[nearest_neighbor_location, 0]
        
        if label_object_to_classify == nearest_neighbor_label:
            number_correctly_classified += 1
    
    accuracy = number_correctly_classified / data.shape[0]
    return accuracy

def forward_selection(data):
    """Forward Selection Algorithm."""
    print("\nBeginning Forward Selection search.")
    num_features = data.shape[1] - 1  # Exclude the class label
    best_features = []
    best_accuracy = 0
    
    for i in range(num_features):
        best_current_accuracy = 0
        best_current_feature = None
        
        for feature in range(num_features):
            if feature not in best_features:
                current_features = best_features + [feature]
                accuracy = nearest_neighbor_classifier(data, current_features)
                print(f'Using feature(s) {current_features} accuracy is {accuracy * 100:.1f}%')
                
                if accuracy > best_current_accuracy:
                    best_current_accuracy = accuracy
                    best_current_feature = feature
        
        if best_current_accuracy > best_accuracy:
            best_accuracy = best_current_accuracy
            best_features.append(best_current_feature)
            print(f'Feature set {best_features} was best, accuracy is {best_accuracy * 100:.1f}%')
        else:
            break  # Stop if adding more features doesn't improve accuracy
    
    print("\nFinished Forward Selection!")
    return best_features, best_accuracy

def backward_elimination(data):
    """Backward Elimination Algorithm."""
    print("\nBeginning Backward Elimination search.")
    num_features = data.shape[1] - 1  # Exclude the class label
    best_features = list(range(num_features))  # Start with all features
    best_accuracy = nearest_neighbor_classifier(data, best_features)
    print(f'Using all features {best_features} accuracy is {best_accuracy * 100:.1f}%')
    
    for i in range(num_features):
        worst_current_accuracy = 1.0
        worst_current_feature = None
        
        for feature in best_features:
            current_features = best_features.copy()
            current_features.remove(feature)
            accuracy = nearest_neighbor_classifier(data, current_features)
            print(f'Using feature(s) {current_features} accuracy is {accuracy * 100:.1f}%')
            
            if accuracy > worst_current_accuracy:
                worst_current_accuracy = accuracy
                worst_current_feature = feature
        
        if worst_current_accuracy >= best_accuracy:
            best_accuracy = worst_current_accuracy
            best_features.remove(worst_current_feature)
            print(f'Feature set {best_features} was best, accuracy is {best_accuracy * 100:.1f}%')
        else:
            break  # Stop if removing more features doesn't improve accuracy
    
    print("\nFinished Backward Elimination!")
    return best_features, best_accuracy

def main():
    """Main function to run the program."""
    print("Welcome to Anokhee Shah's Feature Selection Algorithm.")
    file_path = input("Type in the name of the file to test: ")
    
    if not os.path.exists(file_path):
        print("File does not exist. Please check the path and try again.")
        return
    
    # Load the data
    data = load_data(file_path)
    print(f'\nThis dataset has {data.shape[1] - 1} features (not including the class attribute), with {data.shape[0]} instances.')
    
    # Run nearest neighbor with all features
    start_time = time.time()
    accuracy = nearest_neighbor_classifier(data, list(range(1, data.shape[1])))
    end_time = time.time()
    print(f"Running nearest neighbor with all features, using 'leaving-one-out' evaluation, I get an accuracy of {accuracy * 100:.1f}%")
    print(f"Time taken: {end_time - start_time:.4f} seconds")
    
    # Prompt the user to choose an algorithm
    print("\nType the number of the algorithm you want to run:")
    print("1) Forward Selection")
    print("2) Backward Elimination")
    algorithm_choice = input()
    
    if algorithm_choice == '1':
        print("\nRunning Forward Selection...")
        start_time = time.time()
        best_features, best_accuracy = forward_selection(data)
        end_time = time.time()
        print(f"\nBest feature subset (Forward Selection): {best_features} with accuracy {best_accuracy * 100:.1f}%")
        print(f"Time taken: {end_time - start_time:.4f} seconds")
    elif algorithm_choice == '2':
        print("\nRunning Backward Elimination...")
        start_time = time.time()
        best_features, best_accuracy = backward_elimination(data)
        end_time = time.time()
        print(f"\nBest feature subset (Backward Elimination): {best_features} with accuracy {best_accuracy * 100:.1f}%")
        print(f"Time taken: {end_time - start_time:.4f} seconds")
    else:
        print("Invalid choice. Please select a valid algorithm.")

if __name__ == "__main__":
    main()