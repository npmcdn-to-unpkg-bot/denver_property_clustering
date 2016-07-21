from pymongo import MongoClient
from bs4 import BeautifulSoup
from requests import get
# import json
#establish Mongo Connection
client = MongoClient()
db = client.denver
parcels = db.parcels

error_file = ('denver_parcel_errors.txt')

#get parcel_id list
parcel_id_list_m = parcels.find({}, {"PIN":1, "_id":0})

#ditch mongo because the curser will close after some amount of time, which will #kill the scripts. Thus lets throw these ids in a list
parcel_id_list = []
[parcel_id_list.append(i['PIN']) for i in parcel_id_list_m]

parcel_id_list_int = []
for i in parcel_id_list:
    try:
        parcel_id_list_int.append(int(i))
    except:
        pass
# parcel_id_list = [ int(x) for x in parcel_id_list[1:] ]

#this checks which parcels we already scraped
current_par = db.transactions.distinct("parcel_id")
check_list = []
[check_list.append(x) for x in current_par]

check_list = [ int(x) for x in check_list ]

#loop over all parcels and get chain of sale
for parcel_id in parcel_id_list_int:
    parc_id = parcel_id
    try:
        # parc_id = parcel_id['PIN']
        print parc_id
        if parc_id in check_list:
            print 'already scraped'
        else:
            #Chain of title URL with parcel_id from loop
            pre_url = "https://www.denvergov.org/property/realproperty/chainoftitle/#"
            url = pre_url.replace("#", str(parc_id))
            #get url and and read content
            url = get(url)
            url_content = url.content
            print '1'
            #Soupify that shit
            soup = BeautifulSoup(url_content, 'html.parser')

            #Our Dic
            dict_to_intsert = {}
            #Search page for first table, get three items of interest for each sale of the
            #home
            sales = []
            table = soup.findAll("table")[1]
            x = (len(table.findAll('tr')) - 1)
            print '2'
            for row in table.findAll('tr')[1:x]:
                sales_dict = {}
                try:
                    col = row.findAll('td')
                    sale_date = col[3].getText()
                    price = col[4].getText()
                    involved_parties = col[5].getText()
                    sales_dict['parcel_id'] = str(parc_id)
                    sales_dict['date'] = sale_date
                    sales_dict['price'] = price
                    sales_dict['parties'] = involved_parties
                    try:
                        print 'a'
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
