from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import sys
import os
import time

# CONNECTION SETUP
def connect():
    host = os.getenv("CASSANDRA_HOST", "cassandra")

    for i in range(20):
        try:
            cluster = Cluster([host], port=9042)
            session = cluster.connect()
            print("Connected to Cassandra successfully!")
            return cluster, session
        except Exception as e:
            print(f"Cassandra not ready yet... retry {i+1}/20")
            time.sleep(5)

    raise Exception("Cassandra failed to start after retries")

# KEYSPACE SETUP
def setup_keyspace(session):
    session.execute("""
        CREATE KEYSPACE IF NOT EXISTS university_ks
        WITH replication = {
            'class': 'SimpleStrategy',
            'replication_factor': 1
        }
    """)
    session.set_keyspace('university_ks')
    print("✅ Keyspace 'university_ks' ready")

# PART 1 – TASK 1: Create Table with Composite Primary Key
def task1_create_table(session):
    print("\n" + "="*60)
    print("📌 TASK 1: Creating Table with Composite Primary Key")
    print("="*60)

    session.execute("DROP TABLE IF EXISTS exam_results")

    session.execute("""
        CREATE TABLE exam_results (
            department TEXT,
            student_id INT,
            student_name TEXT,
            course_name TEXT,
            score DOUBLE,
            PRIMARY KEY ((department), student_id)
        ) WITH CLUSTERING ORDER BY (student_id ASC)
    """)

    print(" Table 'exam_results' created")


# PART 1 – TASK 2: Insert 5+ Rows
def task2_insert_rows(session):
    print("\n" + "="*60)
    print("TASK 2: Inserting Rows")
    print("="*60)

    rows = [
        ("CS",   1, "Ahmed Hassan",   "Database Systems",  92.5),
        ("CS",   2, "Sara Mohamed",   "Data Structures",   87.0),
        ("CS",   3, "Omar Khaled",    "Algorithms",        78.5),
        ("IT",   4, "Nour Ali",       "Web Development",   95.0),
        ("IT",   5, "Youssef Tarek",  "Networking",        82.0),
        ("Math", 6, "Layla Ibrahim",  "Linear Algebra",    88.5),
        ("Math", 7, "Karim Mostafa",  "Calculus",          74.0),
    ]

    insert_stmt = session.prepare("""
        INSERT INTO exam_results (department, student_id, student_name, course_name, score)
        VALUES (?, ?, ?, ?, ?)
    """)

    for row in rows:
        session.execute(insert_stmt, row)

    print(f" Inserted {len(rows)} rows into 'exam_results'")
    print("\n   Current Data:")
    print(f"   {'Dept':<8} {'ID':<5} {'Name':<20} {'Course':<22} {'Score'}")
    print("   " + "-"*65)
    results = session.execute("SELECT * FROM exam_results")
    for r in results:
        print(f"   {r.department:<8} {r.student_id:<5} {r.student_name:<20} {r.course_name:<22} {r.score}")

# PART 1 – TASK 3: Update a Column Value
def task3_update(session):
    print("\n" + "="*60)
    print("TASK 3: Updating a Column Value")
    print("="*60)

    # Update Ahmed Hassan's score
    session.execute("""
        UPDATE exam_results
        SET score = 98.0
        WHERE department = 'CS' AND student_id = 1
    """)
    print("Updated score of Ahmed Hassan (CS, id=1) → 98.0")

    # Update Nour Ali's course name
    session.execute("""
        UPDATE exam_results
        SET course_name = 'Advanced Web Development'
        WHERE department = 'IT' AND student_id = 4
    """)
    print("Updated course_name of Nour Ali (IT, id=4) → 'Advanced Web Development'")

    # Verify
    row = session.execute(
        "SELECT * FROM exam_results WHERE department='CS' AND student_id=1"
    ).one()
    print(f"\n   Verified: {row.student_name} new score = {row.score}")

# PART 1 – TASK 4: Delete a Row
def task4_delete(session):
    print("\n" + "="*60)
    print("TASK 4: Deleting a Row")
    print("="*60)

    session.execute("""
        DELETE FROM exam_results
        WHERE department = 'Math' AND student_id = 7
    """)
    print("Deleted row: Karim Mostafa (Math, id=7)")

    count = session.execute(
        "SELECT COUNT(*) FROM exam_results WHERE department='Math'"
    ).one()[0]
    print(f"    Remaining rows in Math dept: {count}")

# PART 2 – Shell Instructions
def part2_shell_instructions():
    print("\n" + "="*60)
    print(" PART 2 – Shell Commands (Run in cqlsh)")
    print("="*60)

    print("""
   ── Connect to Cassandra shell ──
   $ cqlsh
   > USE university_ks;

   ────────────────────────────────────────────────
   TASK 1: SELECT in DESCENDING ORDER by partition key
   ────────────────────────────────────────────────
   SELECT * FROM exam_results
   WHERE department = 'CS'
   ORDER BY student_id DESC;

   -- Note: ORDER BY in Cassandra applies within a partition.
   -- To query descending, table should be created with:
   -- WITH CLUSTERING ORDER BY (student_id DESC)
   -- OR use the reversed syntax above per partition.

   ────────────────────────────────────────────────
   TASK 2: CREATE MATERIALIZED VIEW
   (Query by 'score' — not part of primary key)
   ────────────────────────────────────────────────
   CREATE MATERIALIZED VIEW exam_by_score AS
     SELECT department, student_id, student_name, course_name, score
     FROM exam_results
     WHERE score IS NOT NULL
       AND department IS NOT NULL
       AND student_id IS NOT NULL
     PRIMARY KEY (score, department, student_id);

   -- Query the materialized view:
   SELECT * FROM exam_by_score WHERE score = 98.0;
   SELECT * FROM exam_by_score;
""")

# MAIN RUNNER
def main():
    try:
        cluster, session = connect()
        setup_keyspace(session)
        task1_create_table(session)
        task2_insert_rows(session)
        task3_update(session)
        task4_delete(session)
        part2_shell_instructions()
        print("\n" + "="*60)
        print("ALL CASSANDRA TASKS COMPLETED SUCCESSFULLY!")
        print("="*60 + "\n")
        cluster.shutdown()
    except Exception as e:
        print(f"\nError: {e}")
        print("Make sure Cassandra is running: sudo systemctl start cassandra")
        sys.exit(1)

if __name__ == "__main__":
    main()