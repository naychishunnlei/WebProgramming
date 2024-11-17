document.addEventListener("DOMContentLoaded", function () {
    const calendarEl = document.getElementById('calendar');
    const courseListEl = document.getElementById('course-list');
    
    // Example data (you would get this from your backend or API)
    const courses = [
        { id: 1, name: 'Python' },
        { id: 2, name: 'Rust' },
        { id: 3, name: 'C++' },
        { id: 1, name: 'Web Programming' },
    ];
    
    const assignments = [
        { id: 1, title: 'Assignment 1', course: 'Python', due_date: '2024-11-18', description: 'First assignment on SE concepts.'},
        { id: 2, title: 'Assignment 2', course: 'Rust', due_date: '2024-11-20', description: 'Implement binary tree traversal.' },
        { id: 3, title: 'Assignment 3', course: 'C++', due_date: '2024-11-22', description: 'Design ER diagram.' },
        { id: 4, title: 'Assignment 4', course: 'Web Programming', due_date: '2024-11-27', description: 'Design ER diagram.' }
    ];

    // 1. Populate the Calendar with Assignments
    const events = assignments.map(assignment => ({
        title: assignment.title,
        start: assignment.due_date,
        course: assignment.course,
        assignmentId: assignment.id,
    }));

    const calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        events: events,
        eventClick: function(info) {
            const { title, description, start, course, assignmentId } = info.event.extendedProps;
            alert(`Assignment: ${title}\nCourse: ${course}\nDue Date: ${start.toLocaleDateString()}\nDescription: ${description}`);
            // Redirect to assignment details page
            window.location.href = `/course/${course}/assignment/${assignmentId}`;
        }
    });
    calendar.render(); 

    // 2. Populate the Courses List
    courses.forEach(course => {
        const courseItem = document.createElement('li');
        const courseLink = document.createElement('a');
        courseLink.href = `/course/${course.id}`;
        courseLink.textContent = course.name;
        courseItem.appendChild(courseLink);
        courseListEl.appendChild(courseItem);
    });

    // 3. Show Assignments for a specific Course (in the course page)
    function showAssignmentsForCourse(courseId) {
        const filteredAssignments = assignments.filter(a => a.course === courses.find(c => c.id === courseId).name);
        const assignmentsContainer = document.getElementById('assignment-list');
        assignmentsContainer.innerHTML = '';  // Clear the list

        filteredAssignments.forEach(assignment => {
            const assignmentItem = document.createElement('li');
            assignmentItem.textContent = `${assignment.name} - Due: ${assignment.due_date}`;
            assignmentItem.addEventListener('click', () => {
                // Open assignment details and allow submission
                alert(`Assignment: ${assignment.name}\nDue Date: ${assignment.due_date}\nDescription: ${assignment.description}`);
                // Optionally, redirect to a form to upload the assignment
            });
            assignmentsContainer.appendChild(assignmentItem);
        });
    }

    // 4. Logout Toggle functionality
    const logoutBtn = document.getElementById('logoutBtn');
    const logout = document.getElementById('logout');

    // Toggle the logout box when the user icon is clicked
    logoutBtn.addEventListener('click', function () {
        event.stopPropagation();
        logout.classList.toggle('active');
    });

    
});
