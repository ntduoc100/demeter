'''
Create region_data collection
'''
import pymongo

if __name__=='__main__':

    regions = [
    {'Place': 'An Giang', 'id': 'VN.AG', 'coordinate':[105.166672, 10.5]}, 
    {'Place': 'Ba Ria – Vung Tau', 'id': 'VN.BV', 'coordinate':[107.25, 10.58333]}, 
    {'Place': 'Bac Lieu', 'id': 'VN.BL', 'coordinate':[105.724442, 9.285]}, 
    {'Place': 'Bac Giang', 'id': 'VN.BG', 'coordinate':[106.199997, 21.26667]}, 
    {'Place': 'Bac Kan', 'id': 'VN.307', 'coordinate':[105.833328, 22.16667]}, 
    {'Place': 'Bac Ninh', 'id': 'VN.BN', 'coordinate':[106.050003, 21.183331]}, 
    {'Place': 'Ben Tre', 'id': 'VN.BR', 'coordinate':[106.383331, 10.23333]}, 
    {'Place': 'Binh Duong', 'id': 'VN.BI', 'coordinate':[106.666672, 11.16667]}, 
    {'Place': 'Binh Dinh', 'id': 'VN.BD', 'coordinate':[109.0, 14.16667]}, 
    {'Place': 'Binh Phuoc', 'id': 'VN.BP', 'coordinate':[106.916672, 11.75]}, 
    {'Place': 'Binh Thuan', 'id': 'VN.BU', 'coordinate':[108.0, 11.08333]}, 
    {'Place': 'Ca Mau', 'id': 'VN.CM', 'coordinate':[105.150002, 9.17694]}, 
    {'Place': 'Cao Bang', 'id': 'VN.CB', 'coordinate':[106.25, 22.66667]}, 
    {'Place': 'Can Tho', 'id': 'VN.333', 'coordinate':[105.783333, 10.03333]}, 
    {'Place': 'Da Nang', 'id': 'VN.DA', 'coordinate':[108.220833, 16.06778]}, 
    {'Place': 'Dak Lak', 'id': 'VN.723', 'coordinate':[108.166672, 12.83333]}, 
    {'Place': 'Dak Nong', 'id': 'VN.6365', 'coordinate':[108.050003, 12.66667]}, 
    {'Place': 'Dien Bien', 'id': 'VN.DB', 'coordinate':[103.01667, 21.383329]}, 
    {'Place': 'Dong Nai', 'id': 'VN.331', 'coordinate':[106.816673, 10.95]}, 
    {'Place': 'Dong Thap', 'id': 'VN.DT', 'coordinate':[105.633331, 10.45]}, 
    {'Place': 'Gia Lai', 'id': 'VN.724', 'coordinate':[108.25, 13.75]}, 
    {'Place': 'Ha Giang', 'id': 'VN.HG', 'coordinate':[104.98333, 22.83333]}, 
    {'Place': 'Ha Nam', 'id': 'VN.HM', 'coordinate':[106.0, 20.58333]}, 
    {'Place': 'Hanoi', 'id': 'VN.318', 'coordinate':[105.883331, 21.116671]}, 
    {'Place': 'Ha Tinh', 'id': 'VN.328', 'coordinate':[105.75, 18.33333]}, 
    {'Place': 'Hai Duong', 'id': 'VN.HD', 'coordinate':[106.333328, 20.91667]}, 
    {'Place': 'Hai Phong', 'id': 'VN.3623', 'coordinate':[106.68222, 20.85611]}, 
    {'Place': 'Hau Giang', 'id': 'VN.337', 'coordinate':[105.783333, 10.03333]}, 
    {'Place': 'Hoa Binh', 'id': 'VN.HO', 'coordinate':[105.338333, 20.81333]}, 
    {'Place': 'Hung Yen', 'id': 'VN.317', 'coordinate':[106.066673, 20.65]}, 
    {'Place': 'Khanh Hoa', 'id': 'VN.KH', 'coordinate':[109.159126, 11.92144]}, 
    {'Place': 'Kien Giang', 'id': 'VN.KG', 'coordinate':[105.166672, 10.0]}, 
    {'Place': 'Kon Tum', 'id': 'VN.299', 'coordinate':[107.916672, 14.75]}, 
    {'Place': 'Lai Chau', 'id': 'VN.LI', 'coordinate':[103.349998, 22.533331]}, 
    {'Place': 'Lang Son', 'id': 'VN.LS', 'coordinate':[106.73333, 21.83333]}, 
    {'Place': 'Lao Cai', 'id': 'VN.LO', 'coordinate':[103.949997, 22.48333]}, 
    {'Place': 'Lam Dong', 'id': 'VN.LD', 'coordinate':[108.441933, 11.94646]}, 
    {'Place': 'Long An', 'id': 'VN.LA', 'coordinate':[106.166672, 10.66667]}, 
    {'Place': 'Nam Dinh', 'id': 'VN.ND', 'coordinate':[106.166672, 20.41667]}, 
    {'Place': 'Nghe An', 'id': 'VN.NA', 'coordinate':[105.666672, 18.66667]}, 
    {'Place': 'Ninh Binh', 'id': 'VN.NB', 'coordinate':[105.974998, 20.253889]}, 
    {'Place': 'Ninh Thuan', 'id': 'VN.NT', 'coordinate':[108.833328, 11.75]}, 
    {'Place': 'Phu Tho', 'id': 'VN.PT', 'coordinate':[105.22702, 21.39883]}, 
    {'Place': 'Phu Yen', 'id': 'VN.PY', 'coordinate':[109.300003, 13.08333]}, 
    {'Place': 'Quang Binh', 'id': 'VN.QB', 'coordinate':[106.599998, 17.48333]}, 
    {'Place': 'Quang Nam', 'id': 'VN.300', 'coordinate':[108.334999, 15.87944]}, 
    {'Place': 'Quang Ngai', 'id': 'VN.QG', 'coordinate':[108.800003, 15.11667]}, 
    {'Place': 'Quang Ninh', 'id': 'VN.QN', 'coordinate':[107.300003, 21.01667]}, 
    {'Place': 'Quang Tri', 'id': 'VN.QT', 'coordinate':[107.100311, 16.81625]}, 
    {'Place': 'Soc Trang', 'id': 'VN.ST', 'coordinate':[105.980003, 9.60333]}, 
    {'Place': 'Son La', 'id': 'VN.311', 'coordinate':[103.900002, 21.316669]}, 
    {'Place': 'Tay Ninh', 'id': 'VN.TN', 'coordinate':[106.099998, 11.3]}, 
    {'Place': 'Thai Binh', 'id': 'VN.TB', 'coordinate':[106.333328, 20.450001]}, 
    {'Place': 'Thai Nguyen', 'id': 'VN.TY', 'coordinate':[105.84417, 21.592779]}, 
    {'Place': 'Thanh Hoa', 'id': 'VN.TH', 'coordinate':[105.76667, 19.799999]}, 
    {'Place': 'Ho Chi Minh city', 'id': 'VN.HC', 'coordinate':[106.666672, 10.75]}, 
    {'Place': 'Thua Thien Hue', 'id': 'VN.TT', 'coordinate':[107.599998, 16.466669]}, 
    {'Place': 'Tien Giang', 'id': 'VN.TG', 'coordinate':[106.349998, 10.35]}, 
    {'Place': 'Tra Vinh', 'id': 'VN.TV', 'coordinate':[106.345284, 9.93472]}, 
    {'Place': 'Tuyen Quang', 'id': 'VN.TQ', 'coordinate':[105.218063, 21.82333]},  
    {'Place': 'Vinh Long', 'id': 'VN.VL', 'coordinate':[105.966667, 10.25]}, 
    {'Place': 'Vinh Phuc', 'id': 'VN.VC', 'coordinate':[105.596672, 21.309999]}, 
    {'Place': 'Yen Bai', 'id': 'VN.YB', 'coordinate':[104.866669, 21.700001]}, 
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
