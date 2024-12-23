document.addEventListener("DOMContentLoaded", function () {
    const courseName = document.getElementById("course-name").textContent;  // Get course name from the hidden div
    const assignmentListEl = document.getElementById('assignment-list');

    // Fetch assignments for the course using the correct URL
    fetch(`/course/${encodeURIComponent(courseName)}/assignments`)
        .then(response => response.json())
        .then(assignments => {
            if (!Array.isArray(assignments)) {
                console.error('Invalid assignments data:', assignments);
                assignmentListEl.innerHTML = '<li>Error: Invalid assignments data.</li>';
                return;
            }

            // Check if there are any assignments for the course
            if (assignments.length === 0) {
                assignmentListEl.innerHTML = '<li>No assignments found for this course.</li>';
                return;
            }

            assignments.forEach(assignment => {
                const assignmentItem = document.createElement('li');
                assignmentItem.textContent = `${assignment.name} - Due: ${assignment.due_date}`;

                // Add a click event to show more details about the assignment
                assignmentItem.addEventListener('click', () => {
                    alert(`Assignment: ${assignment.name}\nDue Date: ${assignment.due_date}\nDescription: ${assignment.description}`);
                });

                // You can also add a download button
                const downloadButton = document.createElement('button');
                downloadButton.textContent = "Download";
                downloadButton.addEventListener('click', (e) => {
                    e.stopPropagation();  // Prevent triggering the click event of the list item
                    window.location.href = `/assignment/${courseName}/${assignment.id}/download`;
                });

                assignmentItem.appendChild(downloadButton);
                assignmentListEl.appendChild(assignmentItem);
            });
        })
        .catch(error => {
            console.error('Error fetching assignments:', error);
            assignmentListEl.innerHTML = '<li>Failed to load assignments. Please try again later.</li>';
        });
});
