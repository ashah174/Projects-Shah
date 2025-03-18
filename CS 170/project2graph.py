import numpy as np
<<<<<<< HEAD
import matplotlib.pyplot as plt
import time
=======
import time
import matplotlib.pyplot as plt
>>>>>>> e4236db (Initial commit with project files, directories, and README)

def load_data(file_path):
    """Load data from a file."""
    return np.loadtxt(file_path)

<<<<<<< HEAD
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
=======
def classify(data, features):
    """Classify data using nearest neighbor and a subset of features."""
    correct = 0
    for i in range(data.shape[0]):
        current = data[i, 1:][features]
        label = data[i, 0]
        best_distance = float('inf')
        best_label = -1
        
        for k in range(data.shape[0]):
            if k != i:
                neighbor = data[k, 1:][features]
                distance = np.sqrt(np.sum((current - neighbor) ** 2))
                if distance < best_distance:
                    best_distance = distance
                    best_label = data[k, 0]
        
        if label == best_label:
            correct += 1
    
    accuracy = (correct / data.shape[0]) * 100  # Convert to percentage
    return accuracy

def forward_select(data):
    """Forward selection algorithm for feature selection."""
    num_features = data.shape[1] - 1  # Exclude the label column
    best_set = []
    best_acc = 0.0
    feature_sets = []
    accuracies = []
    
    print("\nStarting Forward Selection...")
    for i in range(num_features):
        add_feature = -1
        local_acc = 0.0
        
        for feature in range(num_features):
            if feature not in best_set:
                current_set = best_set + [feature]
                acc = classify(data, current_set)
                print(f"Using features {current_set}, accuracy is {acc:.1f}%")
                feature_sets.append(current_set)  # Store feature set
                accuracies.append(acc)  # Store accuracy
                
                if acc > local_acc:
                    local_acc = acc
                    add_feature = feature
        
        if local_acc > best_acc:
            best_acc = local_acc
            best_set.append(add_feature)
            print(f"Feature set {best_set} is best, accuracy is {best_acc:.1f}%")
        else:
            print("Accuracy did not improve. Stopping.")
            break
    
    print("\nForward Selection Complete!")
    print(f"Best feature set: {best_set} with accuracy {best_acc:.1f}%")
    
    # Plot the feature selection results
    plot_feature_selection_accuracies(feature_sets, accuracies, "Forward Selection")
    
    return best_acc

def backward_eliminate(data):
    """Backward elimination algorithm for feature selection."""
    num_features = data.shape[1] - 1  # Exclude the label column
    best_set = list(range(num_features))  # Start with all features
    best_acc = classify(data, best_set)
    feature_sets = []
    accuracies = []
    
    print("\nStarting Backward Elimination...")
    print(f"Using all features {best_set}, accuracy is {best_acc:.1f}%")
    
    for i in range(num_features):
        remove_feature = -1
        local_acc = 0.0
        
        for feature in best_set:
            current_set = best_set.copy()
            current_set.remove(feature)
            acc = classify(data, current_set)
            print(f"Using features {current_set}, accuracy is {acc:.1f}%")
            feature_sets.append(current_set)  # Store feature set
            accuracies.append(acc)  # Store accuracy
            
            if acc > local_acc:
                local_acc = acc
                remove_feature = feature
        
        if local_acc > best_acc:
            best_acc = local_acc
            best_set.remove(remove_feature)
            print(f"Feature set {best_set} is best, accuracy is {best_acc:.1f}%")
        else:
            print("Accuracy did not improve. Stopping.")
            break
    
    print("\nBackward Elimination Complete!")
    print(f"Best feature set: {best_set} with accuracy {best_acc:.1f}%")
    
    # Plot the feature selection results
    plot_feature_selection_accuracies(feature_sets, accuracies, "Backward Elimination")
    
    return best_acc

def plot_feature_selection_accuracies(feature_sets, accuracies, algorithm_name):
    """Plot a bar graph for feature selection accuracies with readability enhancements."""
    plt.figure(figsize=(10, 6))  # Adjust figure size for readability

    # Limit the number of x-axis labels if too many features
    num_features = len(feature_sets)
    step = max(1, num_features // 20)  # Show at most 20 labels
    displayed_labels = [str(feature_sets[i]) if i % step == 0 else '' for i in range(num_features)]
    
    plt.bar(range(num_features), accuracies, color='skyblue')
    plt.xticks(range(num_features), displayed_labels, rotation=45, ha="right")  # Rotate for readability
    plt.xlabel("Feature Set")
    plt.ylabel("Accuracy (%)")
    plt.title(f"{algorithm_name} - Feature Selection Accuracy")  # Set dynamic title


>>>>>>> e4236db (Initial commit with project files, directories, and README)
    plt.show()

def main():
    """Main function to run the program."""
<<<<<<< HEAD
    print("Welcome to Anokhee Shah's Feature Selection Algorithm.")
    file_path = input("Type in the name of the file to test: ")
=======
    print("Welcome to Anokhee's Feature Selection Algorithm!")
    file_path = input("Enter the dataset that you would like to use. \nWe have a large data set or a small data set: ")
>>>>>>> e4236db (Initial commit with project files, directories, and README)
    data = load_data(file_path)
    
    num_features = data.shape[1] - 1  # Exclude the label column
    num_instances = data.shape[0]
<<<<<<< HEAD
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
=======
    print(f"\nThis dataset has {num_features} features and {num_instances} instances.")
    
    # Test accuracy using all features
    start_time = time.time()
    all_acc = classify(data, list(range(num_features)))
    end_time = time.time()
    print(f"\nUsing all features, accuracy is {all_acc:.1f}%")
    print(f"Time taken: {end_time - start_time:.4f} seconds")
    
    print("\nChoose an algorithm:")
    print("1) Forward Selection")
    print("2) Backward Elimination")
    choice = int(input("Enter your choice (1 or 2): "))
>>>>>>> e4236db (Initial commit with project files, directories, and README)
    
    start_time = time.time()
    
    if choice == 1:
        print("\nRunning Forward Selection...")
<<<<<<< HEAD
        feature_sets, accuracies = forward_selection(data)
        plot_feature_selection(feature_sets, accuracies, "Forward Selection Accuracy Over Time")
    elif choice == 2:
        print("\nRunning Backward Elimination...")
        feature_sets, accuracies = backward_elimination(data)
        plot_feature_selection(feature_sets, accuracies, "Backward Elimination Accuracy Over Time")
=======
        accuracy = forward_select(data)
    elif choice == 2:
        print("\nRunning Backward Elimination...")
        accuracy = backward_eliminate(data)
>>>>>>> e4236db (Initial commit with project files, directories, and README)
    else:
        print("Invalid choice. Exiting.")
        return
    
    end_time = time.time()
    
<<<<<<< HEAD
    print(f"\nTime taken: {end_time - start_time:.4f} seconds")

if __name__ == "__main__":
    main()
=======
    print(f"\nTotal time taken: {end_time - start_time:.4f} seconds")

if __name__ == "__main__":
    main()
>>>>>>> e4236db (Initial commit with project files, directories, and README)
