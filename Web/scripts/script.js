var viz;

function draw() {
    var config = {
        container_id: "viz",
        server_url: "neo4j://104.198.183.32",
        server_user: "neo4j",
        server_password: "tSgiHA1DN9R98PeM",
        labels: {
            "Paper": {
                "caption": "id",
                "size": "pagerank",
                // "community": "community",
                // "title_properties": [
                //     "name",
                //     "pagerank"
                // ]
            }
        },
        relationships: {
            "CITED": {
                // "thickness": "weight",
                "caption": false
            }
        },
        initial_cypher: "MATCH ((n)-[c:CITED]->(m)) RETURN * LIMIT 500"
    };

    viz = new NeoVis.default(config);
    viz.render();
}