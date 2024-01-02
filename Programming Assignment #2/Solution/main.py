import sys
from FindCitations import FindCitations
from FindCyclicReferences import FindCyclicReferences

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python main.py [COUNT|CYCLE] [1-10 workers] [filename]")
        sys.exit(1)

    task = sys.argv[1]
    workers = int(sys.argv[2])
    filename = sys.argv[3]

    if task == "COUNT":
        if workers < 1 or workers > 10:
            print("Number of workers should be between 1 and 10.")
            sys.exit(1)

        # Execute FindCitations task
        Find_Citations = FindCitations(workers)
        Find_Citations.start(filename)

    elif task == "CYCLE":
        if workers < 1 or workers > 10:
            print("Number of workers should be between 1 and 10.")
            sys.exit(1)

        # Execute FindCyclicReferences task
        Find_Cyclic_Refs = FindCyclicReferences(workers)
        Find_Cyclic_Refs.start(filename)

    else:
        print("Invalid task type. Use COUNT or CYCLE.")
        sys.exit(1)
    
