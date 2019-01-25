//db.getCollection("wiltshire_street").find({})

db.getCollection("wiltshire_street").find({"properties.crime_type": "Vehicle crime"})
