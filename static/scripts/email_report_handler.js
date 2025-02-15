document.addEventListener("DOMContentLoaded", function () {
    const sendReportButton = document.getElementById("sendReportButton");
    const emailMessage = document.getElementById("emailMessage");

    sendReportButton.addEventListener("click", function () {
        fetch(sendReportUrl, {  // ✅ Use global variable for URL
            method: "POST",
            headers: {
                "X-CSRFToken": csrfToken,
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                emailMessage.style.display = "block";  // ✅ Show success message
                setTimeout(() => emailMessage.style.display = "none", 3000);
            } else {
                alert("Error sending report. Please try again.");
            }
        })
        .catch(error => {
            console.error("Error:", error);
            alert("Network error. Please try again.");
        });
    });
});
