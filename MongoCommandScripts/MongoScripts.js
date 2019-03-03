//db.getCollection("wiltshire_street").find({})

db.getCollection("wiltshire_street").find({"properties.crime_type": "Vehicle crime"})

db.getCollection("cumbria").find({"properties.crime_date": '2017-02'})
