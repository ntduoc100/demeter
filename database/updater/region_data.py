'''
Run once to create region_data collection
'''
import pymongo
import sys

if __name__=='__main__':

    regions = [
    {'region': 'An Giang', 'id': 1594446, 'lon': 105.166672, 'lat': 10.5}, 
    {'region': 'Ba Ria – Vung Tau', 'id': 1584534, 'lon': 107.25, 'lat': 10.58333}, 
    {'region': 'Bac Lieu', 'id': 1591474, 'lon': 105.724442, 'lat': 9.285}, 
    {'region': 'Bac Giang', 'id': 1591527, 'lon': 106.199997, 'lat': 21.26667}, 
    {'region': 'Bac Kan', 'id': 1905669, 'lon': 105.833328, 'lat': 22.16667}, 
    {'region': 'Bac Ninh', 'id': 1591449, 'lon': 106.050003, 'lat': 21.183331}, 
    {'region': 'Ben Tre', 'id': 1587976, 'lon': 106.383331, 'lat': 10.23333}, 
    {'region': 'Binh Duong', 'id': 1905475, 'lon': 106.666672, 'lat': 11.16667}, 
    {'region': 'Binh Dinh', 'id': 1587871, 'lon': 109.0, 'lat': 14.16667}, 
    {'region': 'Binh Phuoc', 'id': 1905480, 'lon': 106.916672, 'lat': 11.75}, 
    {'region': 'Binh Thuan', 'id': 1581882, 'lon': 108.0, 'lat': 11.08333}, 
    {'region': 'Ca Mau', 'id': 1586443, 'lon': 105.150002, 'lat': 9.17694}, 
    {'region': 'Cao Bang', 'id': 1586185, 'lon': 106.25, 'lat': 22.66667}, 
    {'region': 'Can Tho', 'id': 1586203, 'lon': 105.783333, 'lat': 10.03333}, 
    {'region': 'Da Nang', 'id': 1583992, 'lon': 108.220833, 'lat': 16.06778}, 
    {'region': 'Dak Lak', 'id': 1584169, 'lon': 108.166672, 'lat': 12.83333}, 
    {'region': 'Dak Nong', 'id': 1586896, 'lon': 108.050003, 'lat': 12.66667}, 
    {'region': 'Dien Bien', 'id': 1583477, 'lon': 103.01667, 'lat': 21.383329}, 
    {'region': 'Dong Nai', 'id': 1587923, 'lon': 106.816673, 'lat': 10.95}, 
    {'region': 'Dong Thap', 'id': 1586151, 'lon': 105.633331, 'lat': 10.45}, 
    {'region': 'Gia Lai', 'id': 1581088, 'lon': 108.25, 'lat': 13.75}, 
    {'region': 'Ha Giang', 'id': 1581349, 'lon': 104.98333, 'lat': 22.83333}, 
    {'region': 'Ha Nam', 'id': 1905637, 'lon': 106.0, 'lat': 20.58333}, 
    {'region': 'Hanoi', 'id': 1581129, 'lon': 105.883331, 'lat': 21.116671}, 
    {'region': 'Ha Tinh', 'id': 1580700, 'lon': 105.75, 'lat': 18.33333}, 
    {'region': 'Hai Duong', 'id': 1905686, 'lon': 106.333328, 'lat': 20.91667}, 
    {'region': 'Hai Phong', 'id': 1581298, 'lon': 106.68222, 'lat': 20.85611}, 
    {'region': 'Hau Giang', 'id': 1586203, 'lon': 105.783333, 'lat': 10.03333}, 
    {'region': 'Hoa Binh', 'id': 1580830, 'lon': 105.338333, 'lat': 20.81333}, 
    {'region': 'Hung Yen', 'id': 1580142, 'lon': 106.066673, 'lat': 20.65}, 
    {'region': 'Khanh Hoa', 'id': 1586350, 'lon': 109.159126, 'lat': 11.92144}, 
    {'region': 'Kien Giang', 'id': 1579008, 'lon': 105.166672, 'lat': 10.0}, 
    {'region': 'Kon Tum', 'id': 1565088, 'lon': 107.916672, 'lat': 14.75}, 
    {'region': 'Lai Chau', 'id': 1570815, 'lon': 103.349998, 'lat': 22.533331}, 
    {'region': 'Lang Son', 'id': 1576633, 'lon': 106.73333, 'lat': 21.83333}, 
    {'region': 'Lao Cai', 'id': 1576303, 'lon': 103.949997, 'lat': 22.48333}, 
    {'region': 'Lam Dong', 'id': 1584071, 'lon': 108.441933, 'lat': 11.94646}, 
    {'region': 'Long An', 'id': 1575788, 'lon': 106.166672, 'lat': 10.66667}, 
    {'region': 'Nam Dinh', 'id': 1573517, 'lon': 106.166672, 'lat': 20.41667}, 
    {'region': 'Nghe An', 'id': 1562798, 'lon': 105.666672, 'lat': 18.66667}, 
    {'region': 'Ninh Binh', 'id': 1571968, 'lon': 105.974998, 'lat': 20.253889}, 
    {'region': 'Ninh Thuan', 'id': 1559971, 'lon': 108.833328, 'lat': 11.75}, 
    {'region': 'Phu Tho', 'id': 1569901, 'lon': 105.22702, 'lat': 21.39883}, 
    {'region': 'Phu Yen', 'id': 1563281, 'lon': 109.300003, 'lat': 13.08333}, 
    {'region': 'Quang Binh', 'id': 1582886, 'lon': 106.599998, 'lat': 17.48333}, 
    {'region': 'Quang Nam', 'id': 1580541, 'lon': 108.334999, 'lat': 15.87944}, 
    {'region': 'Quang Ngai', 'id': 1568770, 'lon': 108.800003, 'lat': 15.11667}, 
    {'region': 'Quang Ninh', 'id': 1586357, 'lon': 107.300003, 'lat': 21.01667}, 
    {'region': 'Quang Tri', 'id': 1582926, 'lon': 107.100311, 'lat': 16.81625}, 
    {'region': 'Soc Trang', 'id': 1567788, 'lon': 105.980003, 'lat': 9.60333}, 
    {'region': 'Son La', 'id': 1567681, 'lon': 103.900002, 'lat': 21.316669}, 
    {'region': 'Tay Ninh', 'id': 1566559, 'lon': 106.099998, 'lat': 11.3}, 
    {'region': 'Thai Binh', 'id': 1566346, 'lon': 106.333328, 'lat': 20.450001}, 
    {'region': 'Thai Nguyen', 'id': 1566319, 'lon': 105.84417, 'lat': 21.592779}, 
    {'region': 'Thanh Hoa', 'id': 1566166, 'lon': 105.76667, 'lat': 19.799999}, 
    {'region': 'Ho Chi Minh city', 'id': 1566083, 'lon': 106.666672, 'lat': 10.75}, 
    {'region': 'Thua Thien Hue', 'id': 1580240, 'lon': 107.599998, 'lat': 16.466669}, 
    {'region': 'Tien Giang', 'id': 1574023, 'lon': 106.349998, 'lat': 10.35}, 
    {'region': 'Tra Vinh', 'id': 1563926, 'lon': 106.345284, 'lat': 9.93472}, 
    {'region': 'Tuyen Quang', 'id': 1563287, 'lon': 105.218063, 'lat': 21.82333},  
    {'region': 'Vinh Long', 'id': 1562693, 'lon': 105.966667, 'lat': 10.25}, 
    {'region': 'Vinh Phuc', 'id': 1562548, 'lon': 105.596672, 'lat': 21.309999}, 
    {'region': 'Yen Bai', 'id': 1560349, 'lon': 104.866669, 'lat': 21.700001}, 
]

    # args = sys.argv[1:]
    # if len(args) > 1:
    #     sys.exit()
    
    # connection_str = f'mongodb+srv://root:{args[0]}@cluster0.5qjhz.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
    # connection_str = 'mongodb://localhost:27017'
    connection_str = 'mongodb://demeterdb:27017'

    client = pymongo.MongoClient(connection_str)

    db = client.get_database('demeter')
    collection = db.get_collection('region_data')
    collection.insert_many(regions)
    