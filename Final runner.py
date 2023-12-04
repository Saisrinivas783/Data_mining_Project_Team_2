#%%
# Importing necessary libraries
import random
import os
import shutil
import codecs
import numpy as np
import os
import pandas as pd

import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import seaborn  as sns
import numpy as np
import matplotlib.pyplot as plt
import scipy 
from sklearn.manifold import TSNE
import scipy.stats as stats

from tqdm import tqdm
import imageio
import os
import codecs
import array
import numpy as np

sns.set()

# %%
class shift_files:
    """
    A class to handle the organization of files from a source directory to two separate destination directories.

    Attributes:
        source (str): Name of the source directory.
        destination_1 (str): Name of the first destination directory for certain file types.
        destination_2 (str): Name of the second destination directory for other file types.
    """

    def __init__(self):
        """
        Initializes the shift_files class with source and destination directory names.
        It creates the destination directories if they do not exist.
        """
        # Initial setup: defining source and destination directories
        source = 'train'
        destination_1 = 'byteFiles'
        destination_2 = 'asmFiles'

        # Create destination directories if they don't exist
        if not os.path.isdir(destination_1):
            os.makedirs(destination_1)
        if not os.path.isdir(destination_2):
            os.makedirs(destination_2)

        # Assigning instance variables for source and destinations
        self.source = source
        self.destination_1 = destination_1
        self.destination_2 = destination_2

    @staticmethod
    def process(source, destination_1, destination_2):
        """
        Processes the files from the source directory and moves them to appropriate destination directories.

        Args:
            source (str): The source directory from which to move files.
            destination_1 (str): The first destination directory.
            destination_2 (str): The second destination directory.
        """
        # Check if source directory exists
        if os.path.isdir(source):
            # Listing files in the source directory
            data_files = os.listdir(source)
            asm_files = {}
            bytes_files = {}

            # Categorizing files by their extension
            for file in data_files:
                if file.endswith(".asm"):
                    asm_files[file.split('.')[0]] = file
                elif file.endswith(".bytes"):
                    bytes_files[file.split('.')[0]] = file

            # Selecting files based on predefined IDs from a CSV file
            ids_selected = pd.read_csv('IDS_selected.csv')
            ids_selected = ids_selected['ID'].to_list()
            selected_bytes_keys = ids_selected

            # Moving selected files to their respective destination directories
            for key in selected_bytes_keys:
                asm_file = asm_files.get(key + ".asm")
                if asm_file:
                    shutil.move(os.path.join(source, bytes_files[key]), destination_1)
                    shutil.move(os.path.join(source, asm_file), destination_2)
        else:
            # Error message if the source directory doesn't exist
            print("Please keep source file named 'train' in the same folder as the runner. Download link \
                  https://www.kaggle.com/competitions/malware-classification/data")

    def execute(self):
        """
        Executes the file shifting process using the class attributes.
        """
        # Executing the file processing using instance attributes
        shift_files.process(self.source, self.destination_1, self.destination_2)

# Creating an instance of the class and executing the process
shift_files_instance = shift_files()
shift_files_instance.execute()

