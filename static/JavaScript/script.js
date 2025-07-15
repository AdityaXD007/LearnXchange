// Global state management
class SkillSwapApp {
  constructor() {
    this.currentUser = this.loadUser();
    this.skills = this.loadSkills();
    this.sessions = this.loadSessions();
    this.requests = this.loadRequests();
    this.init();
  }

  init() {
    this.initNavigation();
    this.initAuth();
    this.initModals();
    this.loadPageSpecificFeatures();
  }

  // Navigation
  initNavigation() {
    const navToggle = document.getElementById("navToggle");
    const navMenu = document.getElementById("navMenu");

    if (navToggle && navMenu) {
      navToggle.addEventListener("click", () => {
        navMenu.classList.toggle("active");
      });
    }

    // Update navigation based on auth status
    this.updateNavigation();
  }

  updateNavigation() {
    const navAuth = document.querySelector(".nav-auth");
    if (!navAuth) return;

    if (this.currentUser) {
      navAuth.innerHTML = `
                <div class="user-menu">
                    <img src="${
                      this.currentUser.avatar ||
                      "/src/assets/default-avatar.png"
                    }"
                         alt="Profile" class="nav-avatar">
                    <span>${this.currentUser.name}</span>
                    <button onclick="app.logout()" class="btn btn-outline btn-sm">Logout</button>
                </div>
            `;
    }
  }

  // Authentication
  initAuth() {
    const loginForm = document.getElementById("loginForm");
    const registerForm = document.getElementById("registerForm");

    if (loginForm) {
      loginForm.addEventListener("submit", (e) => this.handleLogin(e));
    }

    if (registerForm) {
      registerForm.addEventListener("submit", (e) => this.handleRegister(e));
    }
  }

  handleLogin(e) {
    e.preventDefault();
    const formData = new FormData(e.target);
    const email = formData.get("email");
    const password = formData.get("password");

    // Simulate authentication
    if (email && password) {
      this.currentUser = {
        id: Date.now(),
        name: email.split("@")[0],
        email: email,
        avatar: null,
        bio: "",
        teachingSkills: [],
        learningSkills: [],
        rating: 0,
        completedSessions: 0,
      };
      this.saveUser(this.currentUser);
      this.showSuccess("Login successful!");
      setTimeout(() => {
        window.location.href = "/src/pages/dashboard.html";
      }, 1000);
    }
  }

  handleRegister(e) {
    e.preventDefault();
    const formData = new FormData(e.target);
    const name = formData.get("name");
    const email = formData.get("email");
    const password = formData.get("password");

    if (name && email && password) {
      this.currentUser = {
        id: Date.now(),
        name: name,
        email: email,
        avatar: null,
        bio: "",
        teachingSkills: [],
        learningSkills: [],
        rating: 0,
        completedSessions: 0,
      };
      this.saveUser(this.currentUser);
      this.showSuccess("Registration successful!");
      setTimeout(() => {
        window.location.href = "/src/pages/profile.html";
      }, 1000);
    }
  }

  logout() {
    this.currentUser = null;
    localStorage.removeItem("skillswap_user");
    window.location.href = "/";
  }

  // Skills Management
  addSkill(skillName, type) {
    const skill = {
      id: Date.now(),
      name: skillName,
      type: type, // 'teaching' or 'learning'
      level: "beginner",
    };

    if (type === "teaching") {
      this.currentUser.teachingSkills.push(skill);
    } else {
      this.currentUser.learningSkills.push(skill);
    }

    this.saveUser(this.currentUser);
    this.renderSkills();
  }

  removeSkill(skillId, type) {
    if (type === "teaching") {
      this.currentUser.teachingSkills = this.currentUser.teachingSkills.filter(
        (s) => s.id !== skillId
      );
    } else {
      this.currentUser.learningSkills = this.currentUser.learningSkills.filter(
        (s) => s.id !== skillId
      );
    }
    this.saveUser(this.currentUser);
    this.renderSkills();
  }

