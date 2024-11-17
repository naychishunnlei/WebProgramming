import { sharedData } from './sharedData.js';
const menuBar = document.getElementById("bar");
const navul = document.getElementById("nav-ul");
const loginIcon = document.getElementById("login");
const loginForm = document.getElementById("login-form");
const formCloseBtn = document.querySelector(".closeBtn");
const loginBtn = document.querySelector(".btn-login");
const eye = document.getElementById("eye");
const studentID = document.getElementById("stuID");
const password = document.getElementById("password");

menuBar.addEventListener("click",()=>{
    console.log("clicked");
    navul.classList.toggle("active");
});

loginIcon.addEventListener("click",()=>{
    loginForm.classList.add("active");
    
});

loginForm.addEventListener("submit",(e)=>{
    e.preventDefault();
    
    if(loginForm.classList.contains("active")){
        window.open("student.html","_blank");
    }
    sharedData.value = studentID.value;
    localStorage.setItem("studentID", sharedData.value);
    console.log(sharedData.value);
    // studentID.value = "";
    // password.value = "";
});

formCloseBtn.addEventListener("click",()=>{
    loginForm.classList.remove("active");
});

eye.addEventListener("click",()=>{
    if(eye.classList.contains("fa-eye")){
        eye.classList.replace("fa-eye","fa-eye-slash");
        password.setAttribute("type","text");

    }else{
        eye.classList.replace("fa-eye-slash","fa-eye");
        password.setAttribute("type","password");
    }
});