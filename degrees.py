import csv
import sys

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "small"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: "))
    #print(f"source: {source}")
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    #print(f"Target: {target}")    
    if target is None:
        sys.exit("Person not found.")
    

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    from util import Node, StackFrontier, QueueFrontier
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 

def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """
    # TODO
    # raise NotImplementedError

    # *******************************************************************************
      # Initialize frontier to just the starting position
    start = Node(source, None, None)
    frontier = QueueFrontier()
    frontier.add(start)
    # Initialise an empty explored - List of Actors to explored
    explored = set()
 
    # Loop until a solution is found, or Frontier is empty(no solution):
    while True:
      # Check the Frontier if it is empty
      if frontier.empty():
        print(f'The actors did now worked togeather in a movie')
        return None

      # Otherwise expand the next node in the Queue, add it to the explored states and get set of movies and actors for the actor in the current node:
      node_to_analyze = frontier.remove()
      explored.add(node_to_analyze.state)
      print(f"len(explored) = {len(explored)}")

      # action = movie id    and state = actor
      for action, state in neighbors_for_person(node_to_analyze.state):

        # If node_to_analyze.state containing the actor is the target actor, 
        # then the program found the solution, and path is returned
        if state == target:
          path = []
          print('Solution Found!')
          path.append((action, state))

          # Add action and state to path until back to start node
          while node_to_analyze.parent != None:
            path.append((node_to_analyze.action, node_to_analyze.state))
            node_to_analyze = node_to_analyze.parent

          path.reverse()
          return path

        #  Add neighbors to frontier
        if not frontier.contains_state(state) and state not in explored:
          new_node = Node(state=state, parent= node_to_analyze, action =action)
          frontier.add(new_node)
    # *******************************************************************************

def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    #print(neighbors)
    return neighbors


if __name__ == "__main__":
    main()
