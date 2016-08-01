

def google_me(zips):
   zip_df = pd.DataFrame(columns=['zip', 'city', 'state', 'lat', 'lng'])
   gmaps = googlemaps.Client(key=os.environ['API_KEY'])
   count = 1
   for zip_code in zips:
       city, state, lat, lng = 'NA', 'NA', 'NA', 'NA'
       try:
           result = gmaps.geocode(zip_code)[0]
           for comp in result['address_components']:
               if 'locality' in comp['types'] or 'neighborhood' in comp['types']:
                   city = comp['short_name']
               if 'administrative_area_level_1' in comp['types']:
                   state = comp['short_name']
           lat = result['geometry']['location']['lat']
           lng = result['geometry']['location']['lng']
       except:
           pass
       zip_df = zip_df.append({'zip': zip_code,
                               'city': city,
                               'state': state,
                               'lat': lat,
                               'lng': lng}, ignore_index=True)
       print(count, '{percent:.2%}'.format(percent=count / len(zips)),
             zip_code, city, state, lat, lng)
       count += 1
   return zip_df
