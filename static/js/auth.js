// static/js/auth.js
document.addEventListener('DOMContentLoaded', () => {
  if (window.location.pathname.includes('login.html')) {
    document.getElementById('loginForm')?.addEventListener('submit', async (e) => {
      e.preventDefault();
      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;

      try {
        const res = await fetch('/api/auth/login', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({ email, password })
        });

        const data = await res.json();
        if (!res.ok) throw new Error(data.error || 'Login failed');

        localStorage.setItem('token', data.token);
        localStorage.setItem('user', JSON.stringify(data.user));

        const role = data.user.role;
        if (role === 'admin') window.location.href = '/static/pages/admin/dashboard.html';
        else if (role === 'hrOfficer') window.location.href = '/static/pages/hr/dashboard.html';
        else window.location.href = '/static/pages/employee/dashboard.html';

      } catch (err) {
        document.getElementById('error').textContent = err.message;
        document.getElementById('error').style.display = 'block';
      }
    });
  }
});
