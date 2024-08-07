import requests
from bs4 import BeautifulSoup

class MyHTMLExtraction:

    def __init__(self, url):
        self.url = url

    def getHTMLContent(self):
        response = requests.get(self.url)
        return response.content

    def parseHTMLTable(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        table = soup.find('table')
        return table

    def getTableData(self, table):
        data = [
                 [td.text.strip() for td in tr.find_all('td')]
                 for tr in table.find_all('tr')
                  if tr.find_all('td')
        ]
        return data

    def convertCoordinatesToNumber(self, data):
        headers = data[0]
        _data = data[1:]
        convertedData = []
        for row in _data:
            try:
                x = int(row[0])
                y = int(row[2])
                char = row[1]
                convertedData.append({
                    headers[0]: x,
                    headers[1]: char,
                    headers[2]: y
                })
            except ValueError:
                print(f"Invalid data found & skipped: {row}")

        # convertedTable = [
        #     {
        #      headers[0]: int(row[0]),
        #      headers[1]: row[1],
        #      headers[2]: int(row[2])
        #     }
        #     for row in _data
        # ]
        # print(convertedData)
        return convertedData

    def createGrid(self, convertedData):

        maxX = max(entry['x-coordinate'] for entry in convertedData)
        maxY = max(entry['y-coordinate'] for entry in convertedData)

        grid = [[' ' for _ in range(maxX+ 1)] for _ in range(maxY +1)]

        for entry in convertedData:
            x = entry['x-coordinate']
            y = entry['y-coordinate']
            char = entry['Character']
            grid[y][x] = char
        return grid

    def printGrid(self, grid):

        # for row in range(len(grid)):
        #     for col in range(len(grid[row])):
        #         print(grid[row][col])
        for row in grid:
            print(' '.join(row))

    def main(self):

        htmlcontent = self.getHTMLContent()
        htmltable = self.parseHTMLTable(htmlcontent)
        data = self.getTableData(htmltable)
        converteddata = self.convertCoordinatesToNumber(data)
        grid = self.createGrid(converteddata)
        self.printGrid(grid)

if __name__ == "__main__":
    url = "https://docs.google.com/document/d/e/2PACX-1vSHesOf9hv2sPOntssYrEdubmMQm8lwjfwv6NPjjmIRYs_FOYXtqrYgjh85jBUebK9swPXh_a5TJ5Kl/pub"
    handle = MyHTMLExtraction(url)
    handle.main()