document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("patient-form");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const data = {
            name: form[0].value,
            age: form[1].value,
            condition: form[2].value,
            resource: form[3].value
        };

        try {
            const res = await fetch("/api/patients", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data)
            });

            if(res.ok) {
                alert("Patient registered successfully!");
                form.reset();
                // TODO: refresh waiting list and resources
            } else {
                alert("Failed to register patient");
            }
        } catch(err) {
            console.error(err);
            alert("Error connecting to server");
        }
    });
});
