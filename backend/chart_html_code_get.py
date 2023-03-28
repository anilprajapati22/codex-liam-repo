from bs4 import BeautifulSoup

def get_div():
    f=open("chart.html","r")

    soup = BeautifulSoup(f.read(),'html.parser')

    div = soup.find("div")
    return str(div)
