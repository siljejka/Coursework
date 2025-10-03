import java.io.File;
import java.io.IOException;
import java.util.Scanner;
import java.util.*;


// Class which initiates a node
class Task {
  int id, time, staff;
  String  name;
  int earliestStart, latestStart;
  List<Task>   outEdges;
  int cntPredecessors;
  boolean visited = false, closed = false; // Node colours for cycle identification

  // Constructor
  public Task(int n){
    id = n;
    outEdges = new ArrayList<Task>();
  }

  // Method which adds a directional edge from the task to another
  public void addEdge(Task task){
    outEdges.add(task);
  }
}


/* Class that takes a file input of a project task structure, then creates an
   array of tasks from it. The class then runs a graph traversal to check for cycles,
   then if no cycles are found it does a topological sort before printing a
   schedule using the earliest start times for each task as well as a full list of
   tasks. */
class ProjectPlanner {
    // Main method
    public static void main(String[] args) throws IOException {
        // Read input from file and create a list of nodes (tasks)
        String filename = args[0];
        Scanner in = new Scanner(new File(filename));

        int n = in.nextInt();
        Task[] tasks = new Task[n];

        for (int i = 0; i < n; i++) {
            tasks[i] = new Task(i + 1);
        }

        for (int i = 0; i < n; i++) {
            int id = in.nextInt();
            Task task = tasks[id - 1];
            task.name = in.next();
            task.time = in.nextInt();
            task.staff = in.nextInt();

            while (true) {
                int dep = in.nextInt();
                if (dep == 0) {
                    break;
                }
                tasks[dep - 1].addEdge(task);
                tasks[id - 1].cntPredecessors++;
            }
        }

        // Initialise a project with the tasks
        ProjectPlanner project = new ProjectPlanner(tasks, n);
        project.graphTraversal();

        // Print project name
        System.out.println("Project " + filename);
        System.out.println(" ");

        // Print cycles if found
        if (project.cyclic == true) {
            project.printCycle();
        }
        // Print schedule and tasks if there are no cycles
        else {
            project.topologicalSort();

            System.out.println("Project schedule for " + filename);
            project.printSchedule();

            System.out.println(" ");
            System.out.println("Project tasks for " + filename);
            project.printProject();
        }
    }

    Task[] tasks; // Array of nodes
    int n; // Number of tasks in project
    boolean cyclic; // True if there are cycles
    List<Task> sortedTasks; // List of tasks in sroted order per topologicalSort()
    ArrayDeque<Task> stack, criticalPath;
    Deque<ArrayDeque<Task>> cycles; /* List of all cycles in the graph if
                                       graphTraversal() has been run. */
    int completionTime; // Fastest possible completion time of project

    // Constructor
    public ProjectPlanner (Task[] taskList, int taskCount) {
        tasks = taskList;
        n = taskCount;
    }

    // Depth first search from a single node
    public void depthFirst (Task v) {
        v.visited = true;
        stack.add(v);

        for (Task u: v.outEdges) {
            if (!u.visited) {
                depthFirst(u);
            }
            else if (!u.closed) {
                cyclic = true;
                stack.add(u);
                ArrayDeque<Task> cycle = stack.clone();
                cycles.add(cycle);
            }
        }

        stack.removeLast();
        v.closed = true;
    }

    /* Prints cycles and co-dependencies if any where found when running
       depthFirst() */
    public void printCycle () {
        System.out.println("The project isn't realizable because of cyclic "
                            + "dependencies.");
        System.out.println("These cyclic dependencies are:");
        for (Deque<Task> cycle: cycles) {
            Task last = cycle.removeLast();
            for (Task v: cycle) {
                System.out.print(v.id + " -> ");
            }
            System.out.println(last.id);
            cycle.add(last);
        }
    }

    // Runs depthFirst() from all unvisited task nodes in project graph
    public void graphTraversal () {
        stack = new ArrayDeque<Task>();
        cycles = new ArrayDeque<ArrayDeque<Task>>();

        for (Task v: tasks) {
            if (!v.visited) {
              depthFirst(v);
            }
        }
    }

