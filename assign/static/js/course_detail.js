document.addEventListener("DOMContentLoaded", function () {
    const courseName = document.getElementById("course-name").textContent;  // Get course name from the hidden div
    const assignmentListEl = document.getElementById('assignment-list');

    // Fetch assignments for the course using the correct URL
    fetch(`/assignments/${encodeURIComponent(courseName)}`)
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

                // Create the submit button for each assignment
                const submitButton = document.createElement('button');
                submitButton.textContent = "Submit Assignment";
                submitButton.classList.add("submit-btn");
                
                // Add the click event to open the submit form
                submitButton.addEventListener('click', () => {
                    openSubmitForm(assignment.id, assignment.name, assignment.due_date, assignment.description);
                });

                // Append the submit button to the assignment item
                assignmentItem.appendChild(submitButton);

                // Append the assignment item to the list
                assignmentListEl.appendChild(assignmentItem);
            });
        })
        .catch(error => {
            console.error('Error fetching assignments:', error);
            assignmentListEl.innerHTML = '<li>Failed to load assignments. Please try again later.</li>';
        });

    // Function to open the submit form with assignment details
    function openSubmitForm(assignmentId, assignmentName, dueDate, description) {
        // Populate the form with assignment details (readonly fields)
        document.getElementById("assignment-id").value = assignmentId;
        document.getElementById("assignment-name").value = assignmentName;
        document.getElementById("assignment-due-date").value = dueDate;
        document.getElementById("assignment-description").value = description;

        // Show the modal
        document.getElementById("submit-modal").style.display = "block";
    }

    // Function to close the modal
    function closeSubmitForm() {
        document.getElementById("submit-modal").style.display = "none";
    }

    // Close the modal if clicked outside the modal content
    window.onclick = function(event) {
        if (event.target == document.getElementById("submit-modal")) {
            closeSubmitForm();
        }
    }
});
