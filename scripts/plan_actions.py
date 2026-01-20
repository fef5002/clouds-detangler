"""Plan dedupe / tidy actions (scaffold).

Eventually this script will:

- Connect to the dedupe index (e.g. DuckDB)
- Identify files with the same content hash across clouds
- Decide, based on simple rules, which copy to treat as canonical
- Produce an actions_plan.csv with columns like:
    remote, path, hash, action, target

For now it is just a placeholder.
"""

def main():
    print("plan_actions.py is a placeholder for now.")
    print("Once the index is built, this script will generate an actions_plan.csv")

if __name__ == "__main__":
    main()
