// Fetch assignments from the backend
async function fetchAssignments() {
    const response = await fetch('http://127.0.0.1:8000/assignments');
    if(!response.ok){
        throw new Error(`HTTP error! status: ${response.status}`)
    }
    const assignments = await response.json();
    console.log('Fetched Assignments: ', assignments);
    const events = assignments.map(assignment => ({
        course: assignment.course,
        title: assignment.title,
        due_date: assignment.due_date,
        description: assignment.description,
    }));
    displayAssignments(events);
}

// Display assignments in the list
function displayAssignments(assignments) {
    const today = new Date();
    const startOfWeek = new Date(today.setDate(today.getDate() - today.getDay())); // Sunday
    const endOfWeek = new Date(today.setDate(startOfWeek.getDate() + 6)); // Saturday

    const assignmentList = document.getElementById('assignment-list');
    assignmentList.innerHTML = ''; // Clear previous assignments

    assignments.forEach(assignment => {
        const dueDate = new Date(assignment.due_date); // Parse the due date
        if (dueDate >= startOfWeek && dueDate <= endOfWeek) {
            const listItem = document.createElement('li');
            listItem.innerHTML = `
                <strong>${assignment.course}</strong>: ${assignment.title} (Due: ${assignment.due_date})
                <p>${assignment.description}</p>
            `;
            assignmentList.appendChild(listItem);
        }
    });
}

// Initial fetch of assignments when the page loads
fetchAssignments();

document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        events: [
            {
                title: 'Class Schedule Example',
                start: '2024-10-10'
            }
        ]
    });
    calendar.render();
});

document.addEventListener('DOMContentLoaded', function () {
    const calendarEl = document.getElementById('calendar');

    const calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'timeGridWeek',
        events: [], // Will be populated with fetched data

        // Optionally, you can customize event display
        eventClick: function(info) {
            alert(info.event.title + " starts at " + info.event.start.toLocaleString());
        }
    });

    // Fetch timetable data from the backend
    async function fetchTimetable() {
        const response = await fetch('http://127.0.0.1:8000/timetable');
        const timetable = await response.json();

        // Populate the calendar with the fetched timetable
        timetable.forEach(item => {
            calendar.addEvent({
                title: item.course,
                start: item.start_time,
                end: item.end_time,
                allDay: false // Set to true if it's an all-day event
            });
        });
        
        calendar.render(); // Render the calendar with events
    }

    // Initial fetch when the page loads
    fetchTimetable();
});

document.addEventListener("DOMContentLoaded", function() {
    Promise.all([
        fetch('http://127.0.0.1:8000/assignments').then(response => response.json()),
        fetch('http://127.0.0.1:8000/timetable').then(response => response.json())
    ])
    .then(([assignments, timetable]) => {
        console.log('Assignments:', assignments);
        console.log('Timetable:', timetable);
        displayAssignments(assignments);
        initializeCalendar(timetable);
    })
    .catch(error => console.error('Error fetching data:', error));

    function displayAssignments(assignments) {
        const today = new Date();
        const startOfWeek = new Date(today.setDate(today.getDate() - today.getDay()));
        const endOfWeek = new Date(today.setDate(startOfWeek.getDate() + 6));

        const assignmentList = document.getElementById('assignment-list');
        assignmentList.innerHTML = '';

        assignments.forEach(assignment => {
            const dueDate = new Date(assignment.due_date);
            if(dueDate >= startOfWeek && dueDate <= endOfWeek) {
                const listItem = document.createElement('li');
                listItem.innerHTML = `${assignment.title} - Due: ${assignment.due_date}`;
                assignmentList.appendChild(listItem);
            }
        });
    }

    function initializeCalendar(timetable) {
        const calendarEl = document.getElementById('calendar');
        const calendar = new FullCalendar.Calendar(calendarEl, {
            initialView: 'dayGridMonth',
            events: timetable.map(entry => ({
                title: entry.course,
                start: entry.start_time,
                end: entry.end_time,
                allDay: true
            })),
        });
        calendar.render();
    }
})