    /* Sorts the tasks using topological sort while identifying the earliest
       start times using preceeding nodes. It then back-tracks from the last task
       to find the latest possible start times. Method then saves a list of
       critical tasks in criticalPath. */
    public void topologicalSort () {
        sortedTasks = new ArrayList<Task>();
        int[] remainingTasks = new int[n];

        int i = 0;
        for (Task v: tasks) {
            remainingTasks[i] = v.cntPredecessors;
            i++;
        }

        stack = new ArrayDeque<Task>();
        for (Task v: tasks) {
            if (v.cntPredecessors == 0){
                v.earliestStart = 0;
                stack.push(v);
            }
        }
        while (!stack.isEmpty()) {
            Task v = stack.poll();
            sortedTasks.add(v);
            for (Task u: v.outEdges) {
                remainingTasks[u.id - 1]--;
                if (v.earliestStart + v.time > u.earliestStart) {
                    u.earliestStart = v.earliestStart + v.time;
                }
                if (remainingTasks[u.id - 1] == 0){
                  stack.add(u);
                }
            }
        }

        criticalPath = new ArrayDeque<Task>();
        for (Task v: sortedTasks) {
            if (v.earliestStart + v.time > completionTime) {
                completionTime = v.earliestStart + v.time;
            }
            stack.push(v);
        }
        for (Task v: stack) {
            v.latestStart = completionTime - v.time;
            for (Task u: v.outEdges) {
                if (u.latestStart - v.time < v.latestStart) {
                    v.latestStart = u.latestStart - v.time;
                }
            }
            if (v.latestStart - v.earliestStart == 0) {
                criticalPath.push(v);
            }
        }
    }

    /* For each task the method inputs the start and end points into a
       time-sorted array. It then updates the staff array for all times between
       to reflect current staff needed in the project. These are then printed
       chronologically using printf.*/
    public void printSchedule () {
        String[][] schedule = new String[completionTime+1][tasks.length + 1];
        int[] index = new int[completionTime+1];
        int[] staff = new int[completionTime+1];
        for (Task v: tasks) {
            int endTime = v.earliestStart + v.time;

            schedule[v.earliestStart][index[v.earliestStart]] = "Starting: " + v.id + " (" + v.name + ")";
            index[v.earliestStart]++;
            for (int i = v.earliestStart; i < endTime; i++) {
                staff[i] += v.staff;
            }
            schedule[endTime][index[endTime]] = "Finished: " + v.id;
            index[endTime]++;
        }

        for (int i = 0; i < completionTime + 1; i++) {
            if (index[i] > 0) {
                System.out.println(" ");
                System.out.printf("%-18s %s\n", "Time: " + i, schedule[i][0]);
                int j = 1;
                while (schedule[i][j] != null) {
                    System.out.printf("%-18s %s\n", " ", schedule[i][j]);
                    j++;
                }
                if (staff[i] > 0) {
                    System.out.printf("%-18s %s\n", " ", "Current staff: " + staff[i]);
                }

            }
        }

        System.out.println(" ");
        System.out.println("**** Shortest possible project execution is " +
                            completionTime + " ****");
    }

    // Prints all tasks in project
    public void printProject () {
        for (Task v: tasks) {
            System.out.println(" ");
            int slack = v.latestStart - v.earliestStart;
            System.out.printf("%-18s %s\n", "Task " + v.id + " (" + v.name + ")", " ");
            System.out.println("-----------------------------------");
            System.out.printf("%-18s %s\n", "Time to complete:", v.time);
            System.out.printf("%-18s %s\n", "Staff needed:", v.staff);
            System.out.printf("%-18s %s\n", "Earliest start:", v.earliestStart);
            System.out.printf("%-18s %s\n", "Slack:", slack);
            if (!v.outEdges.isEmpty()) {
                System.out.printf("%-17s %s", "Dependent tasks:", " ");
                for (Task u: v.outEdges) {
                    System.out.print(u.id + " ");
                }
                System.out.println(" ");
            }
        }
        System.out.println(" ");
    }
}
