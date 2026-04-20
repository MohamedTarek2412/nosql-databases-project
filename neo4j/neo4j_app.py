"""
╔══════════════════════════════════════════════════════════════════╗
║         Neo4j Task - Complete Professional Solution              ║
║         Dataset: Movie Graph (Neo4j Official Built-in Dataset)   ║
║         Source : https://github.com/neo4j-graph-examples/movies  ║
║                                                                  ║
║  Nodes        : Person, Movie                                    ║
║  Relationships: ACTED_IN, DIRECTED, PRODUCED, WROTE, REVIEWED   ║
╚══════════════════════════════════════════════════════════════════╝
"""

from neo4j import GraphDatabase
import sys
import os
URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
# ─────────────────────────────────────────────
# CONNECTION SETUP
# ─────────────────────────────────────────────
USER     = "neo4j"
PASSWORD = "password"   


class Neo4jMovieSolution:

    def __init__(self):
        self.driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
        print("✅ Connected to Neo4j successfully!")

    def close(self):
        self.driver.close()

    def run(self, query, **params):
        with self.driver.session() as session:
            return list(session.run(query, **params))

    # ══════════════════════════════════════════════════
    # TASK 1: Create the Graph (Nodes + Relationships + Properties)
    # Dataset: Neo4j Official Movie Graph
    # ══════════════════════════════════════════════════
    def task1_create_graph(self):
        print("\n" + "═"*60)
        print("📌 TASK 1: Creating the Movie Graph")
        print("   Dataset: Neo4j Official Movie Graph Dataset")
        print("   Source : https://github.com/neo4j-graph-examples/movies")
        print("═"*60)

        # Clear existing data
        self.run("MATCH (n) DETACH DELETE n")
        print("   🧹 Cleared existing data\n")

        # ── Create Movie Nodes ──
        self.run("""
            CREATE
              (:Movie {title: 'The Matrix',        released: 1999, tagline: 'Welcome to the Real World'}),
              (:Movie {title: 'The Matrix Reloaded',released: 2003, tagline: 'Free your mind'}),
              (:Movie {title: 'The Matrix Revolutions', released: 2003, tagline: 'Everything that has a beginning has an end'}),
              (:Movie {title: 'The Devil s Advocate', released: 1997, tagline: 'Evil has its winning ways'}),
              (:Movie {title: 'A Few Good Men',    released: 1992, tagline: 'In the heart of the nation s capital'}),
              (:Movie {title: 'Top Gun',           released: 1986, tagline: 'I feel the need, the need for speed'}),
              (:Movie {title: 'Jerry Maguire',     released: 2000, tagline: 'The rest of his life begins now'}),
              (:Movie {title: 'Cast Away',         released: 2000, tagline: 'At the edge of the world, his journey begins'}),
              (:Movie {title: 'Cloud Atlas',       released: 2012, tagline: 'Everything is connected'}),
              (:Movie {title: 'Speed Racer',       released: 2008, tagline: 'Speed has no limits'})
        """)
        print("   ✅ Created 10 Movie nodes")

        # ── Create Person Nodes ──
        self.run("""
            CREATE
              (:Person {name: 'Keanu Reeves',    born: 1964}),
              (:Person {name: 'Carrie-Anne Moss', born: 1967}),
              (:Person {name: 'Laurence Fishburne', born: 1961}),
              (:Person {name: 'Hugo Weaving',    born: 1960}),
              (:Person {name: 'Lilly Wachowski', born: 1967}),
              (:Person {name: 'Lana Wachowski',  born: 1965}),
              (:Person {name: 'Joel Silver',     born: 1952}),
              (:Person {name: 'Tom Hanks',       born: 1956}),
              (:Person {name: 'Tom Cruise',      born: 1962}),
              (:Person {name: 'Jack Nicholson',  born: 1937}),
              (:Person {name: 'Demi Moore',      born: 1962}),
              (:Person {name: 'Kevin Bacon',     born: 1958}),
              (:Person {name: 'Kiefer Sutherland',born: 1966}),
              (:Person {name: 'Al Pacino',       born: 1940}),
              (:Person {name: 'Taylor Hackford', born: 1944}),
              (:Person {name: 'Rob Reiner',      born: 1945}),
              (:Person {name: 'Tony Scott',      born: 1944}),
              (:Person {name: 'Val Kilmer',      born: 1959}),
              (:Person {name: 'Cameron Crowe',   born: 1957}),
              (:Person {name: 'Robert Zemeckis', born: 1951}),
              (:Person {name: 'Tom Tykwer',      born: 1965}),
              (:Person {name: 'Halle Berry',     born: 1966}),
              (:Person {name: 'Jim Broadbent',   born: 1949}),
              (:Person {name: 'Emile Hirsch',    born: 1985})
        """)
        print("   ✅ Created 24 Person nodes")

        # ── ACTED_IN Relationships ──
        acted_in = [
            ("Keanu Reeves",     "The Matrix",              "Neo",     "['The Matrix']"),
            ("Carrie-Anne Moss", "The Matrix",              "Trinity", "['The Matrix']"),
            ("Laurence Fishburne","The Matrix",             "Morpheus","['The Matrix']"),
            ("Hugo Weaving",     "The Matrix",              "Agent Smith","['The Matrix']"),
            ("Keanu Reeves",     "The Matrix Reloaded",     "Neo",     "['The Matrix Reloaded']"),
            ("Carrie-Anne Moss", "The Matrix Reloaded",     "Trinity", "['The Matrix Reloaded']"),
            ("Laurence Fishburne","The Matrix Reloaded",    "Morpheus","['The Matrix Reloaded']"),
            ("Hugo Weaving",     "The Matrix Revolutions",  "Agent Smith","['The Matrix Revolutions']"),
            ("Keanu Reeves",     "The Matrix Revolutions",  "Neo",     "['The Matrix Revolutions']"),
            ("Keanu Reeves",     "The Devil s Advocate",    "Kevin Lomax","['The Devil s Advocate']"),
            ("Al Pacino",        "The Devil s Advocate",    "John Milton","['The Devil s Advocate']"),
            ("Tom Cruise",       "A Few Good Men",          "Lt. Daniel Kaffee","['A Few Good Men']"),
            ("Jack Nicholson",   "A Few Good Men",          "Col. Nathan R. Jessup","['A Few Good Men']"),
            ("Demi Moore",       "A Few Good Men",          "Lt. Cdr. JoAnne Galloway","['A Few Good Men']"),
            ("Kevin Bacon",      "A Few Good Men",          "Capt. Jack Ross","['A Few Good Men']"),
            ("Kiefer Sutherland","A Few Good Men",          "Lt. Jonathan Kendrick","['A Few Good Men']"),
            ("Tom Cruise",       "Top Gun",                 "Maverick","['Top Gun']"),
            ("Val Kilmer",       "Top Gun",                 "Ice Man", "['Top Gun']"),
            ("Tom Cruise",       "Jerry Maguire",           "Jerry Maguire","['Jerry Maguire']"),
            ("Tom Hanks",        "Cast Away",               "Chuck Noland","['Cast Away']"),
            ("Tom Hanks",        "Cloud Atlas",             "Zachry",  "['Cloud Atlas']"),
            ("Halle Berry",      "Cloud Atlas",             "Luisa Rey","['Cloud Atlas']"),
            ("Jim Broadbent",    "Cloud Atlas",             "Timothy Cavendish","['Cloud Atlas']"),
            ("Emile Hirsch",     "Speed Racer",             "Speed Racer","['Speed Racer']"),
        ]

        for person, movie, role, roles in acted_in:
            self.run("""
                MATCH (p:Person {name: $person}), (m:Movie {title: $movie})
                CREATE (p)-[:ACTED_IN {roles: $role, earnings: $roles}]->(m)
            """, person=person, movie=movie, role=role, roles=roles)
        print(f"   ✅ Created {len(acted_in)} ACTED_IN relationships")

        # ── DIRECTED Relationships ──
        directed = [
            ("Lilly Wachowski", "The Matrix"),
            ("Lana Wachowski",  "The Matrix"),
            ("Lilly Wachowski", "The Matrix Reloaded"),
            ("Lana Wachowski",  "The Matrix Reloaded"),
            ("Lilly Wachowski", "The Matrix Revolutions"),
            ("Lana Wachowski",  "The Matrix Revolutions"),
            ("Lilly Wachowski", "Speed Racer"),
            ("Lana Wachowski",  "Speed Racer"),
            ("Lilly Wachowski", "Cloud Atlas"),
            ("Lana Wachowski",  "Cloud Atlas"),
            ("Tom Tykwer",      "Cloud Atlas"),
            ("Taylor Hackford", "The Devil s Advocate"),
            ("Rob Reiner",      "A Few Good Men"),
            ("Tony Scott",      "Top Gun"),
            ("Cameron Crowe",   "Jerry Maguire"),
            ("Robert Zemeckis", "Cast Away"),
        ]

        for person, movie in directed:
            self.run("""
                MATCH (p:Person {name: $person}), (m:Movie {title: $movie})
                CREATE (p)-[:DIRECTED]->(m)
            """, person=person, movie=movie)
        print(f"   ✅ Created {len(directed)} DIRECTED relationships")

        # ── PRODUCED Relationships ──
        produced = [
            ("Joel Silver", "The Matrix"),
            ("Joel Silver", "The Matrix Reloaded"),
            ("Joel Silver", "The Matrix Revolutions"),
        ]
        for person, movie in produced:
            self.run("""
                MATCH (p:Person {name: $person}), (m:Movie {title: $movie})
                CREATE (p)-[:PRODUCED {role: 'Executive Producer'}]->(m)
            """, person=person, movie=movie)
        print(f"   ✅ Created {len(produced)} PRODUCED relationships")

        # ── WROTE Relationships ──
        wrote = [
            ("Lilly Wachowski", "The Matrix"),
            ("Lana Wachowski",  "The Matrix"),
            ("Lilly Wachowski", "The Matrix Reloaded"),
            ("Lana Wachowski",  "The Matrix Reloaded"),
            ("Cameron Crowe",   "Jerry Maguire"),
        ]
        for person, movie in wrote:
            self.run("""
                MATCH (p:Person {name: $person}), (m:Movie {title: $movie})
                CREATE (p)-[:WROTE]->(m)
            """, person=person, movie=movie)
        print(f"   ✅ Created {len(wrote)} WROTE relationships")

        # ── REVIEWED Relationships ──
        reviews = [
            ("Kevin Bacon",  "The Matrix",    "Impressive sci-fi masterpiece", 95),
            ("Demi Moore",   "Top Gun",        "Classic action film",           85),
            ("Val Kilmer",   "Jerry Maguire",  "Heartfelt and funny",           80),
            ("Jim Broadbent","Cast Away",      "Powerful performance by Hanks", 90),
        ]
        for person, movie, summary, rating in reviews:
            self.run("""
                MATCH (p:Person {name: $person}), (m:Movie {title: $movie})
                CREATE (p)-[:REVIEWED {summary: $summary, rating: $rating}]->(m)
            """, person=person, movie=movie, summary=summary, rating=rating)
        print(f"   ✅ Created {len(reviews)} REVIEWED relationships")

        print("\n   📊 Graph created successfully!")
        print("   Nodes  : Person (24) + Movie (10) = 34 total")
        print("   Rels   : ACTED_IN + DIRECTED + PRODUCED + WROTE + REVIEWED")


    # ══════════════════════════════════════════════════
    # TASK 2: Delete Nodes, Relationships, and Properties
    # ══════════════════════════════════════════════════
    def task2_delete(self):
        print("\n" + "═"*60)
        print("📌 TASK 2: Deleting Nodes, Relationships & Properties")
        print("═"*60)

        # 2a – Delete a specific ACTED_IN relationship
        self.run("""
            MATCH (:Person {name: 'Val Kilmer'})-[r:ACTED_IN]->(:Movie {title: 'Top Gun'})
            DELETE r
        """)
        print("   ✅ Deleted ACTED_IN relationship: Val Kilmer → Top Gun")

        # 2b – Delete a REVIEWED relationship
        self.run("""
            MATCH (:Person {name: 'Demi Moore'})-[r:REVIEWED]->(:Movie {title: 'Top Gun'})
            DELETE r
        """)
        print("   ✅ Deleted REVIEWED relationship: Demi Moore → Top Gun")

        # 2c – Remove a property from a Movie node
        self.run("""
            MATCH (m:Movie {title: 'Speed Racer'})
            REMOVE m.tagline
        """)
        print("   ✅ Removed 'tagline' property from Movie: Speed Racer")

        # 2d – Remove a property from a Person node
        self.run("""
            MATCH (p:Person {name: 'Tony Scott'})
            REMOVE p.born
        """)
        print("   ✅ Removed 'born' property from Person: Tony Scott")

        # 2e – Delete a node with all its relationships (DETACH DELETE)
        self.run("""
            MATCH (p:Person {name: 'Kiefer Sutherland'})
            DETACH DELETE p
        """)
        print("   ✅ Deleted Person node + all relationships: Kiefer Sutherland")

        # Verify
        result = self.run("MATCH (n) RETURN COUNT(n) AS total")
        print(f"\n   📊 Remaining nodes after deletions: {result[0]['total']}")


    # ══════════════════════════════════════════════════
    # TASK 3: Update Properties of Nodes and Relationships
    # ══════════════════════════════════════════════════
    def task3_update(self):
        print("\n" + "═"*60)
        print("📌 TASK 3: Updating Node & Relationship Properties")
        print("═"*60)

        # 3a – Update Movie tagline and add a new property
        self.run("""
            MATCH (m:Movie {title: 'The Matrix'})
            SET m.tagline   = 'Welcome to the Real World — Updated',
                m.genre     = 'Sci-Fi',
                m.box_office = 463517383,
                m.updated    = '2024-01-01'
        """)
        print("   ✅ Updated Movie 'The Matrix': added genre, box_office, updated tagline")

        # 3b – Update Person born year and add rating
        self.run("""
            MATCH (p:Person {name: 'Keanu Reeves'})
            SET p.born        = 1964,
                p.nationality = 'Canadian',
                p.popularity  = 9.5
        """)
        print("   ✅ Updated Person 'Keanu Reeves': added nationality, popularity")

        # 3c – Update ACTED_IN relationship property
        self.run("""
            MATCH (:Person {name: 'Keanu Reeves'})-[r:ACTED_IN]->(:Movie {title: 'The Matrix'})
            SET r.roles    = 'Neo / The One',
                r.award     = 'MTV Movie Award',
                r.fee        = 10000000
        """)
        print("   ✅ Updated ACTED_IN relationship: Keanu → The Matrix (added award, fee)")

        # 3d – Update REVIEWED relationship
        self.run("""
            MATCH (:Person {name: 'Kevin Bacon'})-[r:REVIEWED]->(:Movie {title: 'The Matrix'})
            SET r.rating  = 98,
                r.summary = 'One of the greatest sci-fi films ever made — Updated Review'
        """)
        print("   ✅ Updated REVIEWED relationship: Kevin Bacon → The Matrix (rating=98)")

        # 3e – Bulk update: add 'era' property to all movies released before 2000
        self.run("""
            MATCH (m:Movie)
            WHERE m.released < 2000
            SET m.era = 'Classic'
        """)
        print("   ✅ Bulk updated: added era='Classic' to all Movies released before 2000")

        # 3f – Bulk update: add 'generation' to Person nodes born before 1960
        self.run("""
            MATCH (p:Person)
            WHERE p.born < 1960
            SET p.generation = 'Veteran'
        """)
        print("   ✅ Bulk updated: added generation='Veteran' to persons born before 1960")


    # ══════════════════════════════════════════════════
    # TASK 4: Find Nodes Based on Conditions
    # ══════════════════════════════════════════════════
    def task4_find_nodes(self):
        print("\n" + "═"*60)
        print("📌 TASK 4: Finding Nodes Based on Conditions")
        print("═"*60)

        # 4a – Movies released after 2000
        print("\n   🔍 4a) Movies released after year 2000:")
        rows = self.run("""
            MATCH (m:Movie)
            WHERE m.released > 2000
            RETURN m.title AS title, m.released AS year
            ORDER BY m.released ASC
        """)
        for r in rows:
            print(f"      🎬 {r['title']:<35} ({r['year']})")

        # 4b – Persons born in the 1960s
        print("\n   🔍 4b) Persons born in the 1960s (1960–1969):")
        rows = self.run("""
            MATCH (p:Person)
            WHERE p.born >= 1960 AND p.born <= 1969
            RETURN p.name AS name, p.born AS born
            ORDER BY p.born
        """)
        for r in rows:
            print(f"      👤 {r['name']:<25} Born: {r['born']}")

        # 4c – Movies with tagline containing 'World' or 'mind'
        print("\n   🔍 4c) Movies whose tagline contains 'World' or 'free':")
        rows = self.run("""
            MATCH (m:Movie)
            WHERE toLower(m.tagline) CONTAINS 'world'
               OR toLower(m.tagline) CONTAINS 'free'
            RETURN m.title AS title, m.tagline AS tagline
        """)
        for r in rows:
            print(f"      🎬 {r['title']:<30} | \"{r['tagline']}\"")

        # 4d – Persons who acted in more than 1 movie
        print("\n   🔍 4d) Persons who acted in more than 1 movie:")
        rows = self.run("""
            MATCH (p:Person)-[:ACTED_IN]->(m:Movie)
            WITH p, COUNT(m) AS movieCount
            WHERE movieCount > 1
            RETURN p.name AS name, movieCount
            ORDER BY movieCount DESC
        """)
        for r in rows:
            print(f"      🌟 {r['name']:<25} → Acted in {r['movieCount']} movies")

        # 4e – All Movie nodes with era = 'Classic'
        print("\n   🔍 4e) Movies with era = 'Classic' (released before 2000):")
        rows = self.run("""
            MATCH (m:Movie {era: 'Classic'})
            RETURN m.title AS title, m.released AS year, m.era AS era
        """)
        for r in rows:
            print(f"      🏛️  {r['title']:<30} ({r['year']}) — Era: {r['era']}")


    # ══════════════════════════════════════════════════
    # TASK 5: Find Relationships Based on Conditions
    # ══════════════════════════════════════════════════
    def task5_find_relationships(self):
        print("\n" + "═"*60)
        print("📌 TASK 5: Finding Relationships Based on Conditions")
        print("═"*60)

        # 5a – REVIEWED relationships with rating > 85
        print("\n   🔍 5a) REVIEWED relationships with rating > 85:")
        rows = self.run("""
            MATCH (p:Person)-[r:REVIEWED]->(m:Movie)
            WHERE r.rating > 85
            RETURN p.name AS reviewer, m.title AS movie,
                   r.rating AS rating, r.summary AS summary
            ORDER BY r.rating DESC
        """)
        for r in rows:
            print(f"      ⭐ {r['reviewer']:<20} → {r['movie']:<25} | Rating: {r['rating']}")
            print(f"         Summary: \"{r['summary']}\"")

        # 5b – ACTED_IN relationships for The Matrix movies
        print("\n   🔍 5b) All actors in Matrix trilogy:")
        rows = self.run("""
            MATCH (p:Person)-[r:ACTED_IN]->(m:Movie)
            WHERE m.title STARTS WITH 'The Matrix'
            RETURN p.name AS actor, m.title AS movie, r.roles AS role
            ORDER BY m.title, p.name
        """)
        for r in rows:
            print(f"      🎭 {r['actor']:<25} → {r['movie']:<30} | Role: {r['role']}")

        # 5c – DIRECTED relationships (find all directors and their movies)
        print("\n   🔍 5c) All DIRECTED relationships:")
        rows = self.run("""
            MATCH (p:Person)-[:DIRECTED]->(m:Movie)
            RETURN p.name AS director, COLLECT(m.title) AS movies
            ORDER BY p.name
        """)
        for r in rows:
            print(f"      🎬 {r['director']:<25} directed → {r['movies']}")

        # 5d – Persons connected to 'Tom Hanks' through any relationship
        print("\n   🔍 5d) All movies connected to Tom Hanks (any relationship):")
        rows = self.run("""
            MATCH (p:Person {name: 'Tom Hanks'})-[r]->(m:Movie)
            RETURN type(r) AS relationship, m.title AS movie
        """)
        for r in rows:
            print(f"      🔗 Tom Hanks -[{r['relationship']}]-> {r['movie']}")

        # 5e – People who both acted in AND directed the same movie
        print("\n   🔍 5e) People who both ACTED_IN and DIRECTED same movie:")
        rows = self.run("""
            MATCH (p:Person)-[:ACTED_IN]->(m:Movie)<-[:DIRECTED]-(p)
            RETURN p.name AS person, m.title AS movie
        """)
        if rows:
            for r in rows:
                print(f"      🎭🎬 {r['person']} both acted & directed in {r['movie']}")
        else:
            print("      (No person both acted and directed the same movie in this dataset)")

        # 5f – Shortest path between two actors
        print("\n   🔍 5f) Shortest path: Keanu Reeves ↔ Tom Hanks:")
        rows = self.run("""
            MATCH path = shortestPath(
              (:Person {name: 'Keanu Reeves'})-[*..6]-(:Person {name: 'Tom Hanks'})
            )
            RETURN [node IN nodes(path) | 
                    CASE WHEN 'Movie' IN labels(node) THEN node.title
                         ELSE node.name END
                   ] AS path_names,
                   length(path) AS hops
        """)
        for r in rows:
            print(f"      🛣️  Path ({r['hops']} hops): {' → '.join(r['path_names'])}")


    # ══════════════════════════════════════════════════
    # GRAPH SUMMARY
    # ══════════════════════════════════════════════════
    def print_summary(self):
        print("\n" + "═"*60)
        print("📊 FINAL GRAPH SUMMARY")
        print("═"*60)

        nodes = self.run("MATCH (n) RETURN labels(n)[0] AS label, COUNT(n) AS count ORDER BY label")
        print("\n   Nodes:")
        for r in nodes:
            print(f"      [{r['label']:<10}] → {r['count']} nodes")

        rels = self.run("MATCH ()-[r]->() RETURN type(r) AS rel, COUNT(r) AS count ORDER BY rel")
        print("\n   Relationships:")
        for r in rels:
            print(f"      [{r['rel']:<15}] → {r['count']} relationships")

        total_nodes = self.run("MATCH (n) RETURN COUNT(n) AS c")[0]['c']
        total_rels  = self.run("MATCH ()-[r]->() RETURN COUNT(r) AS c")[0]['c']
        print(f"\n   TOTAL → {total_nodes} Nodes | {total_rels} Relationships")


# ─────────────────────────────────────────────
# MAIN RUNNER
# ─────────────────────────────────────────────
def main():
    print("╔" + "═"*58 + "╗")
    print("║     Neo4j Movie Graph — Complete Solution               ║")
    print("║     Dataset: Neo4j Official Movie Graph                 ║")
    print("╚" + "═"*58 + "╝")

    try:
        neo = Neo4jMovieSolution()

        neo.task1_create_graph()
        neo.task2_delete()
        neo.task3_update()
        neo.task4_find_nodes()
        neo.task5_find_relationships()
        neo.print_summary()

        print("\n" + "═"*60)
        print("🎉 ALL NEO4J TASKS COMPLETED SUCCESSFULLY!")
        print("═"*60 + "\n")

        neo.close()

    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("💡 Tips:")
        print("   1. Make sure Neo4j is running")
        print("   2. Update the PASSWORD variable at the top of this file")
        print("   3. Install driver: pip install neo4j")
        sys.exit(1)


if __name__ == "__main__":
    main()