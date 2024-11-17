const arrowBtn = document.getElementById("arrowBtn");
const calendarBox = document.querySelector(".calendar");
const studID = document.getElementById("stuId");
const dayEle = document.querySelector(".date");
const menuBar = document.getElementById("bar");
const navul = document.getElementById("nav-ul");

menuBar.addEventListener("click",()=>{
    console.log("clicked");
    navul.classList.toggle("active");
});


var days = ["Sun","Mon","Tue","Wed","Thu","Fri","Sat"];

arrowBtn.addEventListener("click", (e) => {
    e.preventDefault();
    calendarBox.classList.toggle("active");
});

//get the student id from general page login
const studentID = localStorage.getItem("studentID");
studID.textContent = studentID;

let dateObj = new Date();
let date = dateObj.getDate();
let day = days[dateObj.getDay()];
let hr = dateObj.getHours();
let min = dateObj.getMinutes();
const amPm = hr >= 12 ? 'PM' : 'AM';
hr = hr % 12 || 12;
dayEle.innerText = `${date}, ${day} , ${hr} : ${min} ${amPm}`;


const examTimetableDropdown = document.getElementById('examTimetable');
const classTimetableDropdown = document.getElementById('classTimetable');


examTimetableDropdown.addEventListener('change', function() {
    const selectedExam = examTimetableDropdown.value;
    localStorage.setItem('examSelected', selectedExam);
    localStorage.removeItem('classSelected'); 
    window.location.href = 'timetable.html';

});

classTimetableDropdown.addEventListener('change', function() {
    const selectedClass = classTimetableDropdown.value;
    localStorage.setItem('classSelected', selectedClass);
    localStorage.removeItem('examSelected'); 
    window.location.href = 'timetable.html';

});