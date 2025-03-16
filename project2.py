import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import LeaveOneOut

# Load dataset from file
def load_data(filename):
    data = np.loadtxt(filename)
    X = data[:, 1:]  # Features
    y = data[:, 0]   # Class labels
    return X, y

# Evaluate accuracy using Leave-One-Out Cross Validation
def evaluate_accuracy(X, y):
    loo = LeaveOneOut()
    correct = 0
    for train_idx, test_idx in loo.split(X):
        model = KNeighborsClassifier(n_neighbors=1)
        model.fit(X[train_idx], y[train_idx])
        if model.predict(X[test_idx]) == y[test_idx]:
            correct += 1
    return correct / len(y)

# Forward Selection
def forward_selection(X, y, max_features=None):
    n_features = X.shape[1]
    selected_features = []
    best_accuracy = 0

    print("\nBeginning Forward Selection search.")
    
    for _ in range(n_features):
        best_feature = None
        for i in range(n_features):
            if i in selected_features:
                continue
            temp_features = selected_features + [i]
            acc = evaluate_accuracy(X[:, temp_features], y)
            print(f"Using feature(s) {temp_features} accuracy is {acc * 100:.1f}%")
            if acc > best_accuracy:
                best_accuracy = acc
                best_feature = i

        if best_feature is not None:
            selected_features.append(best_feature)
            print(f"Feature set {selected_features} was best, accuracy is {best_accuracy * 100:.1f}%")

        if max_features and len(selected_features) >= max_features:
            print(f"Max feature set reached: {max_features}")
            break

    print("\nFinished Forward Selection!")
    return selected_features

# Backward Elimination
def backward_elimination(X, y, max_features=None):
    selected_features = list(range(X.shape[1]))
    best_accuracy = evaluate_accuracy(X[:, selected_features], y)

    print("\nBeginning Backward Elimination search.")
    while len(selected_features) > 1:
        worst_feature = None
        for i in selected_features:
            temp_features = selected_features.copy()
            temp_features.remove(i)
            acc = evaluate_accuracy(X[:, temp_features], y)
            print(f"Using feature(s) {temp_features} accuracy is {acc * 100:.1f}%")
            if acc > best_accuracy:
                best_accuracy = acc
                worst_feature = i
        if worst_feature is not None:
            selected_features.remove(worst_feature)
            print(f"Remaining features: {selected_features}, accuracy is {best_accuracy * 100:.1f}%")

        if max_features and len(selected_features) <= max_features:
            print(f"Min feature set reached: {max_features}")
            break

    print("\nFinished Backward Elimination!")
    return selected_features

# Main function
def main():
    print("Welcome to Anokhee Shah's Feature Selection Algorithm.")
    filename = input("Type in the name of the file to test: ")
    X, y = load_data(filename)

    print(f"\nThis dataset has {X.shape[1]} features (not including the class attribute), with {X.shape[0]} instances.")
    
    print("\nRunning nearest neighbor with all features, using 'leaving-one-out' evaluation, I get an")
    accuracy = evaluate_accuracy(X, y)
    print(f"accuracy of {accuracy * 100:.1f}%\n")
    
    choice = int(input("Type the number of the algorithm you want to run:\n1) Forward Selection\n2) Backward Elimination\n"))
    
    max_features = 5  # Optional: Set a limit to the number of features to select, e.g., 5
    
    if choice == 1:
        print("\nRunning Forward Selection...")
        best_forward = forward_selection(X, y, max_features=max_features)
        print(f"Best feature subset (Forward Selection): {best_forward}\n")

    elif choice == 2:
        print("\nRunning Backward Elimination...")
        best_backward = backward_elimination(X, y, max_features=max_features)
        print(f"Best feature subset (Backward Elimination): {best_backward}\n")

if __name__ == "__main__":
    main()
