import glob
import os
import json

import functions as fn

fileName: str = ""
loadExisting: bool = True

files: list = fn.GetJSONFiles()

fileName = input("What file would you like to edit (or create a new file with a new name): ")
content = fn.GetJSONFromFile(fileName, files)

while(True):
  fn.PrintStateMachineAdjacencyList(content)
  menuChoice: int = fn.MenuSelectionPrompt()
  if(menuChoice == 1):
    content = fn.AddStatesPrompt(content)
    pass
  elif(menuChoice == 2):
    content = fn.RemoveStatesPrompt(content)
    pass
  elif(menuChoice == 3):
    content = fn.AddTransitionsPrompt(content)
    pass
  elif(menuChoice == 4):
    content = fn.RemoveTransitionsPrompt(content)
    pass
  elif(menuChoice == 5):
    content = fn.ChangeStartStatePrompt(content)
    pass
  elif(menuChoice == 6):
    content = fn.EditEndStatesPrompt(content)
    pass
  elif(menuChoice == 7):
    fn.PrintStateMachineAdjacencyList(content)
    print("")
    if (fn.SaveJSONToFile(fileName, content)):
      exit()
    
