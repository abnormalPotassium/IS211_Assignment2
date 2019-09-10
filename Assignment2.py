import urllib.request
import csv
import datetime
import logging
import argparse

def downloadData(url):
    with urllib.request.urlopen(url) as response:
        return response.read()

def processData(rawFile):
    birthdict = {}
    file = csv.reader(rawFile.decode('utf-8').splitlines())
    processedFile = [snip for iden, snip in enumerate(file) if iden > 0]
    linenum = 0
    for row in processedFile:
        linenum += 1
        try:
            row[2] = datetime.datetime.strptime(row[2],'%d/%m/%Y')
        except ValueError:
            assignment2.error(f'Error processing line #{linenum}, for ID #{row[0]}')
        else:
            birthdict[int(row[0])] = (row[1], row[2])
    return birthdict

def displayPerson(id, personData):
    try:
        print(f"Person ID #{id} is {personData[id][0]} with a birthday of {personData[id][1].strftime('%Y-%m-%d')}")
    except KeyError:
        print("No user found with that id")
    
assignment2 = logging.getLogger('assignment2')
assignment2.setLevel(logging.ERROR)
fh = logging.FileHandler('errors.log')
fh.setLevel(logging.ERROR)
formatter = logging.Formatter('%(message)s')
fh.setFormatter(formatter)
assignment2.addHandler(fh)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('url')
    args = parser.parse_args()
    
    if(args.url):
        try:
            csvData = downloadData(args.url)
        except (ValueError, urllib.request.HTTPError):
            print("You have an entered an invalid link, please enter a valid link!")
        
        personData = processData(csvData)

        runtime = True
        while runtime:
            try:
                search = int(input('Type in the ID that you would like to search or type a number less than 1 to exit.\n'))
                if search > 0:
                    displayPerson(search, personData)
                elif search <= 0:
                    print("Exiting Program")
                    runtime = False
            except:
                print("This is not a valid ID or even a number")
                pass

if __name__ == '__main__':
    main()