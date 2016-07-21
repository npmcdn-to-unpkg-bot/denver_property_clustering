from pymongo import MongoClient
from bs4 import BeautifulSoup
from requests import get
import threading


def scrape_parcel_info(json_object):
    try:
        parc_id = json_object['PIN']
        # print parc_id
        #Chain of title URL with parcel_id from loop
        pre_url = "https://www.denvergov.org/property/realproperty/chainoftitle/#"
        url = pre_url.replace("#", parc_id)
        print url
        #get url and and read content
        url = get(url)
        url_content = url.content
        #Soupify that shit
        soup = BeautifulSoup(url_content, 'html.parser')

        #Our Dic
        dict_to_intsert = {}
        #Search page for first table, get three items of interest for each sale of the
        #home
        sales = []
        table = soup.findAll("table")[1]
        x = (len(table.findAll('tr')))
        for row in table.findAll('tr')[1:x]:
            sales_dict = {}
            try:
                col = row.findAll('td')
                sale_date = col[3].getText()
                price = col[4].getText()
                involved_parties = col[5].getText()
                sales_dict['parcel_id'] = parc_id
                sales_dict['date'] = sale_date
                sales_dict['price'] = price
                sales_dict['parties'] = involved_parties
                try:
                    db.transactions.insert_one(sales_dict)
                    print 'insert'
                except:
                    fo = open(error_file, "a")
                    fo.write("Parcel ID: %s did not write to the DB" % (parcel_id))
                    fo.write('\n')
                    fo.close()

            except:
                pass

    except:
        #Write to failure file
        fo = open(error_file, "a")
        fo.write("Parcel ID: %s, there was a general error" % (parcel_id))
        fo.write('\n')
        fo.close()
    db.parcels.update({"PIN": str(parc_id)},{"$set" : {"scraped":1}})

def denver_scrape_concurrent(parcels):
    """
    Pulls the JSON object for each parcel and
    retrieves the sale data for each parcel id concurrently.
    """
    # ids = [i for x in parcels]
    threads = []
    for i in parcels:
        t = threading.Thread(target=scrape_parcel_info, args=(i, ))
        threads.append(t)

    for thred in threads: thred.start()

    for thred in threads: thred.join()


if __name__ == '__main__':
    #establish Mongo Connection
    client = MongoClient()
    db = client.denver_properties
    parcels = db.parcels

    error_file = ('denver_parcel_errors.txt')
    parcels = db.parcels.find({'scraped': 0})

    denver_scrape_concurrent(parcels)
