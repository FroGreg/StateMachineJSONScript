import glob, os, typing, json

def GetJSONFiles() -> list:
  currentDir: str = os.path.dirname(os.path.abspath(__file__))
  filePaths = glob.glob(currentDir + "/*.json")
  files: list = []
  openFile: str = ""

  print("Existing files: ")
  for file in filePaths:
      # Cut out the path to the file and then cut off the .json file format from its name.
      files.append(
        file.split('\\')[-1]
        .split(".json")[0]
      )
  for file in files:
      print("- \"" + file + "\"")
  return files

def GetJSONFromFile(t_fileName: str, t_fileList: list[str]) -> dict:

  
  char: str = ""
  fileNameJSON = t_fileName + ".json"
  defaultJSON: dict = {"states": {}, "startstate": "", "endstates": []}
  if(t_fileName not in t_fileList):
    print(f"{fileNameJSON} successfully created.")
    newFile = open(fileNameJSON, "w+")
    newFile.write(json.dumps(defaultJSON))
    newFile.close()
    

    return defaultJSON
  char = input(f"{fileNameJSON} already exists, do you want to (e)dit or (o)verwrite the existing file: ")
  while(char != "e" and char != "o"):
    char = input().lower()
  if(char == "e"):
    returnDict: dict = defaultJSON
    file = open(fileNameJSON, "r+")
    try:
      returnDict = json.loads(file.read())
      if(not ValidateStateMachineJSON(returnDict)):
        raise Exception()
      file.close()
    except:
      file.close()
      print("The file content is not valid StateMachine JSON.")
      exitCheck = input("Do you want to leave the file as is and (e)xit or (w)ipe the its' content and continue with it?")
      if(exitCheck.lower() == "e"):
          exit()
      elif(exitCheck.lower() == "w"):
        # Discard current content and wipe it
        file = open(fileNameJSON, "w")
        file.write(json.dumps(defaultJSON))
        file.close()
        print(f"{t_fileName} wiped.")
        return defaultJSON
    return returnDict
  else:
    # Discard current content and wipe it
    file = open(fileNameJSON, "w")
    file.write(json.dumps(defaultJSON))
    file.close()
    print(f"{t_fileName} wiped.")
    return defaultJSON
  
def SaveJSONToFile(t_fileName: str, t_JSON: dict) -> bool:
  if not (ValidateStateMachineJSON(t_JSON)):
    print("\nThe resulting JSON object is not a valid state anymore, do you want to go back and fix it or throw away the changes?")
    exit_check: str = ""
    while(exit_check not in ["y", "n"]):
      exit_check = input("Go back and fix the changes (no = throw away made changes)? [y/n]").lower()
    if(exit_check == "n"):
      print("Changes have been discarded.")
      return True
    return False
  with open(t_fileName + ".json", "w") as file:
    file.write(json.dumps(t_JSON))
    print(f"{t_fileName}.json saved.")
    return True

def ValidateStateMachineJSON(t_JSON: dict) -> bool:
  '''
  Checks if a given dictionary is a valid representation of a StateMachine object.

    A valid StateMachine JSON object:
      - Has 3 keys: states, startstate, endstates

        -> states: dict of lists representing the states of the machine, the key is the name of the state and the list represents the destinations of the transitions to other states.
           Each entry in the list must be a key in "states"
        
        -> startstate: a single string representing the start state of the machine, must be a key in "states".

        -> endstates: a list of strings denoting which states are considered end states, each entry must be a key in "states".
      

    Valid structure example of the JSON string:

    {
    
      "states":{
      
        "State 1": ["State 2", ...],

        "State 2": ["State 2", "State 1", ...]

        ...

        "State n"; [...]

      },

      "startstate": "State 1",

      "endstates": ["State n", ...]

    }
  '''
  # The function is written "drawn out" with more branches than necessary to enable a more accurate error display.
  if(not(
      len(t_JSON) == 3
      and ("states" in t_JSON) 
      and ("startstate" in t_JSON)
      and ("endstates" in t_JSON)
      and (isinstance(t_JSON["states"], dict))
      and (isinstance(t_JSON["startstate"], str))
      and (isinstance(t_JSON["endstates"], list))
    )):
    print("JSON string structure invalid: Only 3 key-value pairs allowed \"states\": dict, \"startstate\": str and \"enstates\": list.")
    return False
  
  for state in t_JSON["states"].values():
    if(not (isinstance(state, list)) ):
      print("JSON string structure invalid: Values in the \"states\" dicts must be of type list.")
      print(f"Type is {type(state)} instead")
      return False
    for transition in state:
      if(not (isinstance(transition, str))):
        print("JSON string structure invalid: Values of the transition destinations must be of type string.")
        return False
  
  all_states: list[str] = list(t_JSON["states"].keys())
  for state in t_JSON["states"].values():
    for transition in state:
      if(transition not in all_states):
        print(f"The destination state ({transition}) does not exist in the given JSON string.")
        return False
      
  if(t_JSON["startstate"] not in all_states):
    print(f"The start state {t_JSON['startstate']} does not exist in the list of states.")
    return False
  
  for state in t_JSON["endstates"]:
    if(state not in all_states):
      print(f"The end state {state} does not exist in the list of states.")
      return False
  
  print("All checks passed. THe given JSON string is a valid representation of a StateMachine object.")
  return True