#%%
class ByteFileProcessor:
    """
    This class provides a static method to process byte files stored in a specific directory.
    It reads each file, calculates the frequency of each byte value, and writes the results to a CSV file.
    """

    @staticmethod
    def process_byte_files():
        """
        Processes byte files stored in the 'byteFiles' directory and writes the byte frequency features to a CSV file.
        """
        # Listing all files in the 'byteFiles' directory
        files = os.listdir('byteFiles')
        filenames = []
        # Initializing a matrix to store features for each file (256 byte values + 1 for '??')
        feature_matrix = np.zeros((len(files), 257), dtype=int)
        k = 0  # Index for tracking the current file

        # Creating and writing headers to the byte feature CSV file
        byte_feature_file = open('byteoutputfile.csv', 'w+')
        byte_feature_file.write("ID,0,1,2,3,4,5,6,7,8,9,0a,0b,0c,0d,0e,0f,10,11,12,13,14,15,16,17,18,19,1a,1b,1c,1d,1e,1f,20,21,22,23,24,25,26,27,28,29,2a,2b,2c,2d,2e,2f,30,31,32,33,34,35,36,37,38,39,3a,3b,3c,3d,3e,3f,40,41,42,43,44,45,46,47,48,49,4a,4b,4c,4d,4e,4f,50,51,52,53,54,55,56,57,58,59,5a,5b,5c,5d,5e,5f,60,61,62,63,64,65,66,67,68,69,6a,6b,6c,6d,6e,6f,70,71,72,73,74,75,76,77,78,79,7a,7b,7c,7d,7e,7f,80,81,82,83,84,85,86,87,88,89,8a,8b,8c,8d,8e,8f,90,91,92,93,94,95,96,97,98,99,9a,9b,9c,9d,9e,9f,a0,a1,a2,a3,a4,a5,a6,a7,a8,a9,aa,ab,ac,ad,ae,af,b0,b1,b2,b3,b4,b5,b6,b7,b8,b9,ba,bb,bc,bd,be,bf,c0,c1,c2,c3,c4,c5,c6,c7,c8,c9,ca,cb,cc,cd,ce,cf,d0,d1,d2,d3,d4,d5,d6,d7,d8,d9,da,db,dc,dd,de,df,e0,e1,e2,e3,e4,e5,e6,e7,e8,e9,ea,eb,ec,ed,ee,ef,f0,f1,f2,f3,f4,f5,f6,f7,f8,f9,fa,fb,fc,fd,fe,ff,??\n")

        # Processing each file in the directory
        for file in files:
            filenames.append(file)
            byte_feature_file.write(file + ",")
            # Reading and processing each line in the file if it's a text file
            if file.endswith("txt"):
                with open('byteFiles/' + file, "r") as byte_file:
                    for lines in byte_file:
                        line = lines.rstrip().split(" ")
                        # Counting occurrences of each byte value
                        for hex_code in line:
                            if hex_code == '??':
                                feature_matrix[k][256] += 1
                            else:
                                feature_matrix[k][int(hex_code, 16)] += 1

            # Writing the feature matrix to the CSV file
            for i, row in enumerate(feature_matrix[k]):
                byte_feature_file.write(str(row) + ","

#%%
class AsmFileProcessor:
    """
    This class provides static methods to process assembly (asm) files. It analyzes these files for specific patterns
    including prefixes, opcodes, keywords, and registers, and records their frequencies in a CSV file.
    """

    @staticmethod
    def firstprocess():
        """
        Processes assembly files and writes various feature counts to a CSV file.
        """
        # Defining lists of assembly language components to be counted
        prefixes = ['HEADER:', '.text:', '.Pav:', '.idata:', '.data:', '.bss:', '.rdata:', '.edata:', '.rsrc:', '.tls:', '.reloc:', '.BSS:', '.CODE']
        opcodes = ['jmp', 'mov', 'retf', 'push', 'pop', 'xor', 'retn', 'nop', 'sub', 'inc', 'dec', 'add', 'imul', 'xchg', 'or', 'shr', 'cmp', 'call', 'shl', 'ror', 'rol', 'jnb', 'jz', 'rtn', 'lea', 'movzx']
        keywords = ['.dll', 'std::', ':dword']
        registers = ['edx', 'esi', 'eax', 'ebx', 'ecx', 'edi', 'ebp', 'esp', 'eip']

        # Opening a file for writing the feature counts
        asm_output_file = open("asmoutputfile.csv", "w+")  
        files = os.listdir('asmfiles')

        # Processing each file in the 'asmfiles' directory
        for f in files:
            # Initializing count arrays for each feature type
            prefixescount = np.zeros(len(prefixes), dtype=int)
            opcodescount = np.zeros(len(opcodes), dtype=int)
            keywordcount = np.zeros(len(keywords), dtype=int)
            registerscount = np.zeros(len(registers), dtype=int)
            features = []
            f2 = f.split('.')[0]
            asm_output_file.write(f2 + ",")
            
            # Reading and processing each line in the assembly file
            with codecs.open('asmfiles/' + f, encoding='cp1252', errors='replace') as fli:
                for lines in fli:
                    line = lines.rstrip().split()
                    l = line[0]
                    
                    # Counting prefixes
                    for i in range(len(prefixes)):
                        if prefixes[i] in line[0]:
                            prefixescount[i] += 1
                    
                    line = line[1:]
                    
                    # Counting opcodes
                    for i in range(len(opcodes)):
                        if any(opcodes[i] == li for li in line):
                            features.append(opcodes[i])
                            opcodescount[i] += 1
                    
                    # Counting registers in specific sections
                    for i in range(len(registers)):
                        for li in line:
                            if registers[i] in li and ('text' in l or 'CODE' in l):
                                registerscount[i] += 1
                    
                    # Counting keywords
                    for i in range(len(keywords)):
                        for li in line:
                            if keywords[i] in li:
                                keywordcount[i] += 1
            
            # Writing the counts to the output file
            for prefix in prefixescount:
                asm_output_file.write(str(prefix) + ",")
            for opcode in opcodescount:
                asm_output_file.write(str(opcode) + ",")
            for register in registerscount:
                asm_output_file.write(str(register) + ",")
            for key in keywordcount:
                asm_output_file.write(str(key) + ",")
            asm_output_file.write("\n")
        
        # Closing the output file
        asm_output_file.close()

    @staticmethod
    def main():
        """
        Main method to execute the processing of assembly files.
        """
        # Calling the first processing method
        AsmFileProcessor.firstprocess()

# Executing the main method of the AsmFileProcessor class
AsmFileProcessor.main()

#%%
# Reading CSV files containing features extracted from asm and byte files
asm_file = pd.read_csv('asmoutputfile.csv')
byte_file = pd.read_csv('byteoutputfile.csv')

# Removing the ".txt" extension from the IDs in the byte file
byte_file['ID'] = byte_file['ID'].apply(lambda x: x[:-4])

# Reading the labels file and renaming the column for consistency
labels = pd.read_csv('trainLabels.csv').rename(columns={'Id': "ID"})

#%%
# Extracting the column names from both feature files
byte_cols = byte_file.columns.to_list()
asm_cols = asm_file.columns.to_list()

# Printing the number of features in each file
print(len(byte_cols) - 1, 'Unigram byte features')
print(len(asm_cols) - 1, 'Unigram asm features')

def make_box_labels(Y):
    """
    Creates a box plot for the distribution of labels in the dataset.

    Args:
        Y (DataFrame): A DataFrame containing the class/label column.
    """
    total = len(Y) * 1.0
    ax = sns.countplot(x="Class", data=Y)

    ax.set_title("Distribution of Labels")
    # Adding annotations to the plot
    for p in ax.patches:
        ax.annotate('{:.1f}%'.format(100 * p.get_height() / total), (p.get_x() + 0.1, p.get_height() + 5))

    # Setting the y-axis ticks and labels to represent percentages
    ax.yaxis.set_ticks(np.linspace(0, total, 11))
    ax.set_yticklabels(map('{:.1f}%'.format, 100 * ax.yaxis.get_majorticklocs() / total))

    # Displaying the plot with a grid
    plt.grid()
    plt.show()

# Merging the byte and asm files on their ID, then merging with labels
final_df = byte_file.merge(asm_file, on="ID", how="inner")
final_df = final_df.merge(labels, on='ID', how='inner')

# Visualizing the distribution of classes/labels in the final dataset
make_box_labels(final_df[["ID", 'Class']])

#%%

class Analysis:
    """
    This class provides various static methods for data analysis, including normalization, t-SNE plotting, 
    counts and probabilities calculation, and distribution comparison.
    """

    def __init__(self):
        """
        Initialize the Analysis class. Currently, the initializer does not perform any action.
        """
        pass

    @staticmethod
    def normalize(df, columns):
        """
        Normalize the specified columns of a DataFrame, excluding 'ID' and 'Class' columns.

        Parameters:
        df (DataFrame): The DataFrame to be normalized.
        columns (list): List of columns to normalize.

        Returns:
        DataFrame: A copy of the original DataFrame with normalized columns.
        """
        result1 = df.copy()
        for feature_name in columns:
            # Skip normalization for 'ID' and 'Class' columns
            if str(feature_name) not in ['ID', 'Class']:
                max_value = df[feature_name].max()
                min_value = df[feature_name].min()
                # Perform min-max normalization
                result1[feature_name] = (df[feature_name] - min_value) / (max_value - min_value)
        return result1

    @staticmethod
    def get_Tsne_plot(result, val, data_y, type_):
        """
        Generate and display a t-SNE plot.

        Parameters:
        result (DataFrame): The DataFrame containing data to be visualized using t-SNE.
        val (int): Perplexity value for t-SNE.
        data_y (Series): Class labels for the data points.
        type_ (str): A descriptive string for the plot title.
        """
        xtsne = TSNE(perplexity=val)
        result = xtsne.fit_transform(result.drop(['ID'], axis=1))
        vis_x = result[:, 0]
        vis_y = result[:, 1]

        # Generate and display the scatter plot
        plt.title("T-SNE Dist plot for " + type_)
        plt.scatter(vis_x, vis_y, c=data_y, cmap=plt.cm.get_cmap("jet", 9))
        plt.colorbar(ticks=range(10))
        plt.clim(0.5, 9)
        plt.show()

    @staticmethod
    def get_counts(df):
        """
        Calculate the sum of integer columns and the maximum of the 'Class' column for each row in a DataFrame.

        Parameters:
        df (DataFrame): The DataFrame to be processed.

        Returns:
        Series: Sum of integer columns and maximum of 'Class' column.
        """
        df_bytes = df.select_dtypes(include='int64').sum(axis=0)
        df_bytes['Class'] = df['Class'].max()

        return df_bytes

    @staticmethod
    def get_probs(final_df, asm_cols, byte_cols):
        """
        Calculate probabilities for given columns grouped by 'Class'.

        Parameters:
        final_df (DataFrame): The DataFrame to be analyzed.
        asm_cols (list): List of assembly columns.
        byte_cols (list): List of byte columns.

        Returns:
        tuple: Two DataFrames containing probabilities for byte and assembly columns, respectively.
        """
        # Remove 'ID' from columns if present
        asm_cols = [col for col in asm_cols if col != 'ID']
        byte_cols = [col for col in byte_cols if col != 'ID']

        counts_df = final_df.groupby('Class').apply(Analysis.get_counts)

        # Calculate sums and probabilities
        byte_counts = counts_df[byte_cols[:]].sum(axis=1)
        asm_counts = counts_df[asm_cols[:]].sum(axis=1)

        bytes_probs = counts_df[byte_cols[:]].div(byte_counts.values, axis=0).T
        asm_probs = counts_df[asm_cols[:]].div(asm_counts.values, axis=0).T

        return bytes_probs, asm_probs

    @staticmethod
    def compare_dists(df):
        """
        Compare the distributions of DataFrame columns against normal and Bernoulli distributions.

        Parameters:
        df (DataFrame): The DataFrame whose columns are to be compared.

        """
        distributions = ['norm', 'bernoulli']

        fig, axes = plt.subplots(nrows=9, ncols=2, figsize=(10, 30))

        # Loop through each column and distribution for comparison
        for i, column in enumerate(df.columns):
            for j, distribution in enumerate(distributions):
                ax = axes[i][j]
                if distribution == 'norm':
                    # Normal distribution comparison
                    stats.probplot(df[column], dist=distribution, plot=ax)
                    ax.set_title(f'{column} - {distribution.capitalize()}')
                elif distribution == 'bernoulli':
                    # Bernoulli distribution comparison
                    quantiles = df[column].rank(pct=True)
                    stats.probplot(quantiles, dist='uniform', plot=ax)
                    ax.set_title(f'{column} - Empirical vs Uniform')
                
                ax.grid(True)

        plt.tight_layout()
        plt.show()


#%%
# Assign the 'Class' column from the 'final_df' DataFrame to 'data_y'.
data_y = final_df.Class

# Normalize the data in 'final_df' for the columns specified in 'byte_cols'.
byte_data = Analysis.normalize(final_df, byte_cols)

# Generate and display a t-SNE plot using the normalized byte data.
Analysis.get_Tsne_plot(byte_data, 50, data_y, "Byte Unigrams")

#%%
# Generate and display a t-SNE plot using the normalized byte data.
Analysis.get_Tsne_plot(byte_data, 30, data_y, "Byte Unigrams")

#%%
# Assign the 'Class' column from the 'final_df' DataFrame to 'data_y'.
data_y = final_df.Class

# Normalize the data in 'final_df' for the columns specified in 'asm_cols'.
asm_data = Analysis.normalize(final_df, asm_cols)

# Generate and display a t-SNE plot using the normalized assembly data.
Analysis.get_Tsne_plot(asm_data.fillna(0), 50, data_y, "ASM Unigrams")

#%%
# Assign the 'Class' column from the 'final_df' DataFrame to 'data_y'.
data_y = final_df.Class

# Normalize the data in 'final_df' for the columns specified in 'asm_cols'.
asm_data = Analysis.normalize(final_df, asm_cols)

# Generate and display a t-SNE plot using the normalized assembly data.
Analysis.get_Tsne_plot(asm_data.fillna(0), 30, data_y, "ASM Unigrams")

#%%
# Assign the 'Class' column from the 'final_df' DataFrame to 'data_y'.
data_y = final_df.Class

# Normalize the data in 'final_df' for the columns specified in 'asm_cols' and 'byte_cols'.
whole_data = Analysis.normalize(final_df, asm_cols + byte_cols)

# Generate and display a t-SNE plot using the normalized data (assembly and byte data combined).
Analysis.get_Tsne_plot(whole_data.fillna(0), 50, data_y, "ASM + Bytes Unigrams")


#%%
# Generate and display a t-SNE plot using the normalized data (assembly and byte data combined) but different perplexity value for the t-SNE plot.
Analysis.get_Tsne_plot(whole_data.fillna(0), 30, data_y, "ASM + Bytes Unigrams")


#%%
# Calculate probabilities for byte columns in 'final_df'.
bytes_probs, _ = Analysis.get_probs(final_df, asm_cols, byte_cols)

# Compare the distributions of byte probabilities against predefined distributions.
Analysis.compare_dists(bytes_probs)

#%%
# This segment calculates probabilities for assembly columns in 'final_df' using the 'get_probs' method.
_, asm_probs = Analysis.get_probs(final_df, asm_cols, byte_cols)

# Compare the distributions of assembly probabilities against predefined distributions.
Analysis.compare_dists(asm_probs)

#%%
# Export the 'final_df' DataFrame to a CSV file named 'final_df.csv'.
final_df.to_csv('final_df.csv', header=True)

#%%

def collect_img_asm():
    """
    Reads binary files from a directory ('asmFiles'), converts them into square images, 
    and saves these images back to the same directory with a '.png' extension.

    Each file in the 'asmFiles' directory is processed. The function calculates the size
    of the file to determine the dimensions of the square image. The binary data is read,
    reshaped into a square, and then saved as a PNG image. The original file is deleted
    after the image is created.
    """
    # Iterate over each file in the 'asmFiles' directory
    for i, asmfile in tqdm(enumerate(os.listdir("asmFiles"))):
        # Extract the base filename without extension
        filename = asmfile.split('.')[0]

        # Open the binary file in read-binary mode
        file = codecs.open("asmFiles/" + asmfile, 'rb')

        # Get the file size to calculate the dimensions of the square image
        filelen = os.path.getsize("asmFiles/" + asmfile)
        width = int(filelen ** 0.5)  # Calculate the width of the square
        rem = int(filelen / width)   # Calculate the remaining length after reshaping

        # Read the binary data from the file
        arr = array.array('B')
        arr.frombytes(file.read())
        file.close()

        # Reshape the binary data into a square and convert it to uint8 type
        reshaped = np.reshape(arr[:width * width], (width, width))
        reshaped = np.uint8(reshaped)

        # Remove the original file
        os.remove("asmFiles/" + asmfile)

        # Save the reshaped data as a PNG image
        imageio.imwrite('asmFiles/' + filename + '.png', reshaped)

# Call the function to process the files
collect_img_asm()


#%%
import os
import cv2

class ImageFeatureExtractor:
    """
    This class provides a static method to extract features from images and save them as a CSV file.
    The method processes images in a specified directory, flattens each image into a one-dimensional array,
    and normalizes these arrays to form a feature dataset, which is then saved to a CSV file.
    """

    @staticmethod
    def extract_image_features():
        """
        Extracts features from images stored in a directory and saves the feature data to a CSV file.

        The method reads each image from the 'asmFiles' directory, flattens the image into a one-dimensional
        array (limited to the first 800 pixels), and stores these pixel values in a dataset. The dataset is
        normalized and saved as a CSV file to a specified path.
        """
        asm_files_directory = 'asmFiles'  # Hard-coded ASM files directory
        csv_file_path = 'E:/Malware_Classification/imgdf_data.csv'  # Hard-coded CSV file path
        
        # Initialize an array to store image features
        imagefeatures = np.zeros((3001, 800))
        asmfs = []  # List to store the names of the ASM files
        imgfeatures_name = []  # List to store the feature names

        # Iterate over each file in the ASM files directory
        for i, asmfile in tqdm(enumerate(os.listdir(asm_files_directory))):
            asmfs.append(asmfile[:-4])  # Append the file name without extension
            # Read the image and flatten it to extract features
            img = cv2.imread(os.path.join(asm_files_directory, asmfile))
            img_arr = img.flatten()[:800]  # Flatten the image and take the first 800 pixels
            imagefeatures[i, :] += img_arr  # Add the flattened image to the feature array

        # Generate feature names (e.g., pix0, pix1, ..., pix799)
        for i in range(800):
            imgfeatures_name.append('pix' + str(i))

        # Normalize the features and create a DataFrame
        imgdf = pd.DataFrame(normalize(imagefeatures, axis=0), columns=imgfeatures_name)
        imgdf['ID'] = asmfs  # Add the file names as an ID column

        # Save the feature DataFrame to a CSV file
        imgdf.to_csv(csv_file_path, index=False)

# Call the static method to extract image features
ImageFeatureExtractor.extract_image_features()

#%%
# Read image feature data and the existing final dataset into DataFrames
image_data = pd.read_csv('imgdf_data.csv')
final_df = pd.read_csv('final_df.csv')

# Merge the image data with the final dataset based on the 'ID' column.
final_df = final_df.merge(image_data, on="ID", how="inner").drop('Unnamed: 0', axis=1)

#%%
# Normalize all columns in the merged DataFrame 'final_df' using the 'normalize' method from the 'Analysis' class.
final_df_norm = Analysis.normalize(final_df, final_df.columns)

# Extract the 'Class' column from 'final_df' to use as labels in the t-SNE plot.
data_y = final_df.Class

# Generate and display a t-SNE plot using the normalized DataFrame.
Analysis.get_Tsne_plot(final_df_norm.fillna(0), 50, data_y, "Byte + ASM Unigrams + Pixel")


#%%
# Extract the 'Class' column from 'final_df' to use as labels in the t-SNE plot, but with a different perplexity value (30 instead of 50).
Analysis.get_Tsne_plot(final_df_norm.fillna(0), 30, data_y, "Byte + ASM Unigrams + Pixel")

#%%
# Export the merged and possibly modified 'final_df' DataFrame to a CSV file.
final_df.to_csv("final_df_with_pix.csv", header=True)

#%%
import warnings
warnings.filterwarnings("ignore")  # Ignore warnings to clean up output

import shutil
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pickle
from sklearn.manifold import TSNE
from sklearn import preprocessing
from multiprocessing import Process  # Used for multithreading
import multiprocessing
import codecs  # Used for file operations
import random as r
from xgboost import XGBClassifier
from sklearn.model_selection import RandomizedSearchCV
from sklearn.tree import DecisionTreeClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import log_loss, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB
from sklearn.metrics import classification_report

#NaiveBayesClassifier Class

class NaiveBayesClassifier:
    """
    Class to perform parameter tuning and model selection for different types of Naive Bayes classifiers.

    Attributes:
        X (DataFrame): Feature dataset.
        y (Series): Target variable.
        X_train, X_test, y_train, y_test: Split datasets for training and testing.
    """

    def __init__(self, X, y):
        """
        Initialize the NaiveBayesClassifier with feature and target data.

        Parameters:
            X (DataFrame): Feature dataset.
            y (Series): Target variable.
        """
        self.X = X
        self.y = y
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y, test_size=0.2, random_state=42)

    def tune_params(self, estimator, param_grid):
        """
        Tune parameters for a given estimator using GridSearchCV.

        Parameters:
            estimator: The machine learning estimator to tune.
            param_grid (dict): Parameter grid for the estimator.

        Returns:
            Tuple of best parameters, best score, test accuracy, and best estimator.
        """
        grid = GridSearchCV(estimator=estimator, param_grid=param_grid, cv=5, scoring='accuracy')
        grid.fit(self.X_train, self.y_train)
        return grid.best_params_, grid.best_score_, grid.best_estimator_.score(self.X_test, self.y_test), grid.best_estimator_

    def perform_tuning(self):
        """
        Perform parameter tuning for Gaussian, Multinomial, and Bernoulli Naive Bayes classifiers.

        Returns:
            Best estimators for Gaussian, Multinomial, and Bernoulli Naive Bayes classifiers.
        """
        # Parameter grids for different types of Naive Bayes classifiers
        gnb_params = {'var_smoothing': [1e-9, 1e-8, 1e-7]}  # Gaussian
        mnb_params = {'alpha': [0.1, 0.5, 1.0]}  # Multinomial
        bnb_params = {'alpha': [0.1, 0.5, 1.0]}  # Bernoulli

        # Create classifiers
        gnb = GaussianNB()
        mnb = MultinomialNB()
        bnb = BernoulliNB()

        # Tune and evaluate classifiers
        best_params_gnb, best_score_gnb, test_accuracy_gnb, gnb_be = self.tune_params(gnb, gnb_params)
        best_params_mnb, best_score_mnb, test_accuracy_mnb, mnb_be = self.tune_params(mnb, mnb_params)
        best_params_bnb, best_score_bnb, test_accuracy_bnb, bnb_be = self.tune_params(bnb, bnb_params)

        # Print results
        print("Gaussian Naive Bayes - Best Parameters:", best_params_gnb)
        print("Gaussian Naive Bayes - Best Accuracy Score:", best_score_gnb)
        print("Test Set Accuracy - Gaussian Naive Bayes:", test_accuracy_gnb)

        print("Multinomial Naive Bayes - Best Parameters:", best_params_mnb)
        print("Multinomial Naive Bayes - Best Accuracy Score:", best_score_mnb)
        print("Test Set Accuracy - Multinomial Naive Bayes:", test_accuracy_mnb)

        print("Bernoulli Naive Bayes - Best Parameters:", best_params_bnb)
        print("Bernoulli Naive Bayes - Best Accuracy Score:", best_score_bnb)
        print("Test Set Accuracy - Bernoulli Naive Bayes:", test_accuracy_bnb)

        return gnb_be, mnb_be, bnb_be
