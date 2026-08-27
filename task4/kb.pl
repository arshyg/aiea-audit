% Facts: students
student(anna).
student(bob).
student(sluggy).
student(belle).

% Facts: courses
course(cs101).
course(cs101m).
course(cs102).
course(cs201).
course(math101).

% Facts: prerequisites (course requires prereqs)
prereq(cs101m, cs101).
prereq(cs102, cs101).
prereq(cs102, cs101m).
prereq(cs201, cs102).
prereq(cs201, math101).

% Facts: which courses each student has completed
completed(anna, cs101).
completed(anna, math101).
completed(bob, cs101).
completed(sluggy, cs101).
completed(sluggy, cs102).
completed(sluggy, math101).
completed(sluggy, cs101m).
completed(belle, math101).

% Rule: a student is eligible for a course if they've completed all its prereqs(we use forall to check)
eligible(Student, Course) :-
    student(Student),
    course(Course),
    forall(prereq(Course, Prereq), completed(Student, Prereq)).

% Rule: a course is a direct prereq of another
indirect_prereq(Course, Prereq) :-
    prereq(Course, Prereq).
indirect_prereq(Course, Prereq) :-
    prereq(Course, Mid),
    indirect_prereq(Mid, Prereq).
