import numpy as np
import matplotlib.pyplot as plt
import time

def load_data(file_path):
    """Load data from a file."""
    return np.loadtxt(file_path)

def nearest_neighbor_classification(data, features):
    """Perform nearest neighbor classification using a subset of features."""
    number_correctly_classified = 0
    for i in range(data.shape[0]):
        object_to_classify = data[i, 1:][features]
        label_object_to_classify = data[i, 0]
        nearest_neighbor_distance = float('inf')
        nearest_neighbor_label = -1
        
        for k in range(data.shape[0]):
            if k != i:
                neighbor_features = data[k, 1:][features]
                distance = np.sqrt(np.sum((object_to_classify - neighbor_features) ** 2))
                if distance < nearest_neighbor_distance:
                    nearest_neighbor_distance = distance
                    nearest_neighbor_label = data[k, 0]
        
        if label_object_to_classify == nearest_neighbor_label:
            number_correctly_classified += 1
    
    accuracy = (number_correctly_classified / data.shape[0]) * 100  # Convert to percentage
    return accuracy

def forward_selection(data):
    """Forward selection algorithm for feature selection."""
    num_features = data.shape[1] - 1  # Exclude the label column
    best_features = []
    best_accuracy = 0.0
    accuracy_list = []
    feature_sets = []

    print("\nBeginning Forward Selection search.")
    for i in range(num_features):
        feature_to_add = -1
        best_local_accuracy = 0.0
        
        for feature in range(num_features):
            if feature not in best_features:
                current_features = best_features + [feature]
                accuracy = nearest_neighbor_classification(data, current_features)
                print(f"Using feature(s) {current_features} accuracy is {accuracy:.1f}%")
                
                if accuracy > best_local_accuracy:
                    best_local_accuracy = accuracy
                    feature_to_add = feature
        
        if best_local_accuracy > best_accuracy:
            best_accuracy = best_local_accuracy
            best_features.append(feature_to_add)
            print(f"Feature set {best_features} was best, accuracy is {best_accuracy:.1f}%")
        else:
            print("Warning: Accuracy did not improve. Stopping forward selection.")
            break
        
        accuracy_list.append(best_accuracy)
        feature_sets.append(str(best_features))

    print("\nFinished Forward Selection!")
    print(f"Best feature subset (Forward Selection): {best_features} with accuracy {best_accuracy:.1f}%")
    return feature_sets, accuracy_list

def backward_elimination(data):
    """Backward elimination algorithm for feature selection."""
    num_features = data.shape[1] - 1  # Exclude the label column
    best_features = list(range(num_features))  # Start with all features
    best_accuracy = nearest_neighbor_classification(data, best_features)
    
    accuracy_list = [best_accuracy]
    feature_sets = [str(best_features)]

    print("\nBeginning Backward Elimination search.")
    print(f"Using all features {best_features} accuracy is {best_accuracy:.1f}%")
    
    for i in range(num_features):
        feature_to_remove = -1
        best_local_accuracy = 0.0
        
        for feature in best_features:
            current_features = best_features.copy()
            current_features.remove(feature)
            accuracy = nearest_neighbor_classification(data, current_features)
            print(f"Using feature(s) {current_features} accuracy is {accuracy:.1f}%")
            
            if accuracy > best_local_accuracy:
                best_local_accuracy = accuracy
                feature_to_remove = feature
        
        if best_local_accuracy > best_accuracy:
            best_accuracy = best_local_accuracy
            best_features.remove(feature_to_remove)
            print(f"Feature set {best_features} was best, accuracy is {best_accuracy:.1f}%")
        else:
            print("Warning: Accuracy did not improve. Stopping backward elimination.")
            break
        
        accuracy_list.append(best_accuracy)
        feature_sets.append(str(best_features))

    print("\nFinished Backward Elimination!")
    print(f"Best feature subset (Backward Elimination): {best_features} with accuracy {best_accuracy:.1f}%")
    return feature_sets, accuracy_list

def plot_feature_selection(feature_sets, accuracies, title):
    """Plot the feature selection process."""
    plt.figure(figsize=(10, 5))
    plt.bar(feature_sets, accuracies, color='gray')
    plt.xlabel("Feature Sets")
    plt.ylabel("Accuracy (%)")
    plt.ylim(0, 100)
    plt.xticks(rotation=30, ha='right')
    plt.title(title)
    plt.show()

def main():
    """Main function to run the program."""
    print("Welcome to Anokhee Shah's Feature Selection Algorithm.")
    file_path = input("Type in the name of the file to test: ")
    data = load_data(file_path)
    
    num_features = data.shape[1] - 1  # Exclude the label column
    num_instances = data.shape[0]
    print(f"\nThis dataset has {num_features} features (not including the class attribute), with {num_instances} instances.")
    
    # Evaluate accuracy using all features
    start_time = time.time()
    all_features_accuracy = nearest_neighbor_classification(data, list(range(num_features)))
    end_time = time.time()
    print(f"Running nearest neighbor with all features, using 'leave-one-out' evaluation, I get an accuracy of {all_features_accuracy:.1f}%")
    print(f"Time taken: {end_time - start_time:.4f} seconds")
    
    print("\nType the number of the algorithm you want to run:")
    print("1) Forward Selection")
    print("2) Backward Elimination")
    choice = int(input())
    
    start_time = time.time()
    
    if choice == 1:
        print("\nRunning Forward Selection...")
        feature_sets, accuracies = forward_selection(data)
        plot_feature_selection(feature_sets, accuracies, "Forward Selection Accuracy Over Time")
    elif choice == 2:
        print("\nRunning Backward Elimination...")
        feature_sets, accuracies = backward_elimination(data)
        plot_feature_selection(feature_sets, accuracies, "Backward Elimination Accuracy Over Time")
    else:
        print("Invalid choice. Exiting.")
        return
    
    end_time = time.time()
    
    print(f"\nTime taken: {end_time - start_time:.4f} seconds")

if __name__ == "__main__":
    main()