class TestMetricsMulticlass:              #TestMetricsMulticlass Class
    """
    Class to compute and display various test metrics for multiclass classification.

    Attributes:
        y_true (array-like): True class labels.
        y_pred_proba (array-like): Predicted probabilities for each class.
    """

    def __init__(self, y_true, y_pred_proba):
        """
        Initialize the TestMetricsMulticlass with true labels and predicted probabilities.

        Parameters:
            y_true (array-like): True class labels.
            y_pred_proba (array-like): Predicted probabilities for each class.
        """
        self.y_true = y_true
        self.y_pred_proba = y_pred_proba

    def compute_confusion_matrix(self):
        """
        Compute the confusion matrix for the predicted classifications.

        Returns:
            Confusion matrix as a 2D array.
        """
        y_pred = self.y_pred_proba.argmax(axis=1)
        return confusion_matrix(self.y_true, y_pred)

    def compute_classification_report(self):
        """
        Generate a classification report for the predicted classifications.

        Returns:
            Text report showing the main classification metrics.
        """
        y_pred = self.y_pred_proba.argmax(axis=1)
        return classification_report(self.y_true, y_pred)

    def compute_multiclass_log_loss(self):
        """
        Compute the multiclass log loss for the predicted probabilities.

        Returns:
            Log loss value.
        """
        return log_loss(self.y_true, self.y_pred_proba)

    @staticmethod
    def plot_confusion_matrix(test_y, predict_y):
        """
        Plot confusion matrix, precision matrix, and recall matrix.

        Parameters:
            test_y (array-like): True class labels.
            predict_y (array-like): Predicted class labels.
        """
        # Code for plotting the matrices...
        # Read the final DataFrame and drop any unnamed columns
