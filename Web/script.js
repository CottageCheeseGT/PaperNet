var viz;

function draw() {
    var config = {
        container_id: "viz",
        server_url: "neo4j://104.198.183.32",
        server_user: "neo4j",
        server_password: "tSgiHA1DN9R98PeM",
        // labels: {
        //     "Character": {
        //         "caption": "name",
        //         "size": "pagerank",
        //         "community": "community",
        //         "title_properties": [
        //             "name",
        //             "pagerank"
        //         ]
        //     }
        // },
        // relationships: {
        //     "INTERACTS": {
        //         "thickness": "weight",
        //         "caption": false
        //     }
        // },
        initial_cypher: "MATCH (n) RETURN n"
    };

    viz = new NeoVis.default(config);
    viz.render();
}