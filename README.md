# DSLR (Data Science Logistic Regression)


### Information

Throughout this project, we learn to maniupulates data and how logistic regression works.  
This project use Harry Potter's courses as a context but this can be used for any types of data.  


### Programs
- #### Describe.py
    This program is used to calculate scores found in the given file as a parameter.  
    It shows how much data it registered for each courses, the means, the std (standard derivation), the lowest and highest score.  
- #### Histogram.py
    This programs purpose is to display the courses where the std is the lowest.
- #### Scatter_plot.py
    This program takes the two courses where their scores are similar and displays a graph, using **matplotlib.pyplot**, containing the scores of each student on both courses.
- #### Pair_plot.py
    This program create a graph for each courses compared to other courses (ie, Arythmancy-Flying, Arythmancy-Potion, ... ) and from those graphs, we choose which courses will be used to train the next program.
- #### Logreg_train.py
    This program is where we will get our weights for each houses depending on the courses we gave it.
    It uses **OvR (One vs Rest)** to compare each houses.
    When the program is done comparing, it saves the result in a file called **"weights.csv"**
- #### Logreg_predict.py
    This program will use the **weights.csv** and the **dataset_test.csv** and will try to guess which student is from which houses.
    There is no way to check if it is indeed true.
    Once the predictions are done, it writes the results in a file called **"houses.csv"**