final_df = pd.read_csv('final_df.csv').drop('Unnamed: 0', axis=1)

# Normalize the DataFrame using the 'normalize' method from the 'Analysis' class
final_df_norm = Analysis.normalize(final_df, final_df.columns).drop('ID', axis=1)

#%%
# Define a list of column names representing byte features.
bytes_cols = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 
'0a', '0b', '0c', '0d', '0e', '0f', '10', '11', '12', '13', '14', 
'15', '16', '17', '18', '19', '1a', '1b', '1c', '1d', '1e', '1f', 
'20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '2a', 
'2b', '2c', '2d', '2e', '2f', '30', '31', '32', '33', '34', '35', 
'36', '37', '38', '39', '3a', '3b', '3c', '3d', '3e', '3f', '40', 
'41', '42', '43', '44', '45', '46', '47', '48', '49', '4a', '4b', 
'4c', '4d', '4e', '4f', '50', '51', '52', '53', '54', '55', '56', 
'57', '58', '59', '5a', '5b', '5c', '5d', '5e', '5f', '60', '61', 
'62', '63', '64', '65', '66', '67', '68', '69', '6a', '6b', '6c', 
'6d', '6e', '6f', '70', '71', '72', '73', '74', '75', '76', '77', 
'78', '79', '7a', '7b', '7c', '7d', '7e', '7f', '80', '81', '82', 
'83', '84', '85', '86', '87', '88', '89', '8a', '8b', '8c', '8d', 
'8e', '8f', '90', '91', '92', '93', '94', '95', '96', '97', '98', 
'99', '9a', '9b', '9c', '9d', '9e', '9f', 'a0', 'a1', 'a2', 'a3', 
'a4', 'a5', 'a6', 'a7', 'a8', 'a9', 'aa', 'ab', 'ac', 'ad', 'ae', 
'af', 'b0', 'b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8', 'b9', 
'ba', 'bb', 'bc', 'bd', 'be', 'bf', 'c0', 'c1', 'c2', 'c3', 'c4', 
'c5', 'c6', 'c7', 'c8', 'c9', 'ca', 'cb', 'cc', 'cd', 'ce', 'cf', 
'd0', 'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8', 'd9', 'da', 
'db', 'dc', 'dd', 'de', 'df', 'e0', 'e1', 'e2', 'e3', 'e4', 'e5', 
'e6', 'e7', 'e8', 'e9', 'ea', 'eb', 'ec', 'ed', 'ee', 'ef', 'f0', 
'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'fa', 'fb', 
'fc', 'fd', 'fe', 'ff', '??']

