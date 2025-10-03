# H20 IN2010: Assignment 2
## siljejka

Assignment delivery contains only one compilable and executable file.

### Compile

javac ProjectPlanner.java

### Execute

java Oblig2 <project_filename>.txt

## Assumptions

Assumes input in the form of a text file with the first argument being the number of successive arguments.

Each other line must be in the form task id, task name, task time, task staff, then a list of tasks it depends on ending in 0 when none.

The program further assumes the graph is directional and acyclic, if it's not the program will stop and list dependencies of all nodes which have an edge back from any path out.

## Peculiarities

None which I'm aware of.

## Status

Everything seems to work as intended, although the solution isn't very general and only works for a very specific set of circumstances (those given by the assignment).

## Credit

### Graph traversal

Uses depth first algorithm from lectures with an added node-colouring (closed) in addition to visited for identification of cycles.

### Topological sort

Uses topological sort method from lectures to sort tasks in a possible order of execution and identify the earliest start times, the method then reverses the sorted list to back-track the graph and identify slack.

### Print schedule

Copies format from suggested output in the assignment.
