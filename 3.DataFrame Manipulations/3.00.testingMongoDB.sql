
db.Studio.find().forEach(function (myDoc){
    var newFields = []
    for (let mediaKey in myDoc.media['edges']) {
        newFields.push({id:myDoc["media"]['edges'][mediaKey]["node"]["id"]})
    }
    db.Studio.updateOne(
        {_id : myDoc._id},
        {"$set": {"fields" : newFields} }
    )
})

db.Studio.find()


db.Studio.updateMany({},{
    "$unset":{"fields":""}
})

db.Character.find({
    age:{
        $lt:"27"
    }
})

db.getCollection("CharactersTranspose").updateMany({"dateOfBirth.day": 9}, {
    "$set": {
        age : new NumberInt("26"),
        fewa: new Boolean("false"),
        dateOfBirth: {
            "month": new NumberInt("9"),
            "day": new NumberInt("9")
        }
    }
})


