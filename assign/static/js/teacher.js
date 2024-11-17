document.addEventListener("DOMContentLoaded", function () {
    // Elements
    const logoutEle = document.getElementById("logout");
    const logoutBtn = document.getElementById("logoutBtn");
    const menuBar = document.getElementById("bar");
    const addAssignmentBtn = document.querySelector("#addBtn");
    const showModal = document.querySelector(".modal");
    const closeBtn = document.getElementById("closeBtn");
    const courseEle = document.getElementById("course");
    const courseLinks = document.querySelectorAll(".course-li");
    const assignmentContainers = document.querySelectorAll(".course-assignments");
    const courseTitle = document.getElementById("courseTitle");
    const errorMessage = document.getElementById("error-message");

    // Event Listeners
    menuBar.addEventListener("click", (e) => {
        e.stopPropagation();
        courseEle.classList.toggle("active");
    });

    logoutBtn.addEventListener("click", () => logoutEle.classList.toggle("active"));
    addAssignmentBtn.addEventListener("click", () => showModal.classList.add("active"));
    closeBtn.addEventListener("click", () => showModal.classList.remove("active"));

    courseLinks.forEach(function (link) {
        link.addEventListener("click", function (event) {
            event.preventDefault();
            const selectedCourseLi = this.getAttribute("href").substring(1);
            updateCourseBanner(selectedCourseLi);
            showAssignments(selectedCourseLi);

            // Highlight the active course
            courseLinks.forEach((link) => link.classList.remove("active"));
            this.classList.add("active");
        });
    });

    // Functions
    function updateCourseBanner(courseName) {
        courseTitle.innerHTML = `${courseName.toUpperCase()} Assignments`;
        const imageContainer = document.querySelector(".image-container img");

        // Map courses to banner images
        const bannerMap = {
            python: "/static/img/python-banner.png",
            rust: "/static/img/rust-banner.png",
            "c++": "/static/img/c++-banner.jpg",
            web: "/static/img/web-banner.png",
        };

        // Update the banner or fall back to default
        imageContainer.src = bannerMap[courseName] || "/static/img/default-banner.png";
    }

    function showAssignments(courseName) {
        assignmentContainers.forEach((container) => {
            if (courseName === container.getAttribute("data-course")) {
                container.style.display = "block";
            } else {
                container.style.display = "none";
            }
        });
    }

    // Handle Add Assignment Form Submission
    const addAssignmentForm = document.getElementById("assignment-form");
    if (addAssignmentForm) {
        addAssignmentForm.addEventListener("submit", function (event) {
            event.preventDefault();
            const formData = new FormData(this);

            fetch("/teachers/assignments/", {
                method: "POST",
                body: formData,
            })
                .then((response) => {
                    if (!response.ok) throw new Error("Failed to add assignment");
                    return response.json();
                })
                .then((data) => {
                    console.log("Assignment added:", data);
                    showModal.classList.remove("active"); // Close the modal
                    location.reload(); // Reload to reflect the changes
                })
                .catch((error) => {
                    console.error("Error adding assignment:", error);
                    errorMessage.innerText = error.message;
                    errorMessage.style.display = "block";
                });
        });
    }

    // Handle Assignment Deletion
    document.querySelectorAll(".fa-trash").forEach((icon) => {
        icon.addEventListener("click", function (event) {
            event.preventDefault();
            if (confirm("Are you sure you want to delete this assignment?")) {
                const url = this.parentElement.getAttribute("href");

                fetch(url, { method: "DELETE" })
                    .then((response) => {
                        if (!response.ok) throw new Error("Failed to delete assignment");
                        return response.json();
                    })
                    .then((data) => {
                        console.log("Assignment deleted:", data);
                        this.closest(".assignment-box").remove(); // Remove from UI
                    })
                    .catch((error) => console.error("Error deleting assignment:", error));
            }
        });
    });

    // Pre-select and display the current course assignments if provided
    const currentCourse = "{{ course_name|default('') }}";
    if (currentCourse) {
        updateCourseBanner(currentCourse);
        showAssignments(currentCourse);

        // Highlight the active course link
        courseLinks.forEach((link) => {
            if (link.getAttribute("href").substring(1) === currentCourse) {
                link.classList.add("active");
            }
        });
    }
});
