import os, sys, shutil
import subprocess
import traceback

import inv_check
import insert_jaif
import ontology_to_daikon

import backend


WORKING_DIR = os.path.dirname(os.path.realpath(__file__))
daikon_jar = os.path.join(WORKING_DIR, "libs/daikon.jar") 


def run_command(cmd):
  print (" ".join(cmd))
  try:
    return subprocess.check_output(cmd, stderr=subprocess.STDOUT)
  except:
    raise Exception('calling {cmd} failed\n{trace}'.format(cmd=' '.join(cmd),trace=traceback.format_exc()))


def main():
  """ SUMMARY: use case of the user-driven functionality of PASCALI.
  Scenario: User provides the concept of Sequence and the equivalent Java
  types, and the concept of sorted sequence and the relevant type invariant.
  Goal: learn how to get from Sequence -> Sorted Sequence. 
  """

  """ Look for new mapping from 'ontology concepts'->'java type' and run 
  checker framework. Should be implemented in type_inference
  Mapping example:
    Sequence -> java.lang.Array, java.util.List, LinkedHashSet, etc.

  INPUT: corpus, file containing set of concept->java_type mapping
  OUTPUT: Set of jaif files that are merged into the classes using
          insert_jaif. 
  BODY: This also triggers back-end labeled graph generation.
  """

  print "todo" #WERNER


  """ Missing step: interact with PA to add a definition of Sorted Sequence
  which is a specialization of Sequence that has a sortedness invariants. 
  The sortedness invariant gets turned into a Daikon template
  INPUT: user interaction
  OUTPUT: type_annotation and type_invariant (for sorted sequence)

  """

  ontology_invariant_file = "TODO_from_Howie.txt"
  with open(ontology_invariant_file, 'w') as f:
    f.write("TODO")
  
  invariant_name = "TODO_sorted_sequence"

  daikon_pattern_java_file = ontology_to_daikon.create_daikon_invariant(ontology_invariant_file, invariant_name)

  """ Search for methods that have a return type annotated with Sequence
  and for which we can establish a sortedness invariant (may done by LB).

  INPUT: dtrace file of project
         daikon_pattern_java_file that we want to check on the dtrace file.
  
  OUTPUT: list of ppt names that establish the invariant. Here a ppt 
  is a Daikon program point, s.a. test01.TestClass01.sort(int[]):::EXIT

  Note: this step translate the type_invariant into a Daikon 
  template (which is a Java file).
  """

  pattern_class_name = invariant_name
  pattern_class_dir = os.path.join(WORKING_DIR, "invClass")
  if os.path.isdir(pattern_class_dir):
    shutil.rmtree(pattern_class_dir)
  os.mkdir(pattern_class_dir)

  cmd = ["javac", "-g", "-classpath", daikon_jar, daikon_pattern_java_file, "-d", pattern_class_dir]
  run_command(cmd)

  corpus = ["TODO"] #TODO: @Tim, add the real corpus here

  for project in corpus:
    dtrace_file = backend.get_dtrace_file_for_project(project)
    list_of_methods = inv_check.find_ppts_that_establish_inv(dtrace_file, pattern_class_dir, pattern_class_name)

  """ Expansion of dynamic analysis results .... 
  Find a list of similar methods that are similar to the ones found above (list_of_methods).
  INPUT: list_of_methods, corpus with labeled graphs generated, threshold value for similarity, 
  OUTPUT: superset_list_of_methods
  """

  print "todo" # WENCHAO

  """ Update the type annotations for the expanded dynamic analysis results.
  INPUT: superset_list_of_methods, annotation to be added
  OUTPUT: nothing
  EFFECT: updates the type annotations of the methods in superset_list_of_methods.
  This requires some additional checks to make sure that the methods actually 
  perform some kind of sorting. Note that we do it on the superset because the original
  list_of_methods might miss many implementations because fuzz testing could not 
  reach them.
  """
  for class_file in []: # MARTIN
    generated_jaif_file = "TODO"
    insert_jaif.merge_jaif_into_class(class_file, generated_jaif_file)


  """ Ordering of expanded dynamic analysis results ....
  Find the k 'best' implementations in superset of list_of_methods
  INPUT: superset_list_of_methods, corpus, k
  OUTPUT: k_list_of_methods 
  Note: similarity score is used. may consider using other scores; e.g., TODO:???
  """

  print "todo" # Huascar

  """ 
  Close the loop and add the best implementation found in the previous
  step back to the ontology.
  INPUT: k_list_of_methods
  OUTPUT: patch file for the ontology. Worst case: just add the 'best' implementation
  found in the corpus as a blob to the ontology. Best case: generate an equivalent 
  flow-graph in the ontology.
  """
  print "TODO" # ALL



if not os.path.isfile(daikon_jar):
  print "Downloading dependencies"
  cmd = ["./fetch_dependencies.sh"]
  run_command(cmd)
  print "Done."

if __name__ == '__main__':
  main()
