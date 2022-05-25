'''
Create region_data collection
'''
import pymongo

if __name__=='__main__':

    regions = [
{'Place': 'An Giang', 'id': 1594446, 'coordinate':[105.166672, 10.5]}, 
    {'Place': 'Ba Ria – Vung Tau', 'id': 1584534, 'coordinate':[107.25, 10.58333]}, 
    {'Place': 'Bac Lieu', 'id': 1591474, 'coordinate':[105.724442, 9.285]}, 
    {'Place': 'Bac Giang', 'id': 1591527, 'coordinate':[106.199997, 21.26667]}, 
    {'Place': 'Bac Kan', 'id': 1905669, 'coordinate':[105.833328, 22.16667]}, 
    {'Place': 'Bac Ninh', 'id': 1591449, 'coordinate':[106.050003, 21.183331]}, 
    {'Place': 'Ben Tre', 'id': 1587976, 'coordinate':[106.383331, 10.23333]}, 
    {'Place': 'Binh Duong', 'id': 1905475, 'coordinate':[106.666672, 11.16667]}, 
    {'Place': 'Binh Dinh', 'id': 1587871, 'coordinate':[109.0, 14.16667]}, 
    {'Place': 'Binh Phuoc', 'id': 1905480, 'coordinate':[106.916672, 11.75]}, 
    {'Place': 'Binh Thuan', 'id': 1581882, 'coordinate':[108.0, 11.08333]}, 
    {'Place': 'Ca Mau', 'id': 1586443, 'coordinate':[105.150002, 9.17694]}, 
    {'Place': 'Cao Bang', 'id': 1586185, 'coordinate':[106.25, 22.66667]}, 
    {'Place': 'Can Tho', 'id': 1586203, 'coordinate':[105.783333, 10.03333]}, 
    {'Place': 'Da Nang', 'id': 1583992, 'coordinate':[108.220833, 16.06778]}, 
    {'Place': 'Dak Lak', 'id': 1584169, 'coordinate':[108.166672, 12.83333]}, 
    {'Place': 'Dak Nong', 'id': 1586896, 'coordinate':[108.050003, 12.66667]}, 
    {'Place': 'Dien Bien', 'id': 1583477, 'coordinate':[103.01667, 21.383329]}, 
    {'Place': 'Dong Nai', 'id': 1587923, 'coordinate':[106.816673, 10.95]}, 
    {'Place': 'Dong Thap', 'id': 1586151, 'coordinate':[105.633331, 10.45]}, 
    {'Place': 'Gia Lai', 'id': 1581088, 'coordinate':[108.25, 13.75]}, 
    {'Place': 'Ha Giang', 'id': 1581349, 'coordinate':[104.98333, 22.83333]}, 
    {'Place': 'Ha Nam', 'id': 1905637, 'coordinate':[106.0, 20.58333]}, 
    {'Place': 'Hanoi', 'id': 1581129, 'coordinate':[105.883331, 21.116671]}, 
    {'Place': 'Ha Tinh', 'id': 1580700, 'coordinate':[105.75, 18.33333]}, 
    {'Place': 'Hai Duong', 'id': 1905686, 'coordinate':[106.333328, 20.91667]}, 
    {'Place': 'Hai Phong', 'id': 1581298, 'coordinate':[106.68222, 20.85611]}, 
    {'Place': 'Hau Giang', 'id': 1586203, 'coordinate':[105.783333, 10.03333]}, 
    {'Place': 'Hoa Binh', 'id': 1580830, 'coordinate':[105.338333, 20.81333]}, 
    {'Place': 'Hung Yen', 'id': 1580142, 'coordinate':[106.066673, 20.65]}, 
    {'Place': 'Khanh Hoa', 'id': 1586350, 'coordinate':[109.159126, 11.92144]}, 
    {'Place': 'Kien Giang', 'id': 1579008, 'coordinate':[105.166672, 10.0]}, 
    {'Place': 'Kon Tum', 'id': 1565088, 'coordinate':[107.916672, 14.75]}, 
    {'Place': 'Lai Chau', 'id': 1570815, 'coordinate':[103.349998, 22.533331]}, 
    {'Place': 'Lang Son', 'id': 1576633, 'coordinate':[106.73333, 21.83333]}, 
    {'Place': 'Lao Cai', 'id': 1576303, 'coordinate':[103.949997, 22.48333]}, 
    {'Place': 'Lam Dong', 'id': 1584071, 'coordinate':[108.441933, 11.94646]}, 
    {'Place': 'Long An', 'id': 1575788, 'coordinate':[106.166672, 10.66667]}, 
    {'Place': 'Nam Dinh', 'id': 1573517, 'coordinate':[106.166672, 20.41667]}, 
    {'Place': 'Nghe An', 'id': 1562798, 'coordinate':[105.666672, 18.66667]}, 
    {'Place': 'Ninh Binh', 'id': 1571968, 'coordinate':[105.974998, 20.253889]}, 
    {'Place': 'Ninh Thuan', 'id': 1559971, 'coordinate':[108.833328, 11.75]}, 
    {'Place': 'Phu Tho', 'id': 1569901, 'coordinate':[105.22702, 21.39883]}, 
    {'Place': 'Phu Yen', 'id': 1563281, 'coordinate':[109.300003, 13.08333]}, 
    {'Place': 'Quang Binh', 'id': 1582886, 'coordinate':[106.599998, 17.48333]}, 
    {'Place': 'Quang Nam', 'id': 1580541, 'coordinate':[108.334999, 15.87944]}, 
    {'Place': 'Quang Ngai', 'id': 1568770, 'coordinate':[108.800003, 15.11667]}, 
    {'Place': 'Quang Ninh', 'id': 1586357, 'coordinate':[107.300003, 21.01667]}, 
    {'Place': 'Quang Tri', 'id': 1582926, 'coordinate':[107.100311, 16.81625]}, 
    {'Place': 'Soc Trang', 'id': 1567788, 'coordinate':[105.980003, 9.60333]}, 
    {'Place': 'Son La', 'id': 1567681, 'coordinate':[103.900002, 21.316669]}, 
    {'Place': 'Tay Ninh', 'id': 1566559, 'coordinate':[106.099998, 11.3]}, 
    {'Place': 'Thai Binh', 'id': 1566346, 'coordinate':[106.333328, 20.450001]}, 
    {'Place': 'Thai Nguyen', 'id': 1566319, 'coordinate':[105.84417, 21.592779]}, 
    {'Place': 'Thanh Hoa', 'id': 1566166, 'coordinate':[105.76667, 19.799999]}, 
    {'Place': 'Ho Chi Minh city', 'id': 1566083, 'coordinate':[106.666672, 10.75]}, 
    {'Place': 'Thua Thien Hue', 'id': 1580240, 'coordinate':[107.599998, 16.466669]}, 
    {'Place': 'Tien Giang', 'id': 1574023, 'coordinate':[106.349998, 10.35]}, 
    {'Place': 'Tra Vinh', 'id': 1563926, 'coordinate':[106.345284, 9.93472]}, 
    {'Place': 'Tuyen Quang', 'id': 1563287, 'coordinate':[105.218063, 21.82333]},  
    {'Place': 'Vinh Long', 'id': 1562693, 'coordinate':[105.966667, 10.25]}, 
    {'Place': 'Vinh Phuc', 'id': 1562548, 'coordinate':[105.596672, 21.309999]}, 
    {'Place': 'Yen Bai', 'id': 1560349, 'coordinate':[104.866669, 21.700001]}, 
]
    # Testing
    connection_str = f'mongodb+srv://root:12345ADMIN@cluster0.5qjhz.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'

    # connection_str = 'mongodb://localhost:27017'
    # connection_str = 'mongodb://demeterdb:27017'

    client = pymongo.MongoClient(connection_str)

    db = client.get_database('demeter')
    if 'region_data' in db.list_collection_names():
        db.drop_collection('region_data')

    collection = db.get_collection('region_data')
    collection.create_index('Place')
    collection.insert_many(regions)