# Select byte columns from the DataFrame 'final_df' for the feature set (X).
X = final_df[bytes_cols]
Y = final_df['Class']

# Initialize a Naive Bayes Classifier with the byte features (X) and target variable (Y).
nb_classifier = NaiveBayesClassifier(X, Y)

# Perform parameter tuning for the Naive Bayes classifier.
gnb_byt, mnb_byt, bnb_byt = nb_classifier.perform_tuning()

#%%
# Initialize an instance of TestMetricsMulticlass with the true labels (Y) and 
# predicted probabilities from the Gaussian Naive Bayes classifier (gnb_byt).
test_metrics_multiclass = TestMetricsMulticlass(Y, gnb_byt.predict_proba(X))

# Compute the classification report, which includes precision, recall, f1-score, and support for each class.
class_report = test_metrics_multiclass.compute_classification_report()
print("\nClassification Report:")
print(class_report)

# Compute the multiclass log loss, which measures the performance of the classifier 
multiclass_logloss = test_metrics_multiclass.compute_multiclass_log_loss()
print("\nMulticlass Log Loss:", multiclass_logloss)

# Plot the confusion matrix for the Gaussian Naive Bayes classifier predictions.
TestMetricsMulticlass.plot_confusion_matrix(Y, gnb_byt.predict(X))

