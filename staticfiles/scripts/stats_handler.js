document.addEventListener("DOMContentLoaded", function () {
    const ctx = document.getElementById("statsChart").getContext("2d");
    let chartInstance = null;
    let currencySymbol = "$";  // Default value

    function updateChart(data, label) {
        if (!data || Object.keys(data).length === 0) {
            document.getElementById("statsChart").style.display = "none";
            return;
        } else {
            document.getElementById("statsChart").style.display = "block";
        }

        if (chartInstance) {
            chartInstance.destroy(); // Destroy old chart before creating a new one
        }

        chartInstance = new Chart(ctx, {
            type: "bar",
            data: {
                labels: Object.keys(data),
                datasets: [{
                    label: label,
                    data: Object.values(data),
                    backgroundColor: "rgba(75, 192, 192, 0.2)",
                    borderColor: "rgba(75, 192, 192, 1)",
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return currencySymbol + value.toFixed(2);
                            }
                        }
                    }
                }
            }
        });
    }

    function fetchStatistics(filterType) {
        fetch(statsDataUrl)
            .then(response => response.json())
            .then(data => {
                if (!data) {
                    console.error("No data received");
                    return;
                }
                currencySymbol = data.currency_symbol || "$"; // ✅ Get currency symbol
                updateChart(data[filterType], `Total Spending by ${filterType}`);
                document.getElementById("mostBought").innerText = data.most_bought || "N/A";
                document.getElementById("leastBought").innerText = data.least_bought || "N/A";
            })
            .catch(error => console.error("Error loading statistics:", error));
    }

    document.getElementById("filter").addEventListener("change", function () {
        fetchStatistics(this.value);
    });

    // Load default statistics (Monthly) on page load
    fetchStatistics("monthly");
});
