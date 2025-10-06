import GenerateSidedPDF

def main():
    print("\n------FLAG-CARD-GENERATOR-------")

    while True:
        response = input("Output path, File name (separated by space): ")
        try:
            file_path, file_name = response.split(' ', 1)  # allow spaces in path
            GenerateSidedPDF.generate_sided_pdf(file_path, file_name)
            print(f"Document generated successfully! saved at {file_path}\\{file_name}.pdf")
            break 
        except ValueError:
            print("Please provide both <path> and <filename> separated by space.")
        except Exception as e:
            print(f"Error: {e}")
            print("Try again.\n")

if __name__ == '__main__':
    main()