#%%
# Initialize an instance of TestMetricsMulticlass with the true labels (Y) and 
# predicted probabilities from the Multinomial Naive Bayes classifier (mnb_byt).
test_metrics_multiclass = TestMetricsMulticlass(Y, mnb_byt.predict_proba(X))

# Compute the classification report for the Multinomial Naive Bayes classifier.
class_report = test_metrics_multiclass.compute_classification_report()
print("\nClassification Report:")
print(class_report)

# Compute the multiclass log loss for the classifier. Log loss measures the accuracy of
multiclass_logloss = test_metrics_multiclass.compute_multiclass_log_loss()
print("\nMulticlass Log Loss:", multiclass_logloss)

# Plot the confusion matrix for the Multinomial Naive Bayes classifier predictions.
TestMetricsMulticlass.plot_confusion_matrix(Y, mnb_byt.predict(X))

#%%
# Initialize an instance of TestMetricsMulticlass with the true labels (Y) and 
# predicted probabilities from the Bernoulli Naive Bayes classifier (bnb_byt).
test_metrics_multiclass = TestMetricsMulticlass(Y, bnb_byt.predict_proba(X))

# Compute the classification report for the Bernoulli Naive Bayes classifier.
class_report = test_metrics_multiclass.compute_classification_report()
print("\nClassification Report:")
print(class_report)

# Compute the multiclass log loss for the classifier. Log loss measures the accuracy of a classifier, particularly for probabilistic predictions. Lower log loss indicates better performance.
multiclass_logloss = test_metrics_multiclass.compute_multiclass_log_loss()
print("\nMulticlass Log Loss:", multiclass_logloss)

