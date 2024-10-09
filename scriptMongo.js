// Map function
var mapFunction = function() {
    emit(this.nom_arrondissement_communes, 1);
};

// Reduce function
var reduceFunction = function(key, values) {
    return Array.sum(values);
};

// Execute mapReduce
var result = db.runCommand({
    mapReduce: "velo_libre_1728482647",
    map: mapFunction,
    reduce: reduceFunction,
    out: { inline: 1 }
});

// Sort and print results
result.results.sort(function(a, b) {
    return b.value - a.value;
});

result.results.forEach(function(doc) {
    print("Arrondissement: " + doc._id + ", Nombre de vélib disponible: " + doc.value);
});