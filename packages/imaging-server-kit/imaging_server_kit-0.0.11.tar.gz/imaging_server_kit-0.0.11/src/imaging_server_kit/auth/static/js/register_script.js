document.getElementById("register-form").addEventListener("submit", async function (event) {
    event.preventDefault();  // Prevent form from submitting normally

    const email = document.getElementById("register-email").value;
    const password = document.getElementById("register-password").value;

    const response = await fetch("http://localhost:8000/auth/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
    });

    const result = await response.json();
    document.getElementById("message").innerText = result.detail || "Registration successful!";
});