# Plot the confusion matrix for the Bernoulli Naive Bayes classifier predictions.
TestMetricsMulticlass.plot_confusion_matrix(Y, bnb_byt.predict(X))

#%%
# Defining a list of column names representing assembly language features.
asm_cols = ['HEADER:', '.text:', '.Pav:', '.idata:', '.data:', '.bss:', '.rdata:', 
'.edata:', '.rsrc:', '.tls:', '.reloc:', '.BSS:', '.CODE', 'jmp', 'mov', 'retf', 
'push', 'pop', 'xor', 'retn', 'nop', 'sub', 'inc', 'dec', 'add', 'imul', 'xchg', 
'or', 'shr', 'cmp', 'call', 'shl', 'ror', 'rol', 'jnb', 'jz', 'rtn', 'lea', 'movzx', 
'.dll', 'std::', ':dword', 'edx', 'esi', 'eax', 'ebx', 'ecx', 'edi', 'ebp', 'esp', 'eip']

# Select assembly language columns from the DataFrame 'final_df' for the feature set (X).
X = final_df[asm_cols]
Y = final_df['Class']

# Initialize a Naive Bayes Classifier with the assembly language features (X) and target variable (Y).
nb_classifier = NaiveBayesClassifier(X, Y)

# Perform parameter tuning for the Naive Bayes classifier.
gnb_byt, mnb_byt, bnb_byt = nb_classifier.perform_tuning()

#%%
# Initialize an instance of TestMetricsMulticlass with the true labels (Y) and predicted probabilities from the Gaussian Naive Bayes classifier (gnb_byt).
test_metrics_multiclass = TestMetricsMulticlass(Y, gnb_byt.predict_proba(X))

# Compute the classification report for the Gaussian Naive Bayes classifier.
class_report = test_metrics_multiclass.compute_classification_report()
print("\nClassification Report:")
print(class_report)

# Compute the multiclass log loss for the classifier. The log loss is a measure of 
multiclass_logloss = test_metrics_multiclass.compute_multiclass_log_loss()
print("\nMulticlass Log Loss:", multiclass_logloss)

# Plot the confusion matrix for the Gaussian Naive Bayes classifier predictions.
TestMetricsMulticlass.plot_confusion_matrix(Y , gnb_byt.predict(X))

#%%
# Create an instance of TestMetricsMulticlass, providing it with the true labels (Y) and the predicted probabilities from the Multinomial Naive Bayes classifier (mnb_byt).
test_metrics_multiclass = TestMetricsMulticlass(Y, mnb_byt.predict_proba(X))

# Compute a classification report for the Multinomial Naive Bayes classifier.
class_report = test_metrics_multiclass.compute_classification_report()
print("\nClassification Report:")
print(class_report)

# Calculate the multiclass log loss for the classifier.
multiclass_logloss = test_metrics_multiclass.compute_multiclass_log_loss()
print("\nMulticlass Log Loss:", multiclass_logloss)

# Plot a confusion matrix based on the predictions from the Multinomial Naive Bayes classifier.
TestMetricsMulticlass.plot_confusion_matrix(Y , mnb_byt.predict(X))

#%%
# Create an instance of TestMetricsMulticlass, providing it with the true labels (Y) and the predicted probabilities from the Multinomial Naive Bayes classifier (mnb_byt).
test_metrics_multiclass = TestMetricsMulticlass(Y, bnb_byt.predict_proba(X))

# Compute a classification report for the Multinomial Naive Bayes classifier.
class_report = test_metrics_multiclass.compute_classification_report()
print("\nClassification Report:")
print(class_report)

# Calculate the multiclass log loss for the classifier.
multiclass_logloss = test_metrics_multiclass.compute_multiclass_log_loss()
print("\nMulticlass Log Loss:", multiclass_logloss)

# Plot a confusion matrix based on the predictions from the Multinomial Naive Bayes classifier.
TestMetricsMulticlass.plot_confusion_matrix(Y , bnb_byt.predict(X))

#%%
# Combine assembly language columns and byte columns to create a comprehensive feature set.
X = final_df[asm_cols + bytes_cols]
Y = final_df['Class']

# Initialize a Naive Bayes Classifier with the combined feature set (X) and target variable (Y).
nb_classifier = NaiveBayesClassifier(X, Y)

# Perform parameter tuning for the Naive Bayes classifier.
gnb_byt , mnb_byt , bnb_byt = nb_classifier.perform_tuning()

#%%
# Initialize an instance of TestMetricsMulticlass with the true labels (Y) and the predicted probabilities from the Gaussian Naive Bayes classifier (gnb_byt).
test_metrics_multiclass = TestMetricsMulticlass(Y, gnb_byt.predict_proba(X))

# Calculate the multiclass log loss for the classifier.
multiclass_logloss = test_metrics_multiclass.compute_multiclass_log_loss()
print("\nMulticlass Log Loss:", multiclass_logloss)

# Plot the confusion matrix for the Gaussian Naive Bayes classifier.
TestMetricsMulticlass.plot_confusion_matrix(Y, gnb_byt.predict(X))

#%%
# Initialize an instance of TestMetricsMulticlass with the actual labels (Y) and the predicted probabilities from the Multinomial Naive Bayes classifier (mnb_byt).
test_metrics_multiclass = TestMetricsMulticlass(Y, mnb_byt.predict_proba(X))

# Compute the classification report for the Multinomial Naive Bayes classifier.
class_report = test_metrics_multiclass.compute_classification_report()
print("\nClassification Report:")
print(class_report)

# Calculate the multiclass log loss for the classifier.
multiclass_logloss = test_metrics_multiclass.compute_multiclass_log_loss()
print("\nMulticlass Log Loss:", multiclass_logloss)