  renderSkills() {
    const teachingContainer = document.getElementById("teachingSkills");
    const learningContainer = document.getElementById("learningSkills");

    if (teachingContainer) {
      teachingContainer.innerHTML = this.currentUser.teachingSkills
        .map(
          (skill) => `
                <div class="skill-tag">
                    <span>${skill.name}</span>
                    <button onclick="app.removeSkill(${skill.id}, 'teaching')" class="remove-skill">×</button>
                </div>
            `
        )
        .join("");
    }

    if (learningContainer) {
      learningContainer.innerHTML = this.currentUser.learningSkills
        .map(
          (skill) => `
                <div class="skill-tag">
                    <span>${skill.name}</span>
                    <button onclick="app.removeSkill(${skill.id}, 'learning')" class="remove-skill">×</button>
                </div>
            `
        )
        .join("");
    }
  }

  // Session Management
  requestSession(teacherId, skillId) {
    const request = {
      id: Date.now(),
      studentId: this.currentUser.id,
      teacherId: teacherId,
      skillId: skillId,
      status: "pending",
      requestedDate: new Date().toISOString(),
      message: "",
    };

    this.requests.push(request);
    this.saveRequests(this.requests);
    this.showSuccess("Session request sent!");
  }

  acceptRequest(requestId) {
    const request = this.requests.find((r) => r.id === requestId);
    if (request) {
      request.status = "accepted";
      const session = {
        id: Date.now(),
        studentId: request.studentId,
        teacherId: request.teacherId,
        skillId: request.skillId,
        date: new Date().toISOString(),
        status: "scheduled",
        meetingLink: "",
      };
      this.sessions.push(session);
      this.saveRequests(this.requests);
      this.saveSessions(this.sessions);
      this.renderRequests();
      this.renderSessions();
    }
  }

  rejectRequest(requestId) {
    const request = this.requests.find((r) => r.id === requestId);
    if (request) {
      request.status = "rejected";
      this.saveRequests(this.requests);
      this.renderRequests();
    }
  }

  // Calendar functionality
  initCalendar() {
    const calendar = document.getElementById("calendar");
    if (!calendar) return;

    const today = new Date();
    const currentMonth = today.getMonth();
    const currentYear = today.getFullYear();

    this.renderCalendar(currentYear, currentMonth);
  }

  renderCalendar(year, month) {
    const calendar = document.getElementById("calendar");
    const monthNames = [
      "January",
      "February",
      "March",
      "April",
      "May",
      "June",
      "July",
      "August",
      "September",
      "October",
      "November",
      "December",
    ];

    const firstDay = new Date(year, month, 1).getDay();
    const daysInMonth = new Date(year, month + 1, 0).getDate();

    let html = `
            <div class="calendar-header">
                <button onclick="app.changeMonth(-1)" class="btn btn-outline">‹</button>
                <h3>${monthNames[month]} ${year}</h3>
                <button onclick="app.changeMonth(1)" class="btn btn-outline">›</button>
            </div>
            <div class="calendar-grid">
                <div class="day-header">Sun</div>
                <div class="day-header">Mon</div>
                <div class="day-header">Tue</div>
                <div class="day-header">Wed</div>
                <div class="day-header">Thu</div>
                <div class="day-header">Fri</div>
                <div class="day-header">Sat</div>
        `;

    // Empty cells for days before month starts
    for (let i = 0; i < firstDay; i++) {
      html += '<div class="calendar-day empty"></div>';
    }

    // Days of the month
    for (let day = 1; day <= daysInMonth; day++) {
      const date = new Date(year, month, day);
      const isToday = date.toDateString() === new Date().toDateString();
      const sessions = this.getSessionsForDate(date);

      html += `
                <div class="calendar-day ${
                  isToday ? "today" : ""
                }" onclick="app.selectDate('${date.toISOString()}')">
                    <span class="day-number">${day}</span>
                    ${
                      sessions.length > 0
                        ? `<div class="session-indicator">${sessions.length}</div>`
                        : ""
                    }
                </div>
            `;
    }

    html += "</div>";
    calendar.innerHTML = html;
  }

  getSessionsForDate(date) {
    return this.sessions.filter((session) => {
      const sessionDate = new Date(session.date);
      return sessionDate.toDateString() === date.toDateString();
    });
  }

  // Modals
  initModals() {
    document.addEventListener("click", (e) => {
      if (e.target.classList.contains("modal-overlay")) {
        this.closeModal(e.target.closest(".modal"));
      }
    });
  }

  openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
      modal.style.display = "flex";
      document.body.style.overflow = "hidden";
    }
  }

  closeModal(modal) {
    if (modal) {
      modal.style.display = "none";
      document.body.style.overflow = "auto";
    }
  }

  // Notifications
  showSuccess(message) {
    this.showNotification(message, "success");
  }

  showError(message) {
    this.showNotification(message, "error");
  }

  showNotification(message, type = "info") {
    const notification = document.createElement("div");
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
            <div class="notification-content">
                <span>${message}</span>
                <button onclick="this.parentElement.parentElement.remove()">×</button>
            </div>
        `;

    document.body.appendChild(notification);

    setTimeout(() => {
      notification.remove();
    }, 5000);
  }

  // Data persistence
  loadUser() {
    const userData = localStorage.getItem("skillswap_user");
    return userData ? JSON.parse(userData) : null;
  }

  saveUser(user) {
    localStorage.setItem("skillswap_user", JSON.stringify(user));
  }

  loadSkills() {
    const skillsData = localStorage.getItem("skillswap_skills");
    return skillsData ? JSON.parse(skillsData) : this.getDefaultSkills();
  }

  saveSkills(skills) {
    localStorage.setItem("skillswap_skills", JSON.stringify(skills));
  }

  loadSessions() {
    const sessionsData = localStorage.getItem("skillswap_sessions");
    return sessionsData ? JSON.parse(sessionsData) : [];
  }

  saveSessions(sessions) {
    localStorage.setItem("skillswap_sessions", JSON.stringify(sessions));
  }

  loadRequests() {
    const requestsData = localStorage.getItem("skillswap_requests");
    return requestsData ? JSON.parse(requestsData) : [];
  }

  saveRequests(requests) {
    localStorage.setItem("skillswap_requests", JSON.stringify(requests));
  }

  getDefaultSkills() {
    return [
      "JavaScript",
      "Python",
      "React",
      "Node.js",
      "CSS",
      "HTML",
      "Photography",
      "Design",
      "Spanish",
      "French",
      "Guitar",
      "Piano",
      "Cooking",
      "Writing",
      "Marketing",
      "Business",
    ];
  }

  // Page-specific features
  loadPageSpecificFeatures() {
    const path = window.location.pathname;

    if (path.includes("dashboard")) {
      this.initDashboard();
    } else if (path.includes("profile")) {
      this.initProfile();
    } else if (path.includes("matching")) {
      this.initMatching();
    } else if (path.includes("sessions")) {
      this.initSessions();
    } else if (path.includes("calendar")) {
      this.initCalendar();
    }
  }

  initDashboard() {
    this.renderDashboardStats();
    this.renderRecentSessions();
    this.renderUpcomingSessions();
  }

  initProfile() {
    this.renderProfile();
    this.renderSkills();
  }

  initMatching() {
    this.renderMatches();
  }

  initSessions() {
    this.renderSessions();
    this.renderRequests();
  }

  renderDashboardStats() {
    // Implementation for dashboard statistics
  }

  renderRecentSessions() {
    // Implementation for recent sessions
  }

  renderUpcomingSessions() {
    // Implementation for upcoming sessions
  }

  renderProfile() {
    // Implementation for profile rendering
  }

  renderMatches() {
    // Implementation for skill matching
  }

  renderSessions() {
    // Implementation for sessions list
  }

  renderRequests() {
    // Implementation for requests list
  }
}

// Initialize the app
let app;
document.addEventListener("DOMContentLoaded", () => {
  app = new SkillSwapApp();
});

// Utility functions
function formatDate(dateString) {
  return new Date(dateString).toLocaleDateString();
}

function formatTime(dateString) {
  return new Date(dateString).toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit",
  });
}

function timeAgo(dateString) {
  const now = new Date();
  const date = new Date(dateString);
  const diffInSeconds = Math.floor((now - date) / 1000);

  if (diffInSeconds < 60) return "Just now";
  if (diffInSeconds < 3600)
    return `${Math.floor(diffInSeconds / 60)} minutes ago`;
  if (diffInSeconds < 86400)
    return `${Math.floor(diffInSeconds / 3600)} hours ago`;
  return `${Math.floor(diffInSeconds / 86400)} days ago`;
}
