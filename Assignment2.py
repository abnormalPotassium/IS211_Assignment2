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
            id = int(row[0])
            logging.error(f'Error processing line #<{linenum}>, for ID #<{id}>')
        birthdict[int(row[0])] = (row[1], row[2])
    return birthdict

def displayPerson(id, personData):
    try:
        print(personData[id][1])
        print(f"""Person ID #{id} is {personData[id][1]} with a birthday of {personData[id][2].datetime.datetime.strftime('%Y-%m-%d')
        }""")

    except KeyError:
        print("No user found with that id")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('url')
    args = parser.parse_args()
    
    if(args.url):
        try:
            csvData = downloadData(args.url)
        except (ValueError, urllib.request.HTTPError):
            print("You have an entered an invalid link, please enter a valid link!")

        logging.basicConfig(filename='errors.log', level=logging.ERROR, format='%(message)s')
        logging.getLogger('assignment2')

        personData = processData(csvData)
        print(personData)

        runtime = personData != None
   
        while runtime:
            search = input('Type in the ID that you would like to search\n')
            if int(search) > 0:
                print(displayPerson(search, personData))
        
            elif int(search) <= 0:
                runtime = False

if __name__ == '__main__':
    main()