# Plot the confusion matrix for the Multinomial Naive Bayes classifier predictions.
TestMetricsMulticlass.plot_confusion_matrix(Y, mnb_byt.predict(X))

#%%
# Create an instance of TestMetricsMulticlass with the actual labels (Y) and the predicted probabilities from the Bernoulli Naive Bayes classifier (bnb_byt).
test_metrics_multiclass = TestMetricsMulticlass(Y, bnb_byt.predict_proba(X))

# Compute the classification report for the Bernoulli Naive Bayes classifier.
class_report = test_metrics_multiclass.compute_classification_report()
print("\nClassification Report:")
print(class_report)

# Calculate the multiclass log loss for the classifier.
multiclass_logloss = test_metrics_multiclass.compute_multiclass_log_loss()
print("\nMulticlass Log Loss:", multiclass_logloss)

# Plot the confusion matrix based on the predictions made by the Bernoulli Naive Bayes classifier.
TestMetricsMulticlass.plot_confusion_matrix(Y, bnb_byt.predict(X))

#%%
# Read the CSV file into a DataFrame and drop the 'Unnamed: 0' column.
final_df = pd.read_csv('final_df_with_pix.csv').drop('Unnamed: 0', axis=1)

# Selecting features by dropping the 'Class' and 'ID' columns from the DataFrame.
X = final_df.drop(['Class', 'ID'], axis=1)

# Selecting the target variable 'Class'.
Y = final_df['Class']

# Assuming NaiveBayesClassifier is a custom class for Naive Bayes classification.
nb_classifier = NaiveBayesClassifier(X, Y)

# Performing parameter tuning on the Naive Bayes classifier and storing the best types.
gnb_byt, mnb_byt, bnb_byt = nb_classifier.perform_tuning()

#%%
# Importing necessary libraries
from tqdm import tqdm
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import log_loss
from xgboost import XGBClassifier
from sklearn.calibration import CalibratedClassifierCV

# Splitting the dataset into training and cross-validation sets with a stratified split.
x_trn_final, x_cv_final, y_trn_final, y_cv_final = train_test_split(X, Y, stratify=Y, test_size=0.20)

# Defining a range of alpha values for tuning.
alpha = [10, 100, 1000, 2000]

# List to store the log error for each alpha value.
cv_log_error_array = []

# Iterating over each alpha value.
for i in tqdm(alpha):
    # Training the XGBClassifier with current alpha value as the number of estimators.
    x_cfl = XGBClassifier(n_estimators=i)
    x_cfl.fit(x_trn_final, y_trn_final)

    # Calibrating the classifier using the sigmoid method.
    sig_clf = CalibratedClassifierCV(x_cfl, method="sigmoid")
    sig_clf.fit(x_trn_final, y_trn_final)

    # Predicting probabilities on the cross-validation set.
    predict_y = sig_clf.predict_proba(x_cv_final)

    # Calculating the log loss and appending it to the list.
    cv_log_error_array.append(log_loss(y_cv_final, predict_y, labels=x_cfl.classes_, eps=1e-15))

# Printing the log loss for each alpha value.
for i in range(len(cv_log_error_array)):
    print(f'log_loss for alpha = {alpha[i]} is {cv_log_error_array[i]}')

# Finding the alpha value that gives the minimum log loss.
best_alpha = np.argmin(cv_log_error_array)

# Plotting the log loss values against alpha values.
fig, ax = plt.subplots()
ax.plot(alpha, cv_log_error_array, c='g')
for i, txt in enumerate(np.round(cv_log_error_array, 3)):
    ax.annotate((alpha[i], np.round(txt, 3)), (alpha[i], cv_log_error_array[i]))
plt.grid()
plt.title("Cross Validation Error for each alpha")
plt.xlabel("Alpha i's")
plt.ylabel("Error measure")
plt.show()

#%%
# Initializing the XGBClassifier with 10 estimators and using all available threads.
x_cfl = XGBClassifier(n_estimators=10, nthread=-1)

# Fitting the classifier to the training data.
x_cfl.fit(x_trn_final, y_trn_final, verbose=True)

# Calibrating the trained classifier using the sigmoid method.
sig_clf = CalibratedClassifierCV(x_cfl, method="sigmoid")
sig_clf.fit(x_trn_final, y_trn_final)

# Predicting probabilities on the training set.
predict_y = sig_clf.predict_proba(x_trn_final)

# Calculating and printing the log loss on the training set.
print(f'For values of best alpha = {alpha[best_alpha]}, The train log loss is:', log_loss(y_trn_final, predict_y))

# Predicting probabilities on the cross-validation set.
predict_y = sig_clf.predict_proba(x_cv_final)

# Calculating and printing the log loss on the cross-validation set.
print(f'For values of best alpha = {alpha[best_alpha]}, The cross validation log loss is:', log_loss(y_cv_final, predict_y))

#%%
# Assuming TestMetricsMulticlass is a custom class for evaluating multi-class classifiers.

# Creating an instance of TestMetricsMulticlass with true labels and predicted probabilities.
test_metrics_multiclass = TestMetricsMulticlass(y_cv_final, predict_y)

# Computing the classification report, which includes precision, recall, f1-score for each class.
class_report = test_metrics_multiclass.compute_classification_report()
print("\nClassification Report:")
print(class_report)

# Computing the multiclass log loss, a measure of accuracy for a classifier.
multiclass_logloss = test_metrics_multiclass.compute_multiclass_log_loss()
print("\nMulticlass Log Loss:", multiclass_logloss)

# Plotting the confusion matrix for the classifier.
# This function uses the true labels and the predicted labels from the classifier.
TestMetricsMulticlass.plot_confusion_matrix(y_cv_final, sig_clf.predict(x_cv_final))



