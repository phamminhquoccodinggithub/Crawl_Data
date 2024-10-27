import pandas as pd


def read_csv_data(file_path):
    """
    Read data from a CSV file.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        pandas.DataFrame: A DataFrame containing the CSV data.
    """
    try:
        df = pd.read_csv(file_path)
        print(f"Successfully read data from {file_path}")
        return df
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except pd.errors.EmptyDataError:
        print(f"Error: The file at {file_path} is empty")
        return None
    except Exception as e:
        print(f"An error occurred while reading the file: {str(e)}")
        return None


def write_to_txt(data, output_file):
    """
    Write data to a text file.

    Args:
        data (list): The data to be written to the file.
        output_file (str): The name of the output text file.
    """
    try:
        with open(output_file, 'a', encoding='utf-8') as file:
            for item in data:
                file.write(f"{item}\n")
        print(f"Successfully wrote data to {output_file}")
    except IOError as e:
        print(f"An error occurred while writing to the file: {str(e)}")


def process_data_lazada(data):
    """
    Process the input data.

    This function takes a pandas DataFrame as input and processes it to extract
    and clean the data from a specific column. It performs the following steps:
    1. Converts the DataFrame to a dictionary.
    2. Extracts the data from column '2', index 0.
    3. Removes the first and last characters (assumed to be brackets).
    4. Removes any remaining square brackets.
    5. Splits the string into a list of items.

    Args:
        data (pandas.DataFrame): The input DataFrame containing the data to process.

    Returns:
        list: A list of processed data items.

    Note:
        This function assumes a specific structure of the input data, where the
        relevant information is stored in column '2' and needs to be cleaned and split.
        If the data structure changes, this function may need to be updated.
    """
    if data is not None:
        content = data.to_dict()
        res = []
        for col in content.keys():
            # Process the data
            tst_data = content[col][0]
            tst_data = tst_data[1:-1]
            tst_data = tst_data.replace('[', '')
            tst_data = tst_data.replace(']', '')
            lst = tst_data.split("',")
            res.extend(lst)
    return set(res)


def main():
    """
    Main function to orchestrate the data processing and writing.
    """
    # Define file paths
    csv_file_path = ['lazada_comment_1.csv', 'lazada_comment_2.csv', 'lazada_comment_3.csv',
                     'lazada_comment_4.csv', 'lazada_comment_5.csv', 'lazada_comment_6.csv', 'lazada_comment_7.csv']
    output_file_path = 'output.txt'

    for f in csv_file_path:
        # Read CSV data
        data = read_csv_data('data/' + f)
        lst = process_data_lazada(data)
        if lst is not None:
            # Write processed data to text file
            write_to_txt(lst, output_file_path)
        else:
            print("Failed to process data due to error in reading CSV file.")

    # # Define file paths
    # csv_file_path = 'lazada_comment_1.csv'
    # output_file_path = 'output.txt'

    # # Read CSV data
    # data = read_csv_data(csv_file_path)
    # lst = process_data(data)
    # if lst is not None:
    #     # Write processed data to text file
    #     write_to_txt(lst, output_file_path)
    # else:
    #     print("Failed to process data due to error in reading CSV file.")


def process_data_tiki(data):
    """
    Process data from a pandas DataFrame, extracting and cleaning content.

    This function takes a pandas DataFrame as input, extracts the 'content' column,
    converts it to a list, and returns a set of unique content items.

    Args:
        data (pandas.DataFrame): The input DataFrame containing a 'content' column.

    Returns:
        set: A set of unique, cleaned content items.

    Note:
        This function assumes that the input DataFrame has a 'content' column.
        If the DataFrame structure changes, this function may need to be updated.
    """
    if data is not None:
        content = data.content.to_list()
        return set(content)


def export_data():
    # Define file paths
    csv_file_path = ['comments_data_gbn.csv', 'comments_data_gln.csv', 'comments_data_gsn.csv',
                     'comments_data_gtcs.csv', 'comments_data_ncds.csv']
    output_file_path = 'output.txt'
    for f in csv_file_path:
        # Read CSV data
        data = read_csv_data('data/' + f)
        lst = process_data_tiki(data)
        if lst is not None:
            # Write processed data to text file
            write_to_txt(lst, output_file_path)
        else:
            print("Failed to process data due to error in reading CSV file.")


if __name__ == "__main__":
    export_data()