def PrintStateMachineAdjacencyList(t_machine: dict) -> None:
  '''
    Prints out the statemachine to the console in the form of an adjacency list.

    Each line consists of the name of the source state on the left, and all the destinations that go out from this state to the right, separated by an "|"
  '''
  print("\n\nCurrent form of the statemachine: ")

  if(len(t_machine["states"]) == 0):
    print("The statemachine is empty.")
    return

  longestStateName: int = len(max(t_machine["states"], key=len))
  for state in t_machine["states"]:
    printString = state.ljust(longestStateName) + " | "
    for transition in t_machine["states"][state]:
      printString += transition + "  "
    print(printString)
  print("Start state: " + t_machine["startstate"])
  print("End states: " + str(t_machine['endstates']) )

def MenuSelectionPrompt() -> int:
  input_string: str = "Your choice: "
  print("\nWhat would you like to do with the statemachine?")
  print("1. Add new states.")
  print("2. Remove states.")
  print("3. Add transitions.")
  print("4. Remove Transitions.")
  print("5. Set start state.")
  print("6. Edit end states.")
  print("7. Save and exit")
  menuChoice: str = input(input_string)
  while(menuChoice not in ["1", "2", "3", "4", "5", "6", "7"]):
    print("Invalid input.")
    menuChoice: str = input(input_string)
  return int(menuChoice)

def ChangeStartStatePrompt(t_JSON: dict) -> dict:
  '''
    This prompts the user to change the start state in the given StateMachine JSON.
    Returns the new JSON with the changed start state.
  '''
  all_states: list = list(t_JSON["states"].keys())
  new_startstate: str = ""
  print("The statemachine currently has the following states: ")
  print(all_states)
  new_startstate = input("Which do you want to set as the new start state (leave empty if you want to abort)? : ")
  if(new_startstate == ""):
    print("Start state selection aborted.")
    return t_JSON
  while(new_startstate not in all_states):
    new_startstate = input("The state you have provided does currently not exist in the statemachine, please put in a valid state identifier or leave the input empty to abort.")
    if(new_startstate == ""):
      print("Start state selection aborted.")
      return t_JSON
  print(f"The new start state is now {new_startstate}.")
  t_JSON["startstate"] = new_startstate
  return t_JSON

def AddStatesPrompt(t_JSON: dict) -> dict:
  '''
    This prompts the User to add new states to the given statemachine JSON.
    Returns the given JSON string with any possible newly added states.
  '''
  old_states: list[str] = list(t_JSON["states"].keys())
  new_states: list[str] = []
  all_states: list[str] = old_states + new_states
  exit_check: str = ""
  while(True):
    print(f"The current states are: " + str(all_states))
    new_state: str = input("Name of the new state: ")
    if new_state == "":
      print("A state must have a identifier and cannot be left blank.")
    elif(new_state not in all_states):
      print(f"{new_state} added.")
      new_states.append(new_state)
      all_states = old_states + new_states
    else: 
      print(f"{new_state} already exists.")
    while(exit_check not in ["y", "n"]):
      exit_check = input("Add more? [y/n]: ").lower()
    if(exit_check == "n"):
      for state in new_states:
        t_JSON["states"][state] = []
      return t_JSON
    exit_check = ""

