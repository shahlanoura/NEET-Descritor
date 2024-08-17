def merge_text_files(text_files, output_text_file):
    try:
        # Open the output file in write mode
        with open(output_text_file, 'w') as outfile:
            # Iterate through the list of text files
            for text_file in text_files:
                try:
                    # Open each text file in read mode
                    with open(text_file, 'r') as infile:
                        # Read the content and write it to the output file
                        outfile.write(infile.read())
                        outfile.write("\n")  # Add a newline to separate files
                except Exception as e:
                    # Log or print an error message if a file cannot be read
                    print(f"Error reading file {text_file}: {e}")
        return output_text_file
    except Exception as e:
        # Log or print an error message if the output file cannot be written
        print(f"Error writing to output file {output_text_file}: {e}")
        return None


