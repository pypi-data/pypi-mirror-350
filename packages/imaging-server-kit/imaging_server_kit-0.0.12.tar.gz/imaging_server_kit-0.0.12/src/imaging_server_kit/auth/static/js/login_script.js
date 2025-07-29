document.getElementById("login-form").addEventListener("submit", async function (event) {
    event.preventDefault();

    const email = document.getElementById("login-email").value;
    const password = document.getElementById("login-password").value;

    const formData = new FormData();
    formData.append("username", email);
    formData.append("password", password);

    const response = await fetch("http://localhost:8000/auth/jwt/login", {
        method: "POST",
        body: formData
    });

    const result = await response.json();

    if (response.ok) {
        localStorage.setItem("token", result.access_token); // Store token for future requests
        document.getElementById("message").innerText = "Login successful!";
    } else {
        document.getElementById("message").innerText = result.detail || "Login failed!";
    }
});
