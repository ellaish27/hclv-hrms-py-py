// static/js/main.js
function logout() {
  localStorage.removeItem('token');
  localStorage.removeItem('user');
  window.location.href = '/static/pages/login.html';
}

function terminate() {
  const employeeId = prompt("Enter employee ID to terminate:");
  if (!employeeId) return;

  fetch(`/api/admin/employees/${employeeId}/terminate`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('token')}`,
      'Content-Type': 'application/json'
    }
  })
  .then(res => res.json())
  .then(data => alert(data.message))
  .catch(err => alert('Error: ' + err.message));
}