def RemoveStatesPrompt(t_JSON: dict) -> dict:
  '''
    This prompts the User to remove existing states from the given statemachine JSON.
    Returns the given JSON string with anthe states removed.
  '''
  old_states: list[str] = list(t_JSON["states"].keys())
  removed_states: list[str] = []
  exit_check: str = ""

  while(True):
    print(f"The current states are: " + str(old_states))
    to_remove: str = input("Which state would you like to remove: ")
    if(to_remove in removed_states):
      print(f"{to_remove} is already removed.")
    elif(to_remove in old_states):
      if t_JSON["startstate"] == to_remove:
        print(f"The startstate {to_remove} has been removed (New start state required).")
      else:
        print(f"The state {to_remove} has been removed.")
      old_states.remove(to_remove)
      removed_states.append(to_remove)
    else:
      print(f"{to_remove} does not exist in the statemachine.")

    while(exit_check not in ["y", "n"]):
      exit_check = input("Remove more? [y/n]: ").lower()
    if(exit_check == "n"):
      for state in removed_states:
        del t_JSON["states"][state]
        if t_JSON["startstate"] == state:
          t_JSON["startstate"] = ""
        # Remove all transitions to the removed state
        for state in t_JSON["states"].keys():
          if(to_remove in t_JSON["states"][state]):
            t_JSON["states"][state].remove(to_remove)
      return t_JSON
    exit_check = ""

def AddTransitionsPrompt(t_JSON: dict) -> dict:
  all_states: list = list(t_JSON["states"].keys())
  source_state: str = ""
  destination_state: str = ""
  exit_check: str = ""

  existing_transitions: list[str] = []

  while(True):
    PrintStateMachineAdjacencyList(t_JSON)
    print("First, put in the source state of the new Transition, followed by the destination.")
    source_state = input("Source state: ")
    destination_state = input("Destination state: ")
    
    try:
      if(source_state not in all_states):
        print(f"{source_state} does not exist in the current statemachine.")
        raise Exception()
      if(destination_state not in all_states):
        print(f"{destination_state} does not exist in the current statemachine.")
        raise Exception()
      
      existing_transitions = t_JSON["states"][source_state]

      if(destination_state in existing_transitions):
        print(f"{source_state} -> {destination_state} already exists.")
        raise Exception()
      
      print(f"{source_state} -> {destination_state} added.")
      t_JSON["states"][source_state].append(destination_state)
    except:
      pass
    finally:
      while(exit_check not in ["y", "n"]):
        exit_check = input("Add more transitions? [y/n]: ")
      if(exit_check == "n"):
        return t_JSON
    exit_check = ""

def RemoveTransitionsPrompt(t_JSON: dict) -> dict:
  all_states: list = list(t_JSON["states"].keys())
  source_state: str = ""
  destination_state: str = ""
  exit_check: str = ""

  while(True):
    PrintStateMachineAdjacencyList(t_JSON)
    print("First, put in the source state of the transition to be removed, followed by the destination.")
    source_state = input("Source state: ")
    destination_state = input("Destination state: ")

    try:
      
      if(source_state not in all_states):
        print(f"{source_state} does not exist in the current statemachine.")
        raise Exception()
      if(destination_state not in all_states):
        print(f"{destination_state} does not exist in the current statemachine.")
        raise Exception()
      if(destination_state not in t_JSON["states"][source_state]):
        print(f"{source_state} -> {destination_state} does not exist in the statemachine.")
        raise Exception()
      
      t_JSON["states"][source_state].remove(destination_state)
    except:
      pass
    finally:
      while(exit_check not in ["y", "n"]):
        exit_check = input("Remove more transitions? [y/n]: ")
      if(exit_check == "n"):
        return t_JSON
    exit_check = ""

def EditEndStatesPrompt(t_JSON: dict) -> dict:
  all_states: list = list(t_JSON["states"].keys())
  end_states: list = t_JSON["endstates"]
  exit_check: str = ""
  operation: str = ""
  selected_state: str = ""
  while(True):
    print(f"\nThe state machine currently has the following states: " + str(all_states))
    print(f"The current end states are: " + str(end_states))

    while(operation not in ["a", "r"]):
      operation = input("Would you like to add or remove an end state? [a]dd/[r]emove: ").lower()



    selected_state = input(f"State to be { 'added to'  if operation == 'a' else 'removed from'  } the end states: ")
    try:
      if(operation == "a"):
        if(selected_state not in all_states):
          print(f"{selected_state} does not exist in the current state machine.")
          raise Exception()
        if(selected_state in t_JSON["endstates"]):
          print(f"{selected_state} is already an end state.")
          raise Exception()
        t_JSON["endstates"].append(selected_state)
      else:
        if(selected_state not in all_states):
          print(f"{selected_state} does not exist in the current state machine.")
          raise Exception()
        if(selected_state not in t_JSON["endstates"]):
          print(f"{selected_state} is not an end state.")
          raise Exception()
        t_JSON["endstates"].remove(selected_state)
        
    except:
      pass
    finally:
      while(exit_check not in ["y", "n"]):
        exit_check = input("Add/remove more end states? [y/n]: ")
      if(exit_check == "n"):
        return t_JSON
    exit_check = ""
    operation = ""
